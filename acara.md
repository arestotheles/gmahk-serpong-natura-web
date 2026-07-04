---
layout: page
title: Acara
permalink: /acara/
---

Kegiatan dan acara mendatang jemaat GMAHK Serpong Natura.

{% assign now_ts = 'now' | date: '%s' | plus: 0 %}
{% assign cutoff_ts = now_ts | minus: 2592000 %}
{% assign visible_events = site.events | sort: 'event_date' | reverse %}

<div class="card-grid">
{% for event in visible_events %}
  {% assign event_ts = event.event_date | date: '%s' | plus: 0 %}
  {% if event_ts >= cutoff_ts %}
    {% include event-card.html event=event %}
  {% endif %}
{% endfor %}
</div>

{% if visible_events.size == 0 %}
<p class="empty-state">Belum ada acara untuk ditampilkan.</p>
{% endif %}
