# GMAHK Serpong Natura — Website

Situs web statis gereja GMAHK Serpong Natura (Bahasa Indonesia), dibangun dengan **Jekyll 4** dan di-host di **GitHub Pages** via GitHub Actions.

## Halaman

- **Beranda** — satu halaman scroll: Hero, Jadwal, Tentang, Acara, Berita, Kontak (navigasi anchor)
- **Arsip** — Berita (`/berita/`) dan Acara (`/acara/`) tetap halaman terpisah
- URL lama `/tentang-kami/`, `/jadwal-ibadah/`, `/kontak/` dialihkan ke bagian Beranda

Branch **`version2`** berisi layout v2 (free-flow, full-bleed). Branch `main` / `feat/church-website` tetap v1 sampai merge.

**Panduan admin:** [docs/admin-guide.md](docs/admin-guide.md)

## Prasyarat

- Ruby 3.2+ dan Bundler
- Git

## Pengembangan Lokal

```bash
bundle install
bundle exec jekyll serve
```

Buka http://localhost:4000/gmahk-serpong-natura-web (sesuaikan dengan `baseurl` di `_config.yml`).

## Tes

```bash
bundle exec rspec
bundle exec jekyll build
```

## Deploy ke GitHub Pages

1. **Aktifkan Pages sekali (wajib untuk repo baru):** GitHub repo → **Settings → Pages** → **Build and deployment** → **Source: GitHub Actions** (bukan "Deploy from a branch").
2. Push ke branch `main`
3. Workflow `.github/workflows/jekyll.yml` membangun dan menerbitkan situs

Jika workflow gagal dengan `Get Pages site failed` / `Not Found`, langkah 1 belum dilakukan. Workflow memakai `enablement: true` agar Pages bisa diaktifkan otomatis pada run pertama, tetapi beberapa akun/org tetap memerlukan pengaturan manual di Settings.

Setelah deploy pertama, situs tersedia di:

`https://<username-atau-org>.github.io/gmahk-serpong-natura-web/`

Ganti `url` dan `baseurl` di `_config.yml` jika nama repositori atau custom domain berbeda.

## Konten Placeholder

Logo, foto hero, teks, dan peta masih placeholder. Ganti melalui:

- `_data/site.yml` — info gereja dan kontak
- `assets/images/` — gambar
- `_berita/`, `_events/` — konten

## Lisensi

Konten gereja — hak cipta jemaat. Kode situs untuk penggunaan internal gereja.
