---
layout: page
title: agent log
permalink: /agent-log/
nav: false
description: Running notes for assistant work sessions.
---

## Session 2025-11-24

- Teaching page now shows a card grid with tags (Course/Tutorial/Demo/Interactive) fed by `_courses/`.
- Added entries in `_courses/`: Example Course (tag Course), Abaqus Tutorials stub (tag Tutorial), Stress Tensor Visualizer (tags Demo, Interactive) redirecting to `/tensor-vis/`.
- Tensor visualizer lives at `_pages/tensor-vis.html` with a back link to `/teaching/`; uses CDN MathJax and three.js.
- Serve locally with `bundle exec jekyll serve --host 0.0.0.0 --port 8081 --livereload-port 35730 --force_polling --verbose` to avoid port conflicts.
- Open items: populate Abaqus tutorials content, add more courses/demos with tags, decide if tensor assets should be hosted locally, optionally add a nav link to teaching or the demo.
- Hidden placeholders for now: `_courses/example_course.md` and `_courses/abaqus_tutorials.md` (hidden flag in front matter); `_pages/projects.md` (book notes page) removed from nav but kept accessible. Plan to unhide once content is ready.

### Future work (user ideas)
- Blog integration pulling posts from Substack (catenaries topic).
- Teaching showcase for Do It Labs tree optimization with FEM.
- Add CASIer work in Python as a teaching/demo item.
- Conferences to add: CompTest, Vienna, Maria 2026, Leoben.
- Papers to add: Maria’s paper, Wally’s paper.
- Document “ReadDaily” / DIY ReadWise setup.
- Abaqus plate-with-a-hole tutorial/demo.
