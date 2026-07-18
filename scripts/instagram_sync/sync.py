#!/usr/bin/env python3
"""Sync public Instagram posts into the Jekyll berita collection."""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import yaml

try:
    import instaloader
except ImportError:  # pragma: no cover - exercised in CI via requirements install
    instaloader = None


@dataclass(frozen=True)
class InstagramPost:
    shortcode: str
    caption: str
    date: datetime
    image_url: str
    post_url: str
    media_id: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_config(root: Path) -> dict:
    path = root / "_data" / "instagram.yml"
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return data or {}


def save_config(root: Path, config: dict) -> None:
    path = root / "_data" / "instagram.yml"
    with path.open("w", encoding="utf-8") as handle:
        yaml.dump(config, handle, allow_unicode=True, default_flow_style=False, sort_keys=False)


def derive_title(caption: str) -> str:
    first_line = caption.strip().split("\n")[0].strip() if caption else ""
    if not first_line:
        return "Postingan Instagram"
    return first_line[:80]


def derive_excerpt(caption: str) -> str:
    text = " ".join(caption.strip().split())
    if not text:
        return "Postingan dari Instagram."
    return text[:140]


def berita_filename(post: InstagramPost) -> str:
    return f"{post.date.strftime('%Y-%m-%d')}-ig-{post.shortcode}.md"


def berita_path(root: Path, post: InstagramPost) -> Path:
    return root / "_berita" / berita_filename(post)


def image_url_from_post(post: object) -> str:
    if getattr(post, "typename", None) == "GraphSidecar":
        return next(post.get_sidecar_nodes()).display_url  # type: ignore[attr-defined]
    if getattr(post, "is_video", False) and getattr(post, "video_url", None):
        return post.video_url  # type: ignore[attr-defined]
    display_url = getattr(post, "display_url", None)
    if display_url:
        return display_url
    return post.url  # type: ignore[attr-defined]


def instagram_post_from_loader(post: object) -> InstagramPost:
    shortcode = post.shortcode  # type: ignore[attr-defined]
    caption = post.caption or ""
    date = post.date_utc.replace(tzinfo=timezone.utc)  # type: ignore[attr-defined]
    return InstagramPost(
        shortcode=shortcode,
        caption=caption,
        date=date,
        image_url=image_url_from_post(post),
        post_url=f"https://www.instagram.com/p/{shortcode}/",
        media_id=str(post.mediaid),  # type: ignore[attr-defined]
    )


def configure_loader_context(
    loader: object,
    config: dict,
    *,
    login: str | None = None,
) -> None:
    username = login or os.environ.get("INSTAGRAM_USERNAME") or config.get("login_username")
    password = os.environ.get("INSTAGRAM_PASSWORD") or config.get("login_password")
    session_file = config.get("session_file")

    if not username:
        return

    if session_file:
        path = Path(session_file)
        if path.exists():
            loader.load_session_from_file(username, filename=str(path))  # type: ignore[attr-defined]
            return

    if password:
        loader.login(username, password)  # type: ignore[attr-defined]
        if session_file:
            loader.save_session_to_file(session_file)  # type: ignore[attr-defined]
        return

    try:
        loader.load_session_from_file(username)  # type: ignore[attr-defined]
    except FileNotFoundError as exc:
        raise RuntimeError(
            "Instagram login required. Set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD, "
            "or create a session file with: instaloader --login USERNAME"
        ) from exc


def fetch_posts_from_instagram(
    handle: str,
    *,
    limit: int | None = None,
    since: datetime | None = None,
    config: dict | None = None,
    login: str | None = None,
) -> list[InstagramPost]:
    if instaloader is None:
        raise RuntimeError("instaloader is not installed")

    config = config or {}
    loader = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
    )
    configure_loader_context(loader, config, login=login)

    try:
        profile = instaloader.Profile.from_username(loader.context, handle)
    except instaloader.exceptions.ProfileNotExistsException as exc:
        raise RuntimeError(
            f"Could not load Instagram profile @{handle}. Instagram often returns 403 for "
            "anonymous access, which Instaloader reports as 'profile does not exist'. "
            "Log in with the church Instagram account: set INSTAGRAM_USERNAME and "
            "INSTAGRAM_PASSWORD, then retry."
        ) from exc

    posts: list[InstagramPost] = []

    for post in profile.get_posts():
        if since and post.date_utc.replace(tzinfo=timezone.utc) <= since:
            continue
        posts.append(instagram_post_from_loader(post))
        if limit is not None and len(posts) >= limit:
            break

    return posts


def shortcode_from_url(url: str) -> str:
    match = re.search(r"instagram\.com/(?:p|reel|tv)/([^/?#]+)", url)
    if not match:
        raise ValueError(f"Not a valid Instagram post URL: {url}")
    return match.group(1)


