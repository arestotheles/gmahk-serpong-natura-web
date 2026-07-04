---
date: 2026-07-04
topic: gmahk-serpong-natura-website
---

# GMAHK Serpong Natura — Website Requirements

## Summary

A warm, mobile-friendly static website for **GMAHK Serpong Natura** in Indonesian, built with **Jekyll** and hosted on **GitHub Pages**. Six pages in navigation: Home, About, Service Times, Events, Berita, and Contact. Church admins publish Berita posts and Events as Markdown files in GitHub. Each post can store cover images, inline images, and PDF attachments on **GitHub** or **Amazon S3 (served via CloudFront)**, chosen per file in front matter. The first release uses placeholders until real content is supplied.

---

## Problem Frame

The church currently shares information only through social media. Newcomers searching for service times or directions have no dedicated home on the web. Members lack a stable archive for announcements and news beyond ephemeral social feeds. The site should welcome first-time visitors and keep the congregation informed, without requiring a CMS or paid hosting.

---

## Key Decisions

- **Jekyll on GitHub Pages** — Native GitHub Pages build keeps hosting and admin workflow simple; admin edits Markdown in the repo.
- **Berita as a dedicated nav page** — Home shows 1–2 latest Berita posts after Acara Mendatang with a “Lihat semua” link; full archive lives on Berita.
- **Events separate from Berita** — Dated calendar items (e.g. youth camp) on Events; longer news and announcements on Berita.
- **Welcome-first Home layout** — Photo-led hero, service times prominent, then Acara Mendatang, then Berita preview.
- **Per-file asset storage** — Each image or PDF declares `storage: github` or `storage: s3` in front matter; no site-wide lock-in.
- **Contact display-only** — Address, phone, email, and embedded map; no contact form or WhatsApp button in v1.
- **Indonesian only** — All visitor-facing content in Bahasa Indonesia.
- **Placeholder content for v1** — Logo, photos, and copy can ship as tasteful placeholders and be replaced later.

---

## Actors

- **A1. Visitor (newcomer)** — Finds the church online, needs service times, location, and a welcoming first impression.
- **A2. Member** — Checks announcements, Berita posts, and upcoming events.
- **A3. Admin** — GitHub-comfortable; creates and edits Markdown posts, commits images/PDFs to the repo or references S3 assets.

---

## Requirements

### Site structure and pages

- R1. The site exposes six pages in main navigation: Home, About (Tentang Kami), Service Times (Jadwal Ibadah), Events (Acara), Berita, and Contact (Kontak).
- R2. All pages are mobile-friendly and use a warm, welcoming visual tone.
- R3. The site is static, hosted on GitHub Pages, with no server-side application in v1.

### Home page

- R4. Home uses a welcome-first layout: hero with church/community imagery and welcoming message, service times visible without scrolling far, then Acara Mendatang, then 1–2 latest Berita posts with a “Lihat semua” link to the Berita page.
- R5. Home does not duplicate the full Berita archive or full Events list.

### Berita (news and announcements)

- R6. Berita is a blog-style archive ordered newest first.
- R7. Each Berita post is a Markdown file with at minimum: title, date, and body.
- R8. Each Berita post may include an optional cover image.
- R9. Each Berita post may include one or more PDF attachments (e.g. bulletin, handout) linked from the post.
- R10. Berita posts support inline images within the body.

### Events

- R11. Events page lists dated upcoming activities (title, date, short description); distinct from Berita articles.
- R12. Events are authored as Markdown files in GitHub, same admin workflow as Berita.

### Other pages

- R13. About page presents church identity, mission, and brief history (placeholder text acceptable in v1).
- R14. Service Times page shows worship schedule clearly (day, time, any notes such as Sabbath School vs divine service).
- R15. Contact page shows address, phone, email, and an embedded map; no form submission in v1.

### Asset storage (GitHub vs S3)

- R16. Each image (cover or inline) and each PDF attachment declares its storage location in post front matter: `github` or `s3`.
- R17. When `storage: github`, the asset file lives in the repository and is referenced by a repo-relative path.
- R18. When `storage: s3`, the asset is served from S3 via CloudFront; front matter carries the CloudFront URL (or equivalent public URL) for that asset.
- R19. The build/render pipeline resolves the correct URL per asset based on front matter without requiring duplicate posts for the same content.
- R20. Admin can mix storage backends within a single post (e.g. cover image on S3, PDF in GitHub).

### Admin workflow

