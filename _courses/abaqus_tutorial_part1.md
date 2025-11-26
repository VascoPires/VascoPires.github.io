---
layout: distill
title: "Part 1: Setting a Quick Model"
description: "Full step-by-step Abaqus/CAE walkthrough for the plate-with-hole: geometry, materials, meshing, BCs, run, and results."
img: assets/img/teaching/2d_plate/files/plate_part.png
importance: 4
tags: ["ABAQUS", "Tutorial"]
giscus_comments: true
date: 2025-10-03
hidden: true
nav: false
---

# 2D Plate with a Hole

Now that we have covered some fundamentals and learned how to operate within Abaqus/CAE, let’s walk through a complete example: a plate with a central hole under tension.

{% include figure.liquid path="assets/img/teaching/2d_plate/plate.png" title="Sketch of the 2D plate with a central hole." class="img-fluid rounded" %}

| ⚙️ Parameter       | 📏 Value |
| ------------------ | -------- |
| Plate length, $L$  | 100 mm   |
| Plate height, $H$  | 20 mm    |
| Hole diameter, $D$ | 10 mm    |

## 🗂️ Sketch & Setup

Open Abaqus/CAE, set the working directory, and start a `Standard/Explicit Model`.

{% include figure.liquid path="assets/img/teaching/2d_plate/files/welcome_window.png" title="Abaqus/CAE start window." class="img-fluid rounded" %}
<div class="caption">Start Session dialog in Abaqus/CAE.</div>

## 🧩 Geometry

Create a new part with `2D Planar → Deformable → Shell`. Draw a rectangle (🟦), add construction lines (➕) through the midpoint, and insert a centered circle for the hole. Keep the profile closed—open contours will fail part creation. Then dimension and constrain until the sketch is fully defined (green).

> **Warning — Shell options:** 2D Planar shells use solid sections/elements; 3D shell parts use shell sections/elements. Pick 2D Planar here.

{% include figure.liquid path="assets/img/teaching/2d_plate/files/sketch_2d.png" title="Initial sketch with rectangle and construction lines." class="img-fluid rounded" %}
<div class="caption">Plate outline with construction lines through the midpoint.</div>
{% include figure.liquid path="assets/img/teaching/2d_plate/files/sketch_dim.png" title="Applying dimensions to the sketch." class="img-fluid rounded" %}
<div class="caption">Apply dimensions to match the target sizes.</div>
{% include figure.liquid path="assets/img/teaching/2d_plate/files/sketch_fully_defined.png" title="Fully defined sketch (all green) at the end of constraining." class="img-fluid rounded" %}
<div class="caption">Fully defined sketch; yellow would mean overdefined.</div>
{% include figure.liquid path="assets/img/teaching/2d_plate/files/plate_part.png" title="Part created after finishing the sketch." class="img-fluid rounded" %}
<div class="caption">Part after exiting the sketch.</div>

## 🧪 Material and Section

Define a material (e.g., PMA) with isotropic elasticity: $E = 3\,$GPa, $\nu = 0.4$. Keep units consistent (mm/N → MPa).

{% include figure.liquid path="assets/img/teaching/2d_plate/files/material_property.png" title="Defining an elastic material." class="img-fluid rounded" %}
<div class="caption">Mechanical → Elasticity → Elastic.</div>
{% include figure.liquid path="assets/img/teaching/2d_plate/files/material_prop2.png" title="Selecting isotropic elasticity and entering properties." class="img-fluid rounded" %}
<div class="caption">Enter properties in MPa to stay consistent with mm/N units.</div>

Create a solid section and assign it to the part.

{% include figure.liquid path="assets/img/teaching/2d_plate/files/section.png" title="Creating a solid section." class="img-fluid rounded" %}
{% include figure.liquid path="assets/img/teaching/2d_plate/files/section_assign.png" title="Assigning the section to the part." class="img-fluid rounded" %}
<div class="caption">Sections bridge materials to geometry; every element needs one.</div>

### Extra detail screenshots

{% include figure.liquid path="assets/img/teaching/2d_plate/attachments/5e33465c182e5d07c0220345130f40c1.png" title="Selecting Elastic under Mechanical > Elasticity." class="img-fluid rounded" %}
{% include figure.liquid path="assets/img/teaching/2d_plate/attachments/02292e9ac2d463b95fbcd39d36d2af2e.png" title="Entering Young’s modulus and Poisson’s ratio (isotropic)." class="img-fluid rounded" %}

## 🧩 Assembly and Mesh

The assembly is what the solver actually sees. Create an **Instance** of your part. Dependent instances keep part-level numbering; independent instances renumber globally. For this simple case, use a **dependent** instance and proceed to meshing.

Seed with a global size ≈ 1.5 and generate the mesh.

{% include figure.liquid path="assets/img/teaching/2d_plate/files/assembly.png" title="Part instance placed in the assembly." class="img-fluid rounded" %}
<div class="caption">Use a dependent instance so meshing stays at part level.</div>
{% include figure.liquid path="assets/img/teaching/2d_plate/files/mesh.png" title="Mesh generated for the plate with a hole." class="img-fluid rounded" %}
<div class="caption">Coarse seed (≈1.5) for a quick run; refine later if needed.</div>

## 🧷 Boundary Conditions

First, create a static general step (General → Static, General). Static time is a loading parameter, not real time; dynamic analyses track physical time.

{% include figure.liquid path="assets/img/teaching/2d_plate/files/step.png" title="Static general step creation." class="img-fluid rounded" %}
<div class="caption">General → Static, General.</div>

Apply displacement BCs on left and right edges: $u_x = -1.5$ mm (left) and $u_x = +1.5$ mm (right) to apply tension.

{% include figure.liquid path="assets/img/teaching/2d_plate/files/bc_config.png" title="Boundary condition dialog." class="img-fluid rounded" %}
{% include figure.liquid path="assets/img/teaching/2d_plate/files/disp_BC.png" title="Applying symmetric displacement boundary conditions." class="img-fluid rounded" %}
<div class="caption">Ensure U1 is along the x-axis; use opposite signs on each side.</div>

### Extra detail screenshot

{% include figure.liquid path="assets/img/teaching/2d_plate/attachments/497c3bb48578a877295dc14df83ca994.png" title="Displacement BCs with opposite signs." class="img-fluid rounded" %}

## 🚀 Job and Output

Create and submit a job (e.g., `plate_with_hole`), monitor it in the Job Monitor, then open the Visualization module to inspect results (e.g., von Mises stress).

{% include figure.liquid path="assets/img/teaching/2d_plate/files/job_creation.png" title="Job creation dialog." class="img-fluid rounded" %}
<div class="caption">Create a job and point it to the current model.</div>
{% include figure.liquid path="assets/img/teaching/2d_plate/files/submit_job.png" title="Submitting the job." class="img-fluid rounded" %}
<div class="caption">Submit and watch the Job Monitor for progress/warnings.</div>

{% include figure.liquid path="assets/img/teaching/2d_plate/files/mises_2d_plate.png" title="Von Mises stress contour showing stress concentration around the hole." class="img-fluid rounded" %}
<div class="caption">Von Mises stress contours highlighting the stress concentration at the hole.</div>