def fetch_post_from_url(
    url: str,
    *,
    config: dict | None = None,
    login: str | None = None,
) -> InstagramPost:
    if instaloader is None:
        raise RuntimeError("instaloader is not installed")

    config = config or {}
    loader = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
    )
    configure_loader_context(loader, config, login=login)
    shortcode = shortcode_from_url(url)
    post = instaloader.Post.from_shortcode(loader.context, shortcode)
    return instagram_post_from_loader(post)


def render_markdown(post: InstagramPost) -> str:
    front_matter = {
        "title": derive_title(post.caption),
        "date": post.date.strftime("%Y-%m-%d"),
        "source": "instagram",
        "instagram_id": post.media_id,
        "instagram_url": post.post_url,
        "excerpt": derive_excerpt(post.caption),
        "cover": {
            "storage": "external",
            "url": post.image_url,
        },
    }
    body = post.caption.strip() or "_Tidak ada caption._"
    yaml_block = yaml.dump(front_matter, allow_unicode=True, default_flow_style=False, sort_keys=False)
    return f"---\n{yaml_block}---\n\n{body}\n"


def write_post(root: Path, post: InstagramPost) -> Path | None:
    path = berita_path(root, post)
    if path.exists():
        return None
    path.write_text(render_markdown(post), encoding="utf-8")
    return path


def parse_synced_at(value: object) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, str):
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    return None


def select_posts(
    posts: Iterable[InstagramPost],
    *,
    synced_ids: set[str],
    since: datetime | None,
) -> list[InstagramPost]:
    selected: list[InstagramPost] = []
    for post in posts:
        if post.media_id in synced_ids:
            continue
        if since and post.date <= since:
            continue
        selected.append(post)
    return selected


def sync_posts(root: Path, posts: list[InstagramPost], config: dict) -> int:
    synced_ids = set(str(item) for item in config.get("synced_post_ids") or [])
    created = 0
    latest = parse_synced_at(config.get("last_sync_at"))

    for post in posts:
        if post.media_id in synced_ids:
            continue
        if write_post(root, post) is not None:
            created += 1
            synced_ids.add(post.media_id)
            if latest is None or post.date > latest:
                latest = post.date

    config["synced_post_ids"] = sorted(synced_ids)
    if latest is not None:
        config["last_sync_at"] = latest.astimezone(timezone.utc).isoformat()
    save_config(root, config)
    return created


def run_bootstrap(root: Path, limit: int, login: str | None = None) -> int:
    config = load_config(root)
    if not config.get("enabled"):
        print("Instagram sync disabled (enabled: false). No changes made.")
        return 0

    handle = config.get("handle") or "gmahk_serpong_natura"
    posts = fetch_posts_from_instagram(handle, limit=limit, config=config, login=login)
    return sync_posts(root, posts, config)


def run_incremental(root: Path, login: str | None = None) -> int:
    config = load_config(root)
    if not config.get("enabled"):
        print("Instagram sync disabled (enabled: false). No changes made.")
        return 0
    if not config.get("bootstrap_verified"):
        print("Bootstrap not verified. Set bootstrap_verified: true before incremental sync.")
        return 0
    if not config.get("schedule_enabled"):
        print("Scheduler disabled (schedule_enabled: false). No changes made.")
        return 0

    handle = config.get("handle") or "gmahk_serpong_natura"
    since = parse_synced_at(config.get("last_sync_at"))
    posts = fetch_posts_from_instagram(handle, config=config, login=login)
    posts = select_posts(posts, synced_ids=set(config.get("synced_post_ids") or []), since=since)
    return sync_posts(root, posts, config)


def run_import_urls(root: Path, urls: list[str], login: str | None = None) -> int:
    config = load_config(root)
    if not config.get("enabled"):
        print("Instagram sync disabled (enabled: false). No changes made.")
        return 0

    posts = [fetch_post_from_url(url.strip(), config=config, login=login) for url in urls if url.strip()]
    return sync_posts(root, posts, config)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sync Instagram posts into _berita/")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--bootstrap", action="store_true", help="Import recent posts (one-time)")
    group.add_argument("--incremental", action="store_true", help="Import posts since last sync")
    group.add_argument(
        "--import-url",
        action="append",
        dest="import_urls",
        metavar="URL",
        help="Import a single post by URL (repeat for multiple)",
    )
    parser.add_argument("--limit", type=int, default=5, help="Bootstrap post count (default: 5)")
    parser.add_argument("--login", help="Instagram username (or set INSTAGRAM_USERNAME)")
    parser.add_argument("--root", type=Path, default=None, help="Repository root")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = args.root or repo_root()

    if args.bootstrap:
        created = run_bootstrap(root, args.limit, login=args.login)
    elif args.import_urls:
        created = run_import_urls(root, args.import_urls, login=args.login)
    else:
        created = run_incremental(root, login=args.login)

    print(f"Created {created} berita file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
