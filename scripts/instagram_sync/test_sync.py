import unittest
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

from sync import (
    InstagramPost,
    berita_filename,
    derive_excerpt,
    derive_title,
    render_markdown,
    select_posts,
    shortcode_from_url,
    sync_posts,
    write_post,
)


class InstagramSyncHelpersTest(unittest.TestCase):
    def test_derive_title_from_first_line(self):
        caption = "Baris pertama judul\nBaris kedua isi."
        self.assertEqual(derive_title(caption), "Baris pertama judul")

    def test_derive_title_fallback(self):
        self.assertEqual(derive_title(""), "Postingan Instagram")

    def test_derive_excerpt_truncates(self):
        caption = "a" * 200
        self.assertEqual(len(derive_excerpt(caption)), 140)

    def test_render_markdown_includes_external_cover(self):
        post = InstagramPost(
            shortcode="ABC123",
            caption="Halo jemaat",
            date=datetime(2026, 7, 18, tzinfo=timezone.utc),
            image_url="https://cdninstagram.com/v/example.jpg",
            post_url="https://www.instagram.com/p/ABC123/",
            media_id="999",
        )
        markdown = render_markdown(post)
        self.assertIn("source: instagram", markdown)
        self.assertIn("storage: external", markdown)
        self.assertIn("https://cdninstagram.com/v/example.jpg", markdown)
        self.assertIn("Halo jemaat", markdown)

    def test_berita_filename_pattern(self):
        post = InstagramPost(
            shortcode="ABC123",
            caption="",
            date=datetime(2026, 7, 18, tzinfo=timezone.utc),
            image_url="https://example.com/a.jpg",
            post_url="https://www.instagram.com/p/ABC123/",
            media_id="1",
        )
        self.assertEqual(berita_filename(post), "2026-07-18-ig-ABC123.md")

    def test_shortcode_from_url(self):
        self.assertEqual(
            shortcode_from_url("https://www.instagram.com/p/ABC123/"),
            "ABC123",
        )
        self.assertEqual(
            shortcode_from_url("https://www.instagram.com/reel/XYZ789/?utm_source=ig"),
            "XYZ789",
        )

    def test_shortcode_from_url_invalid(self):
        with self.assertRaises(ValueError):
            shortcode_from_url("https://example.com/not-ig")


class InstagramSyncWriteTest(unittest.TestCase):
    def test_bootstrap_writes_posts_and_updates_state(self):
        posts = [
            InstagramPost(
                shortcode=f"POST{i}",
                caption=f"Caption {i}",
                date=datetime(2026, 7, 10 + i, tzinfo=timezone.utc),
                image_url=f"https://cdninstagram.com/v/{i}.jpg",
                post_url=f"https://www.instagram.com/p/POST{i}/",
                media_id=str(100 + i),
            )
            for i in range(5)
        ]

        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "_berita").mkdir()
            (root / "_data").mkdir()
            config = {
                "enabled": True,
                "schedule_enabled": False,
                "bootstrap_verified": False,
                "handle": "gmahk_serpong_natura",
                "last_sync_at": None,
                "synced_post_ids": [],
            }
            (root / "_data" / "instagram.yml").write_text(yaml.dump(config), encoding="utf-8")

            created = sync_posts(root, posts, config)

            self.assertEqual(created, 5)
            self.assertEqual(len(list((root / "_berita").glob("*.md"))), 5)
            saved = yaml.safe_load((root / "_data" / "instagram.yml").read_text(encoding="utf-8"))
            self.assertEqual(len(saved["synced_post_ids"]), 5)

    def test_incremental_skips_existing_ids(self):
        post = InstagramPost(
            shortcode="NEW1",
            caption="Baru",
            date=datetime(2026, 7, 20, tzinfo=timezone.utc),
            image_url="https://cdninstagram.com/v/new.jpg",
            post_url="https://www.instagram.com/p/NEW1/",
            media_id="200",
        )
        existing = InstagramPost(
            shortcode="OLD1",
            caption="Lama",
            date=datetime(2026, 7, 15, tzinfo=timezone.utc),
            image_url="https://cdninstagram.com/v/old.jpg",
            post_url="https://www.instagram.com/p/OLD1/",
            media_id="100",
        )

        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "_berita").mkdir()
            (root / "_data").mkdir()
            write_post(root, existing)
            config = {
                "enabled": True,
                "synced_post_ids": ["100"],
                "last_sync_at": "2026-07-15T00:00:00+00:00",
            }
            (root / "_data" / "instagram.yml").write_text(yaml.dump(config), encoding="utf-8")

            selected = select_posts([existing, post], synced_ids={"100"}, since=datetime(2026, 7, 15, tzinfo=timezone.utc))
            created = sync_posts(root, selected, config)

            self.assertEqual(created, 1)
            self.assertEqual(len(list((root / "_berita").glob("*.md"))), 2)


if __name__ == "__main__":
    unittest.main()
