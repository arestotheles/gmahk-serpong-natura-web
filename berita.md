---
layout: page
title: Berita
permalink: /berita/
---

Pengumuman dan artikel dari GMAHK Serpong Natura, terbaru di atas.

{% include berita-visible-posts-assign.html %}

<div class="card-grid">
{% for post in visible_berita %}
  {% include berita-card.html post=post %}
{% endfor %}
</div>

{% if visible_berita.size == 0 %}
<p class="empty-state">Belum ada berita. Admin dapat menambahkan artikel baru melalui GitHub.</p>
{% endif %}
