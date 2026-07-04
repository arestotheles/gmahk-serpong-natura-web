# GMAHK Serpong Natura — Website

Situs web statis gereja GMAHK Serpong Natura (Bahasa Indonesia), dibangun dengan **Jekyll 4** dan di-host di **GitHub Pages** via GitHub Actions.

## Halaman

- Beranda, Tentang Kami, Jadwal Ibadah, Acara, Berita, Kontak
- Admin memperbarui Berita dan Acara sebagai file Markdown di GitHub
- Media dapat disimpan di repositori GitHub atau di S3/CloudFront (per file)

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

1. Push ke branch `main`
2. Di repositori GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**
3. Workflow `.github/workflows/jekyll.yml` membangun dan menerbitkan situs

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
