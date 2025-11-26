---
layout: page
permalink: /teaching/
title: teaching & resources
description: Materials for courses you taught. Replace this text with your description.
nav: true
nav_order: 6
horizontal: false
---

Welcome—this page collects courses, tutorials, and interactive demos. 
<style>
.teaching-tag {
  display: inline-block;
  padding: 3px 8px;
  margin: 0 6px 6px 0;
  background: #eef2ff;
  color: #314b8c;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}
</style>

{% assign visible_courses = site.courses | where_exp: "item", "item.hidden != true" %}
{% assign sorted_courses = visible_courses | sort: "importance" | reverse %}
<div class="row row-cols-1 row-cols-md-3">
  {% for course in sorted_courses %}
  <div class="col mb-4 d-flex">
    <a class="w-100" href="{% if course.redirect %}{{ course.redirect }}{% else %}{{ course.url | relative_url }}{% endif %}">
      <div class="card h-100 hoverable">
        {% if course.img %}
          {% include figure.liquid loading="eager" path=course.img sizes="350px" alt="thumbnail" class="card-img-top" %}
        {% endif %}
        <div class="card-body">
          {% if course.tags %}
            <div class="mb-2">
              {% for tag in course.tags %}
                <span class="teaching-tag">{{ tag }}</span>
              {% endfor %}
            </div>
          {% endif %}
          <h4 class="card-title">{{ course.title }}</h4>
          <p class="card-text">{{ course.description }}</p>
        </div>
      </div>
    </a>
  </div>
  {% endfor %}
</div>
