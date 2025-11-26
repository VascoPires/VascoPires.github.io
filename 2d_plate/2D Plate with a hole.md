---
date: "202510031420"
tags:
  - "#Article"
cssclasses:
  - academia
keywords:
---
# 2D Plate with a Hole

Now that we have covered some fundamentals and learned how to operate within Abaqus/CAE, let's start with a simple example: a plate with a hole, as shown in Figure [[#fig:plate_with_hole]].

```tikz
\begin{document}
    \begin{tikzpicture}[scale=1.0]
      % Plate
      \draw[fill=black!10] (0,0) rectangle (8,4);
    
      % Hole in the center
      \draw[fill=white] (4,2) circle (0.8);
    
      % Symmetry lines (dashed)
      \draw[dashed,thick] (4,0) -- (4,4);
      \draw[dashed,thick] (0,2) -- (8,2);
    
      % Displacement arrows on the right edge
      \foreach \y in {0.5,1.5,2.5,3.5}
        \draw[->,thick,red] (8,\y) -- +(1,0);
      \node[right,red] at (9,2) {$u_x$};
    
      % Displacement arrows on the left edge
      \foreach \y in {0.5,1.5,2.5,3.5}
        \draw[->,thick,red] (0,\y) -- +(-1,0);
      \node[left,red] at (-1,2) {$u_x$};
    
      % Dimensions
      \draw[<->] (0,-0.6) -- (8,-0.6) node[midway,below] {$L$};
      \draw[<->] (-1.8,0) -- (-1.8,4) node[midway,left] {$H$};
        \begin{scope}[shift={(4,2)},rotate=30]
            \draw[<->] (-0.8,0) -- (0.8,0) 
            node[midway,below,xshift=6pt] {$D$}; 
        \end{scope}
    
      % Reference system
      \begin{scope}[shift={(-3,-2)}]
        \draw[->,thick] (0,0) -- (1.2,0) node[right] {$x$};
        \draw[->,thick] (0,0) -- (0,1.2) node[above] {$y$};
        \fill (0,0) circle (2pt) node[below left] {$O$};
      \end{scope}
    
    \end{tikzpicture}
\end{document}
```

**Figure 1:** *Sketch of the 2D plate with a central hole.*  


| ⚙️ Parameter       | 📏 Value |
| ------------------ | -------- |
| Plate length, $L$  | 100 mm   |
| Plate height, $H$  | 20 mm    |
| Hole diameter, $D$ | 10 mm    |

**Table 1:** *Geometric dimensions of the 2D plate with a hole.*  


---

## 🗂️ Setting up the Project

The first step is to set up the working directory. After opening Abaqus, either manually select the working directory from the top of the GUI or open the command prompt in the desired folder and type:

```cmd
abaqus cae
```

