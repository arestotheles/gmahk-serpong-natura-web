# Instagram Berita Sync

Pulls posts from the public Instagram profile configured in `_data/instagram.yml` and writes Jekyll berita Markdown files.

## Why login is often required

Instagram frequently returns **403 Forbidden** for anonymous GraphQL requests. Instaloader then raises `ProfileNotExistsException` even when the profile exists (e.g. `@gmahk_serpong_natura`).

Use the **church Instagram account** credentials for sync — not a personal account unless that account manages the page.

## Local setup

```bash
pip install -r scripts/instagram_sync/requirements.txt
```

Set credentials (PowerShell):

```powershell
$env:INSTAGRAM_USERNAME = "your_church_ig_username"
$env:INSTAGRAM_PASSWORD = "your_password"
```

Optional: save a session file so you do not pass the password every time:

```bash
instaloader --login YOUR_USERNAME
```

Then set in `_data/instagram.yml`:

```yaml
login_username: YOUR_USERNAME
session_file: C:/Users/you/.config/instaloader/session-YOUR_USERNAME
```

## Commands

Bootstrap (last 5 posts; requires `enabled: true`):

```bash
python scripts/instagram_sync/sync.py --bootstrap --limit 5
```

Import specific posts by URL (useful when profile listing is blocked):

```bash
python scripts/instagram_sync/sync.py --import-url "https://www.instagram.com/p/SHORTCODE1/" --import-url "https://www.instagram.com/p/SHORTCODE2/"
```

Incremental sync (requires `enabled`, `bootstrap_verified`, and `schedule_enabled`):

```bash
python scripts/instagram_sync/sync.py --incremental
```

## Tests

```bash
python -m unittest discover -s scripts/instagram_sync
```

## GitHub Actions

Add repository secrets:

- `INSTAGRAM_USERNAME`
- `INSTAGRAM_PASSWORD`

The workflow passes these to the sync script automatically.
