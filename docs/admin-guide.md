# Panduan Admin — GMAHK Serpong Natura Website

Panduan ini untuk admin yang memperbarui **Berita**, **Acara**, dan media melalui GitHub.

## Struktur Repositori

| Path | Isi |
|------|-----|
| `_data/home.yml` | Urutan dan on/off bagian Beranda (section registry) |
| `_data/about.yml` | Teks Tentang Kami di Beranda |
| `_data/site.yml` | Info gereja, jadwal, kontak, media sosial |
| `_berita/` | Artikel berita dan pengumuman |
| `_events/` | Acara dengan tanggal |
| `assets/images/` | Gambar di GitHub (kecil–sedang) |
| `assets/pdf/` | PDF di GitHub |

## Bagian Beranda (section registry)

File `_data/home.yml` mengatur bagian mana yang tampil di Beranda dan urutannya:

```yaml
sections:
  - id: hero
    enabled: true
  - id: jadwal
    enabled: true
  # ...
  - id: pengurus
    enabled: false   # ubah ke true setelah konten siap
```

Setiap `id` harus punya file partial di `_includes/home/<id>.html`. Untuk menambah bagian baru: buat partial, tambahkan entri di `home.yml`, set `enabled: true`.

Navigasi header memakai anchor (`/#tentang`, `/#jadwal`, dll.) ke bagian di Beranda.

## Menambah Berita

1. Buat file baru di `_berita/`, contoh: `2026-07-10-judul-singkat.md`
2. Isi front matter dan isi artikel:

```yaml
---
title: Judul Berita
date: 2026-07-10
excerpt: Ringkasan singkat untuk kartu berita.
cover:
  storage: github
  path: assets/images/nama-gambar.jpg
attachments:
  - label: Buletin PDF
    storage: github
    path: assets/pdf/buletin.pdf
---
```

Isi artikel dalam Markdown di bawah `---`.

3. Commit dan push ke branch `main`. GitHub Actions akan membangun ulang situs (biasanya beberapa menit).

## Menambah Acara

1. Buat file di `_events/`, contoh: `2026-08-01-nama-acara.md`
2. Front matter:

```yaml
---
title: Nama Acara
event_date: 2026-08-01
description: Deskripsi singkat untuk kartu acara.
cover:
  storage: github
  path: assets/images/acara.jpg
---
```

Halaman **Acara** menampilkan acara mendatang dan acara dalam 30 hari terakhir.

## GitHub vs S3 untuk Media

| Situasi | Pilih |
|---------|--------|
| Gambar/PDF kecil, jarang diubah | `storage: github` + commit file ke repo |
| File besar, banyak unduhan | `storage: s3` + upload manual ke bucket S3 |

### GitHub (`storage: github`)

```yaml
cover:
  storage: github
  path: assets/images/foto.jpg
```

Commit file gambar/PDF ke path yang sama di repositori.

### S3 + CloudFront (`storage: s3`)

1. Upload file ke bucket S3 gereja (AWS Console atau CLI).
2. Pastikan file dapat diakses melalui URL CloudFront.
3. Referensikan URL di front matter:

```yaml
cover:
  storage: s3
  url: https://dXXXXXXXX.cloudfront.net/path/file.jpg
attachments:
  - label: Buletin
    storage: s3
    url: https://dXXXXXXXX.cloudfront.net/buletin.pdf
```

**Campuran dalam satu artikel:** cover di S3, PDF di GitHub — didukung.

### Gambar di dalam artikel (inline)

- **GitHub:** `![alt]({{ '/assets/images/foto.jpg' | relative_url }})` atau path relatif sesuai panduan Jekyll.
- **S3:** gunakan URL CloudFront penuh: `![alt](https://dXXX.cloudfront.net/foto.jpg)`

## Kesalahan Front Matter

Jika `storage: github` tanpa `path`, atau `storage: s3` tanpa `url`, build GitHub Actions akan gagal dengan pesan error yang menjelaskan field yang kurang. Perbaiki file Markdown lalu push lagi.

## Memperbarui Info Gereja

Edit `_data/site.yml` untuk:

- Jadwal ibadah (ditampilkan di bagian Jadwal Beranda)
- Alamat, telepon, email (bagian Kontak Beranda)
- URL embed Google Maps (`map_embed_url`)
- Tautan Instagram/Facebook (kosongkan string `""` untuk menyembunyikan ikon)

Teks **Tentang Kami** di Beranda: edit `_data/about.yml`.

## Waktu Deploy

Setelah push ke `main`, tunggu workflow **Deploy Jekyll site to Pages** selesai di tab Actions GitHub. Situs live di URL GitHub Pages repositori.

## Bantuan

Lihat juga [README](../README.md) untuk setup developer lokal.
