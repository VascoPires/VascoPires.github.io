---
layout: page
permalink: /teaching/
title: teaching & resources
description:
nav: true
nav_order: 6
horizontal: false
resource_sections:
  - id: teaching-tools
    title: Teaching tools
  - id: courses-tutorials
    title: Courses & tutorials
  - id: student-projects
    title: Student projects
    hidden: true # remove to show the section again
---

Teaching tools, courses, and tutorials for students, educators, and anyone curious about mechanics and materials.

<style>
.teaching-section {
  margin-top: 2.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--global-divider-color);
}

.teaching-section h2 {
  margin-bottom: 0.5rem;
}

.teaching-section-description {
  max-width: 46rem;
  margin-bottom: 1.5rem;
  color: var(--global-text-color-light);
}

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
{% for section in page.resource_sections %}
{% if section.hidden %}{% continue %}{% endif %}

<section class="teaching-section" aria-labelledby="{{ section.id }}">
  <h2 id="{{ section.id }}">{{ section.title }}</h2>
  <p class="teaching-section-description">{{ section.description }}</p>
<div class="row row-cols-1 row-cols-md-3">
  {% for course in sorted_courses %}
  {% assign resource_section = course.resource_section | default: "courses-tutorials" %}
  {% if resource_section == section.id %}
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
          <h3 class="card-title h4">{{ course.title }}</h3>
          <p class="card-text">{{ course.description }}</p>
        </div>
      </div>
    </a>
  </div>
  {% endif %}
  {% endfor %}
</div>
</section>
{% endfor %}
