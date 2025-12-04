---
layout: distill
title: "Part 1: Setting a Quick Model"
description: "Full step-by-step Abaqus/CAE walkthrough for the plate-with-hole: geometry, materials, meshing, BCs, run, and results."
img: assets/img/plate_hole/tut1.svg
importance: 4
tags: ["ABAQUS", "Tutorial"]
giscus_comments: false
date: 2025-10-03
hidden: true
nav: false
---

# 2D Plate with a Hole

<div class="d-flex justify-content-between flex-wrap gap-2 tutorial-nav mb-3">
  <a class="btn btn-outline-primary" href="{{ '/courses/abaqus_plate_with_hole/' | relative_url }}">← Back to tutorial overview</a>
  <a class="btn btn-primary" href="{{ '/courses/abaqus_tutorial_part2/' | relative_url }}">Next: Part 2 →</a>
</div>

Now that we have covered some fundamentals and learned how to operate within Abaqus/CAE, let’s walk through a complete example: a plate with a central hole under tension, as shown in [Figure 1](#fig:plate-with-hole).


{% include figure.liquid path="assets/img/teaching/2d_plate/plate.png" title="Sketch of the 2D plate with a central hole." class="img-fluid rounded article-figure" id="fig:plate-with-hole" %}
<div class="caption">Sketch of the 2D plate with a central hole.</div>

<table class="table">
  <thead>
    <tr>
      <th scope="col">⚙️ Parameter</th>
      <th scope="col">📏 Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Plate length, $L$</td>
      <td>100 mm</td>
    </tr>
    <tr>
      <td>Plate height, $H$</td>
      <td>20 mm</td>
    </tr>
    <tr>
      <td>Hole diameter, $D$</td>
      <td>10 mm</td>
    </tr>
  </tbody>
</table>
<div id="tab-plate_dimensions" class="caption table-caption"><strong>Table 1:</strong> Geometric dimensions of the 2D plate with a hole.</div>

## 🗂️ Sketch & Setup

The first step is to set up the working directory. After opening Abaqus, either manually select the working directory from the top of the GUI or open the command prompt in the desired folder and type:

```cmd
abaqus cae
```

In the **Start Session** dialog, choose `Standard/Explicit Model` to begin.

{% include figure.liquid path="assets/img/teaching/2d_plate/files/welcome_window.png" title="Abaqus/CAE start window." class="img-fluid rounded article-figure" %}
<div class="caption">Start Session dialog in Abaqus/CAE.</div>

## 🧩 Geometry

The first step of any model is defining the geometry.  
In the **Part** module, select:

$$
\text{Create Part} \; \rightarrow \; \text{2D Planar} \; \rightarrow \; \text{Deformable} \; \rightarrow \; \text{Shell}.
$$

This means we are creating a 2D deformable part using the *Shell* option, which defines an area.  

<aside>
  <p>If we had chosen <strong>Wire</strong>  instead (as seen in the figure), we would have created a 1D part (for example, a truss).</p>
</aside>


<div class="callout warning">
  <div class="callout-title"><span class="callout-icon">⚠️</span><span>Shell definition</span></div>
  <div class="callout-body">A common source of confusion is the difference between the <strong>3D shell</strong> and <strong>2D planar</strong> options. When you are modelling a <em>Part</em> they can look almost the same, but they are fundamentally different. 
  
  A 3D shell is a shell or plate embedded in full 3D space, so out-of-plane behaviour is included and you work with shell sections and shell elements. A 2D planar model, on the other hand, is truly two-dimensional (plane stress/plane strain or axisymmetric), and there you use solid sections and continuum elements instead.</div>
</div>

{% include figure.liquid path="assets/img/teaching/2d_plate/files/part_module.png" title="Abaqus Part module." class="img-fluid rounded article-figure" %}
<div class="caption">Part module and sketch toolbar (rectangle, construction lines, circle).</div>

First, select the 🟦 rectangle tool (*Create Lines: Rectangle (4 Lines)*) and draw it roughly at the center.  Next, add horizontal and vertical construction lines through the midpoint of the sketch. These construction lines serve as auxiliary references and do not form part of the geometry.  

At this point, your sketch should look similar to [Figure 2](#fig-sketch_2d).  
Now, add a circular hole at the center by selecting the circle tool and clicking in the middle of the plate.  Ensure the sketch forms a closed contour - Abaqus requires closed profiles for part creation. Open profiles will cause an error.


{% include figure.liquid path="assets/img/teaching/2d_plate/files/sketch_2d.png" title="Initial sketch with rectangle and construction lines." class="img-fluid rounded article-figure" id="fig-sketch_2d" %}
<div class="caption">Plate outline with construction lines through the midpoint.</div>

Next, apply the dimensions according to [Table 1](#tab-plate_dimensions).  
Use the dimension tool (*second column, fourth row*) from the sketch toolbar.


{% include figure.liquid path="assets/img/teaching/2d_plate/files/sketch_dim.png" title="Applying dimensions to the sketch." class="img-fluid rounded article-figure" %}
<div class="caption">Apply dimensions to match the target sizes.</div>


Finally, center the sketch at the origin.  Create a point at $(0,0)$, apply the **Fixed** constraint to it, and then use the **Coincident** constraint to align the circle center with this point.  

When a sketch is *fully defined*, all lines appear green (see [Figure 3](#fig-sketch_fully_defined)).  If it becomes *overdefined* ⚠️ (e.g., due to conflicting constraints), the lines turn yellow and the conflicting constraints appear in purple.


{% include figure.liquid path="assets/img/teaching/2d_plate/files/sketch_fully_defined.png" title="Fully defined sketch (all green) at the end of constraining." class="img-fluid rounded article-figure" id="fig-sketch_fully_defined" %}
<div class="caption">Fully defined sketch; yellow would mean overdefined.</div>

Press **Done** ✔️ at the bottom of the sketch window to create the part.  
At this point, you have your part created inside the Part module, as shown in [Figure 4](#fig-plate_part). With this, the geometry section of the model is complete.

{% include figure.liquid path="assets/img/teaching/2d_plate/files/plate_part.png" title="Part created after finishing the sketch." class="img-fluid rounded article-figure" id="fig-plate_part" %}
<div class="caption">Part after exiting the sketch.</div>

## 🧪 Material and Section

In Abaqus, material properties are defined within the *Property* module 🧱.  So let's create a PMA material with the following elastic properties (isotropic): $E=3 \; \text{GPa}$  ; $\nu = 0.4$. For this we are going to create a material and then select:

$$
\text{Mechanical} \; \rightarrow \; \text{Elasticity} \; \rightarrow \; \text{Elastic}
$$

as shown in [the elastic material dialog](#fig-material_property). Then, select "Isotropic" (see [the isotropic property entry dialog](#fig-material_prop2)) as the type and insert the young's modulus and the poison coefficient. Pay attention to the **units** ⚠️! Since we are working in **millimeters (mm)** and **newtons (N)**, our elastic properties must be in **megapascals (MPa)** to maintain dimensional consistency 📏.

{% include figure.liquid path="assets/img/teaching/2d_plate/files/material_property.png" title="Defining an elastic material." class="img-fluid rounded article-figure" id="fig-material_property" %}
<div class="caption">Mechanical → Elasticity → Elastic.</div>
{% include figure.liquid path="assets/img/teaching/2d_plate/files/material_prop2.png" title="Selecting isotropic elasticity and entering properties." class="img-fluid rounded article-figure" id="fig-material_prop2" %}
<div class="caption">Enter properties in MPa to stay consistent with mm/N units.</div>

The second step is defining a **section**.  A section is, in essence, the _middle layer_ between the material definition and the geometry. While the **material** defines _how_ a material behaves, the **section** specifies _how_ that material will be represented or simplified in your model. For instance, with the same material, you could create a **solid**, **shell**, or **beam** section - each producing different structural behaviors depending on the modeling assumptions. So even if this feels a bit abstract now, it’s enough to remember that the _section_ combines both the material and the modeling approach. Every element in your model must be assigned a section, and this step ensures that Abaqus knows how to interpret the material response of your geometry.

{% include figure.liquid path="assets/img/teaching/2d_plate/files/section.png" title="Creating a solid section." class="img-fluid rounded article-figure" %}
<div class="caption">Creating a solid section.</div>
{% include figure.liquid path="assets/img/teaching/2d_plate/files/section_assign.png" title="Assigning the section to the part." class="img-fluid rounded article-figure" %}
<div class="caption">Assigning the section to the part.</div>

## 🧩 Assembly

Moving on to the **assembly** step.  The assembly module represents what the **solver actually sees** . You might create several parts in the Part module, but only those you create instances of it in the assembly will be used for simulation. Even if you have just one part, you still need to create an assembly instance. You’re essentially telling the solver: “here’s the part I want to analyze".

To do this, create an **Instance**.  An instance is a placed copy of a part within the assembly. You can have multiple instances of the same part, for example, a connection with 10 identical bolts can be modeled using one bolt geometry and section, but repeated as multiple instances.

{% include figure.liquid path="assets/img/teaching/2d_plate/files/assembly.png" title="Part instance placed in the assembly." class="img-fluid rounded article-figure" %}
<div class="caption">Use a dependent instance so meshing stays at part level.</div>

When creating an instance, Abaqus will ask whether it should be **dependent** or **independent**.  A **dependent instance** means the mesh is created at the _part level_, while an **independent instance** allows meshing at the _assembly level_.

The distinction mainly affects how nodes and elements are numbered:

- In an **independent instance**, all nodes and elements share a _global numbering system_ across the entire assembly (no duplicates).

- In a **dependent instance**, each part maintains its own numbering (so, for example, Element ID = 1 could exist in multiple parts).

The conceptual difference is shown in [Figure 13](#fig-independent-dependent).

{% include figure.liquid path="assets/img/teaching/2d_plate/files/independent_dependent_mesh.svg" title="Independent vs. dependent instances for meshing." class="img-fluid rounded wide-figure article-figure" id="fig-independent-dependent" %}
<div class="caption">Dependent instances share the part mesh; independent instances mesh per assembly instance.</div>

Now, onto the **meshing** step. Meshing is one of the most important parts of any finite element analysis, but here we’ll focus on the basics just to get our model running. Start by defining a **global seed size** of approximately _1.5_.  Then, click on the **mesh icon** (second row, first position) to generate the mesh for your part.  The expected result is shown in [Figure 14](#fig-mesh).

{% include figure.liquid path="assets/img/teaching/2d_plate/files/mesh.png" title="Mesh generated for the plate with a hole." class="img-fluid rounded article-figure" id="fig-mesh" %}
<div class="caption">Coarse seed (≈1.5) for a quick run; refine later if needed.</div>

At this stage, you can perform several operations, such as assigning **element types**, changing the **meshing scheme**, or adjusting **seed sizes**. However, since this is just an introductory example, we’ll leave those for later sections.

## 🧷 Boundary Conditions

The final step before running the simulation is to apply the **boundary conditions**.  Before doing so, take a look at the initial sketch and think about which boundary conditions make physical sense here.


But first, let’s create a **step**  -  this defines the simulation’s time frame.  In Abaqus, analyses can generally be **static** or **dynamic**.

- In a _dynamic (explicit or implicit)_ simulation, the time variable represents _real physical time_.

- In a _static_ analysis, time is _not physical_ but simply a _loading parameter_, indicating how loads are gradually applied.


For this example, we’ll perform a **static analysis**, the simplest type. Create a new step by navigating to:  

$$
\text{Step} \; \rightarrow \; \text{Procedure type: General} \; \rightarrow \; \text{Static, General}
$$

and name it `loading_step`, as shown below.

{% include figure.liquid path="assets/img/teaching/2d_plate/files/step.png" title="Static general step creation." class="img-fluid rounded article-figure" %}
<div class="caption">General → Static, General.</div>

Now, we can define the **boundary conditions**. According to the sketch, we want to apply a **displacement** on both sides of the plate.  

Click the boundary condition icon (second row, first column) and select:

$$
\text{Mechanical} \; \rightarrow \; \text{Displacement/Rotation} \; \rightarrow \; \text{U1:} \; \pm 1.5 \; \rightarrow \; \text{Amplitude: Ramp}
$$

<div class="callout tip">
  <div class="callout-title"><span class="callout-icon">↔️</span><span>Displacement direction</span></div>
  <div class="callout-body">By default, U1 follows the assembly x-axis. Use a negative sign on the left side and a positive sign on the right side to pull the plate in tension.</div>
</div>

{% include figure.liquid path="assets/img/teaching/2d_plate/files/bc_config.png" title="Boundary condition dialog." class="img-fluid rounded article-figure" %}
{% include figure.liquid path="assets/img/teaching/2d_plate/files/disp_BC.png" title="Applying symmetric displacement boundary conditions." class="img-fluid rounded article-figure" %}
<div class="caption">Ensure U1 is along the x-axis; use opposite signs on each side.</div>

## 🚀 Job and Output

Now that the model is ready, let’s create and submit a **job**.  
The job module is where we tell Abaqus to actually run the simulation we’ve set up.

1. Go to the **Job** module and create a new job:
2. Assign a name to the job (e.g., `plate_with_hole`) and verify that it references your current model.
3. In the job settings, you can see basic options such as analysis type, description, and memory allocation.

{% include figure.liquid path="assets/img/teaching/2d_plate/files/job_creation.png" title="Job creation dialog." class="img-fluid rounded article-figure" %}
<div class="caption">Create a job and point it to the current model.</div>
{% include figure.liquid path="assets/img/teaching/2d_plate/files/submit_job.png" title="Submitting the job." class="img-fluid rounded article-figure" %}
<div class="caption">Submit and watch the Job Monitor for progress/warnings.</div>

Once everything is ready, click **Submit** ▶️ to start the analysis. You can monitor its progress in the **Job Monitor**, which displays information such as completion status, warnings, and estimated time.

{% include figure.liquid path="assets/img/teaching/2d_plate/files/mises_2d_plate.png" title="Von Mises stress contour showing stress concentration around the hole." class="img-fluid rounded article-figure" id="fig-mises" %}
<div class="caption">Von Mises stress contours highlighting the stress concentration at the hole.</div>

When the analysis finishes, open the **Visualization module** to check the results. [Figure 20](#fig-mises) shows the **von Mises stress contour** for the plate under tension and the stress concentration around the hole is clearly visible, as expected.

<div class="d-flex justify-content-between flex-wrap gap-2 tutorial-nav mt-4">
  <a class="btn btn-outline-primary" href="{{ '/courses/abaqus_plate_with_hole/' | relative_url }}">← Back to tutorial overview</a>
  <a class="btn btn-primary" href="{{ '/courses/abaqus_tutorial_part2/' | relative_url }}">Next: Part 2 →</a>
</div>
