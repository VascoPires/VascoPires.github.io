---
layout: page
title: Student supervision
description: Research-oriented theses and supervised projects, grouped by research topic.
permalink: /teaching/student-supervision/
resource_section: student-projects
importance: 9
---

<p><a href="{{ '/teaching/' | relative_url }}">Back to teaching &amp; resources</a></p>

This collection brings together research-oriented student projects and theses. Projects are grouped by research topic, with each project retaining its own question, contributors, and context.

{% assign projects = site.data.student_supervision.projects %}
{% if projects.size > 0 %}
{% assign themes = projects | group_by: 'theme' %}
{% for theme in themes %}

<section class="supervision-theme">
  <h2>{{ theme.name | escape }}</h2>
  <div class="row row-cols-1 row-cols-md-3">
    {% for project in theme.items %}
    <div class="col mb-4 d-flex">
      <article class="card h-100 w-100">
        <div class="card-body">
          <h3 class="card-title h4">{{ project.title | escape }}</h3>
          {% if project.context %}<p>{{ project.context | escape }}</p>{% endif %}
          <p class="card-text">{{ project.summary | escape }}</p>
          {% if project.url %}<a href="{{ project.url | relative_url }}">Read about the project</a>{% endif %}
        </div>
      </article>
    </div>
    {% endfor %}
  </div>
</section>
{% endfor %}
{% else %}
<h2>Research projects</h2>
<p>The individual projects will be added as this collection is organized.</p>
{% endif %}

For investigations built around everyday mechanics and nature, visit <a href="{{ '/teaching/do-it-labs/' | relative_url }}">Do it Labs</a>.