- R21. Admin updates Berita and Events by adding or editing Markdown files in GitHub (web UI or local clone).
- R22. For `storage: github` assets, admin commits image/PDF files alongside or under a conventional assets path in the repo.
- R23. For `storage: s3` assets, admin uploads files to the church S3 bucket (outside the site build) and pastes the CloudFront URL into front matter.

### Content and language

- R24. All visitor-facing text is in Bahasa Indonesia.
- R25. v1 may ship with placeholder logo, photos, and copy; structure and layout must support swapping real content without redesign.

---

## Key Flows

- F1. **Admin publishes a Berita post with GitHub-hosted cover image**
  - **Trigger:** Admin has a new announcement with a small image.
  - **Actors:** A3
  - **Steps:** Create Markdown file with title, date, body, `storage: github` on cover image, commit image to repo, commit post, push to main; GitHub Pages rebuilds.
  - **Outcome:** Post appears on Berita and in Home preview when among the latest.

- F2. **Admin publishes a Berita post with S3-hosted assets**
  - **Trigger:** Admin has a large cover image or PDF bulletin.
  - **Actors:** A3
  - **Steps:** Upload image/PDF to S3; create Markdown with `storage: s3` and CloudFront URLs; commit and push post file only.
  - **Outcome:** Post displays images/PDFs from CloudFront; repo stays lean for large files.

- F3. **Newcomer finds service times**
  - **Trigger:** Visitor lands on Home from search or shared link.
  - **Actors:** A1
  - **Steps:** See hero and service times on Home; optionally open Service Times or Contact for detail and map.
  - **Outcome:** Visitor knows when and where to attend without asking on social media.

---

## Acceptance Examples

- AE1. **Berita post with mixed storage**
  - **Covers R16, R18, R20.**
  - **Given:** A Berita post with cover `storage: s3` and PDF attachment `storage: github`.
  - **When:** The site is built and the post is published.
  - **Then:** Cover loads from CloudFront; PDF link serves from the GitHub-hosted file; both appear on the Berita post page.

- AE2. **Home Berita preview**
  - **Covers R4, R6.**
  - **Given:** Five Berita posts exist, ordered by date.
  - **When:** A visitor opens Home.
  - **Then:** At most two latest posts appear after Acara Mendatang; “Lihat semua” navigates to the full Berita archive.

- AE3. **Event vs Berita separation**
  - **Covers R11, R6.**
  - **Given:** A dated youth camp on Events and a “no service this week” article on Berita.
  - **When:** Visitor browses both pages.
  - **Then:** Camp appears only on Events; announcement appears only on Berita (and Home preview if recent).

---

## Success Criteria

- A newcomer can find service times and location within two clicks from Home.
- Admin can publish a new Berita post (with optional image and PDF) using only GitHub and, when needed, S3 upload—without developer help after initial setup.
- Site renders correctly on mobile viewport widths common in Indonesia.
- GitHub Pages deploy succeeds on push to the publishing branch without manual build steps for routine content updates.

---

## Scope Boundaries

**Deferred for later**

- Contact form or WhatsApp click-to-chat button.
- English or bilingual content.
- Berita categories, tags, or filters.
- Automatic sync from Instagram/Facebook.
- Automated S3 upload from GitHub (admin uploads to S3 manually in v1).
- Member-only or login-gated content.
- Sermon audio/video hosting.
- Dedicated Downloads page (PDFs attach to Berita only in v1).

**Outside this product's identity**

- Full church management system (attendance, giving, roster).
- Live streaming platform.
- Mobile native app.

---

## Dependencies / Assumptions

- GitHub organization or account available for the repository and GitHub Pages.
- Custom domain optional; default `*.github.io` URL is acceptable for launch.
- AWS account with S3 bucket and CloudFront distribution configured for church media; CloudFront base URL known to admins.
- Admin understands when to use GitHub (smaller files, simpler workflow) vs S3 (larger images, PDFs, bandwidth).
- Church will supply real logo, photos, address, and service times before or after v1 launch.

---

## Outstanding Questions

**Deferred to Planning**

- Exact front matter field names for `storage`, image paths, and PDF attachment lists.
- S3 bucket naming, CloudFront path conventions, and CORS if needed.
- Whether Events support optional images with the same GitHub/S3 front matter pattern as Berita.
- GitHub Pages custom domain and SSL setup.
- Social media icon links in footer (Instagram/Facebook URLs)—likely yes but URLs TBD.

**Resolve Before Planning**

- None at this time.
