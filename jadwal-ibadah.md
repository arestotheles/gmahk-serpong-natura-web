---
layout: page
title: Jadwal Ibadah
permalink: /jadwal-ibadah/
---

Berikut jadwal kebaktian rutin GMAHK Serpong Natura. *Ganti dengan jadwal resmi gereja.*

{% for slot in site.data.site.service_times %}
### {{ slot.name }}

- **Hari:** {{ slot.day }}
- **Waktu:** {{ slot.time }} WIB
{% if slot.note %}- **Catatan:** {{ slot.note }}{% endif %}

{% endfor %}

Kebaktian diadakan di lokasi gereja. Untuk petunjuk arah, kunjungi halaman [Kontak]({{ '/kontak/' | relative_url }}).
