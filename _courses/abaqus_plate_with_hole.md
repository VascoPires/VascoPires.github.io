---
layout: page
title: "Abaqus Tutorial: 2D Plate with a Hole"
img: assets/img/plate_hole/cover.svg
importance: 4
tags: ["ABAQUS", "Tutorial"]
giscus_comments: false
date: 2025-10-03

# Hide the distill table of contents on this overview page
toc: false
---

# 2D Plate with a Hole — Tutorial Overview

This series walks through building, refining, and analyzing a plate-with-hole model in Abaqus/CAE. 

{% include figure.liquid path="assets/img/plate_hole/cover.svg" class="img-fluid rounded mb-3" alt="Abaqus plate-with-hole tutorial cover" %}

## Tutorial Parts
<style>
.part-card .card { border: 1px solid #e5e7eb; }
.part-card .card:hover { box-shadow: 0 6px 18px rgba(0,0,0,0.08); transform: translateY(-2px); transition: all 150ms ease; }
.part-tag { display: inline-block; padding: 3px 8px; margin-bottom: 6px; background: #eef2ff; color: #314b8c; border-radius: 4px; font-size: 12px; font-weight: 600; letter-spacing: 0.03em; }
</style>

<div class="row row-cols-1 row-cols-md-3 g-3 part-card mb-4">
  <div class="col d-flex">
    <a class="w-100" href="{{ '/courses/abaqus_tutorial_part1/' | relative_url }}">
      <div class="card h-100 hoverable">
        <img class="card-img-top" src="{{ 'assets/img/plate_hole/tut1.svg' | relative_url }}" alt="Part 1 thumbnail">
        <div class="card-body">
          <span class="part-tag">Part 1</span>
          <h5 class="card-title mb-2">Setting a Quick Model</h5>
          <p class="card-text">Geometry, materials, meshing, BCs, and running the base plate-with-hole.</p>
        </div>
      </div>
    </a>
  </div>
  <div class="col d-flex">
    <a class="w-100" href="{{ '/courses/abaqus_tutorial_part2/' | relative_url }}">
      <div class="card h-100 hoverable">
        <img class="card-img-top" src="{{ 'assets/img/plate_hole/tut2.svg' | relative_url }}" alt="Part 2 thumbnail">
        <div class="card-body">
          <span class="part-tag">Part 2</span>
          <h5 class="card-title mb-2">Taking Advantage of Symmetries</h5>
          <p class="card-text">Use symmetry planes to shrink the model and keep loads/BCs consistent.</p>
        </div>
      </div>
    </a>
  </div>
  <div class="col d-flex">
    <a class="w-100" href="{{ '/courses/abaqus_tutorial_part3/' | relative_url }}">
      <div class="card h-100 hoverable">
        <img class="card-img-top" src="{{ 'assets/img/plate_hole/tut3.svg' | relative_url }}" alt="Part 3 thumbnail">
        <div class="card-body">
          <span class="part-tag">Part 3</span>
          <h5 class="card-title mb-2">Getting a Good Mesh</h5>
          <p class="card-text">Element choice, refinement near the hole, and quick quality checks.</p>
        </div>
      </div>
    </a>
  </div>
  <div class="col d-flex">
    <a class="w-100" href="{{ '/courses/abaqus_tutorial_part4/' | relative_url }}">
      <div class="card h-100 hoverable">
        <img class="card-img-top" src="{{ 'assets/img/plate_hole/tut4.svg' | relative_url }}" alt="Part 4 thumbnail">
        <div class="card-body">
          <span class="part-tag">Part 4</span>
          <h5 class="card-title mb-2">Analyzing the Stress Concentration</h5>
          <p class="card-text">Extract stresses along paths and interpret concentration factors.</p>
        </div>
      </div>
    </a>
  </div>
  <div class="col d-flex">
    <a class="w-100" href="{{ '/courses/abaqus_tutorial_part5/' | relative_url }}">
      <div class="card h-100 hoverable">
        <img class="card-img-top" src="{{ 'assets/img/plate_hole/tut5.svg' | relative_url }}" alt="Part 5 thumbnail">
        <div class="card-body">
          <span class="part-tag">Part 5</span>
          <h5 class="card-title mb-2">Different Material Behaviours</h5>
          <p class="card-text">Swap materials, test plastic/viscoelastic options, and compare responses.</p>
        </div>
      </div>
    </a>
  </div>
</div>



### What you’ll learn

- Set up geometry, materials, meshing, and boundary conditions for the plate-with-hole (Part 1).
- Use symmetry to shrink models and align loads/BCs (Part 2).
- Improve mesh quality and refine near stress raisers (Part 3).
- Extract and interpret stress concentrations around the hole (Part 4).
- Explore different material behaviors and compare responses (Part 5).