After that, in the **Start Session** dialog, choose `Standard/Explicit Model` to begin.  
Figure [[#fig:welcome_window]] shows the initial window of Abaqus/CAE.

![[Files/welcome_window.png|Start-up dialog in Abaqus/CAE 2023.]]  


---

## 🧩Geometry


The first step of any model is defining the geometry.  
In the **Part** module, select:
$$
\text{Create Part} \; \rightarrow \; \text{2D Planar} \; \rightarrow \; \text{Deformable} \; \rightarrow \; \text{Shell}.
$$

This means we are creating a 2D deformable part using the *Shell* option, which defines an area.  If we had chosen *Wire* instead, we would have created a 1D part (for example, a truss). 

> [!warning] Shell definition
> A common confusion point is between 3D shell and 2D Planar shell option. In terms of modelling a "Part" they are mostly equivalent, however they are fundamentally different. One, is a shell/plate in a 3D space, so the 3D behavior is included, which means using shell section and elements while on the other hand, in 2D planar, we are using solid sections and elements.

![[Files/part_module.png|Abaqus part module.]]  


First, select the 🟦 rectangle tool (*Create Lines: Rectangle (4 Lines)*) and draw it roughly at the center.  Next, add horizontal and vertical construction lines ➕ through the midpoint of the sketch. These construction lines serve as auxiliary references and do not form part of the geometry.  

At this point, your sketch should look similar to Figure [[#fig:sketch_2d]].  
Now, add a circular hole at the center by selecting the circle tool and clicking in the middle of the plate.  Ensure the sketch forms a closed contour - Abaqus requires closed profiles for part creation. Open profiles will cause an error.

![[Files/sketch_2d.png|Initial 2D sketch of the plate.]]  

Next, apply the dimensions according to Table [[#tab:plate_dimensions]].  
Use the dimension tool (*second column, fourth row*) from the sketch toolbar.

![[Files/sketch_dim.png|Sketch of the plate with the dimensional constraints applied.]]  


Finally, center the sketch at the origin.  Create a point at $(0,0)$, apply the **Fixed** constraint to it, and then use the **Coincident** constraint to align the circle center with this point.  

When a sketch is *fully defined*, all lines appear green (see Figure [[#fig:sketch_fully_defined]]).  If it becomes *overdefined* ⚠️ (e.g., due to conflicting constraints), the lines turn yellow and the conflicting constraints appear in purple.

![[Files/sketch_fully_defined.png|Fully defined sketch of the plate with a hole.]]  


Press **Done** ✔️ at the bottom of the sketch window to create the part.  
At this point, you have your part created inside the Part module, as shown in Figure [[#fig:plate_part]].   With this, the geometry section of the model is complete.

![[Files/plate_part.png|Final part geometry of the plate with a hole.]]  

## 🧪Material/Section Property 


In Abaqus, material properties are defined within the *Property* module 🧱.  So let's create a PMA material with the following elastic properties (isotropic): $E=3 \; \text{GPa}$  ; $\nu = 0.4$. For this we are going to create a material and then select:

$$
\text{Mechanical} \; \rightarrow \; \text{Elasticity} \; \rightarrow \; \text{Elastic}
$$

as shown in Figure [[Files/material_property.png]]. Then, select "Isotropic" (as shown in [[Files/material_prop2.png]]) as the type and insert the young's modulus and the poison coefficient. Pay attention to the **units** ⚠️! Since we are working in **millimeters (mm)** and **newtons (N)**, our elastic properties must be in **megapascals (MPa)** to maintain dimensional consistency 📏.

![[Files/material_property.png]]

![[Files/material_prop2.png]]

The second step is defining a **section**.  
A section is, in essence, the _middle layer_ between the material definition and the geometry. While the **material** defines _how_ a material behaves, the **section** specifies _how_ that material will be represented or simplified in your model. For instance, with the same material, you could create a **solid**, **shell**, or **beam** section - each producing different structural behaviors depending on the modeling assumptions. So even if this feels a bit abstract now, it’s enough to remember that the _section_ combines both the material and the modeling approach. Every element in your model must be assigned a section, and this step ensures that Abaqus knows how to interpret the material response of your geometry.

![[Files/section.png]]
![[Files/section_assign.png]]

## 🧩 Assembly and Mesh

Moving on to the **assembly** and **mesh** steps.  The assembly module represents what the **solver actually sees** . You might create several parts in the Part module, but only those you instantiate in the assembly will be used for simulation. Even if you have just one part, you still need to create an assembly instance of it.  you’re essentially telling the solver: “here’s the part I want to analyze.

To do this, create an **Instance**.  An instance is a placed copy of a part within the assembly. You can have multiple instances of the same part, for example, a connection with 10 identical bolts can be modeled using one bolt geometry and section, but repeated as multiple instances.

![[Files/assembly.png|Creation of an instance in the model's assembly.]]

When creating an instance, Abaqus will ask whether it should be **dependent** or **independent**.  A **dependent instance** means the mesh is created at the _part level_, while an **independent instance** allows meshing at the _assembly level_.

The distinction mainly affects how nodes and elements are numbered:

- In an **independent instance**, all nodes and elements share a _global numbering system_ across the entire assembly (no duplicates).

- In a **dependent instance**, each part maintains its own numbering (so, for example, Element ID = 1 could exist in multiple parts).

The conceptual difference is shown in Figure [[../../Excalidraw/2D Plate with a hole 2025-10-07 15.39.12.excalidraw]].

![[../../Excalidraw/2D Plate with a hole 2025-10-07 15.39.12.excalidraw|Difference between dependent and independent instances in Abaqus.]]

For this example, we’ll keep things simple and use a **dependent instance** .  Once the instance is created, we can leave the Assembly module and move to the **Mesh** module.

## 🕸️ Mesh

Now, onto the **meshing** step.  
Meshing is one of the most important parts of any finite element analysis, but here we’ll focus on the basics just to get our model running.

Start by defining a **global seed size** of approximately _1.5_.   Then, click on the **mesh icon** (second row, first position) to generate the mesh for your part.  The expected result is shown in Figure [[Files/mesh.png]].

![[Files/mesh.png|Mesh of the plate with a 2D hole.]]

At this stage, you can perform several operations, such as assigning **element types**, changing the **meshing scheme**, or adjusting **seed sizes**. However, since this is just an introductory example, we’ll leave those for later sections.

## 🧷 Boundary Conditions

The final step before running the simulation is to apply the **boundary conditions**.  
Before doing so, take a look at the initial sketch and think about which boundary conditions make physical sense here.

But first, let’s create a **step**  -  this defines the simulation’s time frame.  In Abaqus, analyses can generally be **static** or **dynamic**.

- In a _dynamic (explicit or implicit)_ simulation, the time variable represents _real physical time_.
    
- In a _static_ analysis, time is _not physical_ but simply a _loading parameter_, indicating how loads are gradually applied.
    

For this example, we’ll perform a **static analysis** — the simplest type.

Create a new step by navigating to:  

$$
\text{Step} \; \rightarrow \; \text{Procedure type: General} \; \rightarrow \; \text{Static, General}
$$

and name it `loading_step`, as shown in Figure [[Files/step.png]].

![[Files/step.png|Step creation.]]

Now, we can define the **boundary conditions**.  
According to the sketch, we want to apply a **displacement** on both sides of the plate.  
Click the boundary condition icon (second row, first column) and select:

$$
\text{Mechanical} \; \rightarrow \; \text{Displacement/Rotation} \; \rightarrow \; \text{U1:} \; \pm 1.5 \; \rightarrow \; \text{Amplitude: Ramp}
$$


This applies a displacement of $u_x = 1.5$ mm on both sides.  

> [!warning] Displacement Direction
> By default, **U1** corresponds to the *x-axis direction* in the assembly.  
> On the **left side**, apply a **negative displacement** (−1.5 mm), and on the **right side**, apply a **positive displacement** (+1.5 mm) to simulate **tension**.


![[Files/bc_config.png]]

![[Files/disp_BC.png]]

---

## 🚀 Job Submission and Output

Now that the model is ready, let’s create and submit a **job**.  
The job module is where we tell Abaqus to actually run the simulation we’ve set up.

1. Go to the **Job** module and create a new job:
2. Assign a name to the job (e.g., `plate_with_hole`) and verify that it references your current model.
3. In the job settings, you can see basic options such as analysis type, description, and memory allocation.


![[Files/job_creation.png|Job creation window.]]  

Once everything is ready, click **Submit** ▶️ to start the analysis. You can monitor its progress in the **Job Monitor**, which displays information such as completion status, warnings, and estimated time.

![[Files/submit_job.png|Job submission.]]

When the analysis finishes, open the **Visualization module** to check the results.  
Figure [[Files/mises_2d_plate.png]] shows the **von Mises stress contour** for the plate under tension and the stress concentration around the hole is clearly visible, as expected.

![[Files/mises_2d_plate.png|Stress contour of the plate with a hole.]]

