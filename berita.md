---
layout: page
title: Berita
permalink: /berita/
---

Pengumuman dan artikel dari GMAHK Serpong Natura, terbaru di atas.

{% assign sorted_berita = site.berita | sort: 'date' | reverse %}

<div class="card-grid">
{% for post in sorted_berita %}
  {% include berita-card.html post=post %}
{% endfor %}
</div>

{% if sorted_berita.size == 0 %}
<p class="empty-state">Belum ada berita. Admin dapat menambahkan artikel baru melalui GitHub.</p>
{% endif %}
