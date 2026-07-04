---
layout: page
title: Kontak
permalink: /kontak/
---

Hubungi kami atau kunjungi gereja pada hari Sabtu.

## Alamat

{{ site.data.site.contact.address }}

## Telepon

[{{ site.data.site.contact.phone }}](tel:{{ site.data.site.contact.phone | replace: ' ', '' | replace: '-', '' }})

## Email

[{{ site.data.site.contact.email }}](mailto:{{ site.data.site.contact.email }})

## Peta

<div class="map-embed">
  <iframe
    src="{{ site.data.site.contact.map_embed_url }}"
    loading="lazy"
    referrerpolicy="no-referrer-when-downgrade"
    title="Peta lokasi GMAHK Serpong Natura"
    allowfullscreen>
  </iframe>
</div>

*Ganti embed peta dan detail kontak di `_data/site.yml` dengan informasi asli.*
