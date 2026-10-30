# Portfolio content organization — initial proposal

Prepared 2026-10-02 from the current website and the supplied Teaching folders. This is a content proposal, not a website implementation or a technical validation of the projects.

Implementation scope clarified afterward: only the Teaching page may be redesigned. The wider portfolio ideas below are not an implementation instruction. Current layout proposals are described in `teaching-previews.md`.

## Recommendation

Use a curated overview, thematic project families, and individual case studies only where the material warrants them. Bundle the Do it Labs into one family with three named entries. Give the current tree-knot work its own case study, linked to both the tree lab and the plate-with-hole teaching series.

Organize by the questions the work addresses. Describe engineering, research, teaching, and personal exploration as roles or contexts within those themes. This lets one project show several parts of Vasco's work without appearing repeatedly as separate projects.

Working introduction, for later review:

> I work on how structures carry loads and how materials fail, combining engineering design, computational mechanics, research, and teaching.

This is a proposed positioning statement, not final biography copy.

## Proposed themes and initial mapping

| Theme | Organizing question | Material to place here | Presentation |
|---|---|---|---|
| Materials, damage, and failure | How do materials and joints carry loads and fail? | PhD composite-damage work and curved composite joints, as described in the existing site draft | Separate substantial case studies; connect to publications and related tools |
| Structures and engineering design | How do we turn requirements into a workable structure or mechanism? | ESA mission configuration work, composite UAV, Goblin engine CAD reconstruction, practical printed devices | A few selected stories, with smaller examples underneath |
| Mechanics in everyday life and nature | What can familiar objects and natural structures teach us about mechanics? | Do it Labs, plate-with-hole shape studies, tree-knot and simulated growth work | Named families with short examples and deeper studies |
| Computational tools and explanations | How can mechanics be analyzed, explored, and explained? | Stress tensor and failure-criteria visualizers, stress-trajectory workflow, useful analysis utilities | Tool summaries linked to runnable resources and the projects that use them |

These four themes are sections on one overview, not necessarily four new navigation items. Methods such as Abaqus, Python, MATLAB, CAD, and Blender belong within the project description; they do not need their own top-level categories.

The older career-project mapping comes from `_pages/engineering-projects.md`. That file contains placeholders, so dates, contributions, outcomes, and award claims need factual review before publication. The supplied Teaching folders were inspected directly. This is not an inventory of every historical project.

WheelRoute and Rufo can initially sit in a compact “Other explorations” list. Promote either to a main theme once its question, contribution, and evidence are clear. Small scripts belong with the work they support unless they are useful independent tools.

## Do it Labs: one family, three distinct questions

Suggested public title: **Do it Labs: mechanics in everyday life and nature**.

Suggested description:

> Student investigations that begin with a familiar question and develop it into a mechanics model, a comparison, and an engineering explanation.

Use one overview entry for the family. Inside it, introduce the following three projects. Keep student teams visible and state Vasco's confirmed teaching or supervision role separately from the team's work.

| Entry | Engineering question and theme | Existing material | How to frame it |
|---|---|---|---|
| When does a package fall? | Sliding, tipping, and recovery on an accelerating checkout conveyor; everyday dynamics | Introduction, poster, Python simulations, acceleration and rotation plots, existing animation | Explain how geometry, friction, and acceleration history enter the model. Describe measured acceleration inputs only where their provenance is established. |
| Why do chains sag? | Catenary geometry, fixed-length constraints, and long-term length change; cables and material behavior | Experimental proposal, later analytical/MATLAB presentation, catenary scripts | Separate the initial proposed observation from the later numerical scenario. The modeled 20-year sag is not evidence that the proposed eight-week experiment was completed. |
| How do tree forks carry loads? | Branch-junction shape, branch angle, and wood anisotropy; mechanics inspired by nature | Student report, FE model figures, stress comparisons, draft and meeting notes | Present a simplified comparative FE investigation. Preserve the report's boundary-condition and mesh limitations; do not describe it as a validated biological growth model. |

The three projects deserve individual names and summaries, but not three equally prominent cards on the main portfolio. A reader can understand the family first and then choose a question.

For future cohorts, group repeated investigations under the same question, with a compact team/year list. A new cohort warrants a new main entry when it introduces a substantially different question or result.

## Tree-knot work: a connected case study

Suggested title: **From a hole in a plate to grain and growth around a tree knot**.

Suggested short description:

> An exploratory mechanics study connecting stress concentrations, stress-following wood grain, and simulated local growth around holes and branch junctions.

The material in `Teaching/plate_with_hole/tree_knot` supports a story with four chapters:

1. **Start with a familiar mechanics problem.** A hole redirects stress; shape and corner radius affect the concentration. Link to the plate-with-hole tutorial and shape study.
2. **Let the material direction respond.** Compare straight grain with iterative stress-following fibre orientations (CAIO). Explain why reducing fibre shear does not guarantee the strongest final state.
3. **Let the local material amount respond.** Introduce shape/thickness updates (CAO), the branch and hole cases, and iteration-by-iteration growth plots. Growth can improve the model response but can also plateau or worsen it.
4. **Connect the model to a recognizable object.** Use existing or later wood/trunk stills to explain the simulated fields. Keep the analysis plot nearby so the render remains traceable to a model.

The individual geometries, 2D/3D comparisons, and iterations are sections of this story, rather than separate portfolio projects. The student tree-fork lab is a related investigation; its authorship and scope remain distinct from the later computational extension. Confirm that extension's contributor credits before publishing.

The folder already contains CAIO/CAO scripts, result tables, plots, Blender pipelines, and still-image outputs. This proposal does not require new rendering. The handoff indicates 2D growth remains the current focus and 3D growth is on hold; existing 3D grain work can appear as a supporting comparison.

Keep the claims narrow: typical material properties, simplified loads, and failure indices support an exploratory mechanics explanation. Iterations labeled “seasons” are simulation steps, not calibrated years of tree growth. Decorative rings and rendered depth or geometry must not be mistaken for measured biological quantities. The project's documented non-monotonic behavior is a useful finding, not something to hide from the case study.

## How much space each item gets

Use three levels of detail:

- **Selected story:** its own case study when there is a distinct question, a clear contribution, enough evidence to explain the answer, and useful limitations to discuss.
- **Family entry:** a named paragraph or small section when several projects share a teaching format or a coherent investigation. Do it Labs belong here; the larger tree extension can link out to a selected story.
- **Archive entry:** title, year, role, one-line description, and available source links for older or smaller work. Missing results can be marked explicitly; an archive entry does not require a finished narrative.

A sensible first overview has roughly six principal entries: composite damage research, composite joints, aerospace design, Do it Labs, the plate-to-tree mechanics study, and computational teaching tools. This is a starting selection, not a requirement to publish incomplete entries.

Promote a project because it has a strong story and evidence, not because it has the most attractive render. Combine closely related work when it shares a question and methods; preserve separate cases when combining them would obscure different contributions or conclusions.

## Relationship to the teaching page

The portfolio answers “What did you work on, and what did you contribute?” The teaching page answers “What can I learn from or use?”

Keep a single substantive account of each project and link to it from the appropriate places. For example, the portfolio's Do it Labs entry explains the teaching approach and project questions; teaching resources provide briefs or reusable exercises. The tree case study explains the computational investigation; the plate tutorial teaches the modeling workflow. A tool entry links directly to its interactive resource.

The existing teaching page already separates “Teaching tools” from “Courses & tutorials”. Do it Labs can become a third resource section when public-ready material exists. This does not require copying student reports wholesale onto the website.

## A small content record for each project

Keep these fields in the planning inventory before implementing any site structure:

- Public title and one-sentence question.
- Primary theme and parent family, if any.
- Context: research, engineering, teaching/supervision, or personal exploration.
- Vasco's specific contribution and collaborator/student credits.
- Dates and status: ongoing, completed, exploratory, or archived.
- Evidence: report, paper, model, code, experimental data, or result figure.
- Main takeaway and material limitations.
- Links to related projects and reusable teaching resources.
- Optional visual and what it represents.

One primary home per project avoids duplication. Cross-links preserve connections. Keep metadata small; the current material does not yet need a complicated filter system.

## Visualization ideas to retain for later

| Project | Useful visual question | Possible visual |
|---|---|---|
| Checkout stability | Why does this item slide, tip, or recover? | A shared conveyor scene with several geometries and a linked acceleration trace |
| Hanging chain | How does extra length change the sag at a fixed span? | Overlaid catenaries or a before/after still with identical endpoints |
| Tree-fork lab | What changes when the junction is rounded or its branch angle changes? | Side-by-side geometry and stress fields under a common comparison setup |
| Tree-knot extension | What changes when fibres rotate or material is added? | Straight/adapted grain pairs, growth-front plots, and selected trunk stills |
| Composite research | Where does damage begin and how does it evolve? | A laminate schematic plus selected simulation or experimental frames |

Blender is a way to present the project evidence. A separate visualization collection can emerge later if there is enough original visualization work with its own methods and story.

## Source inventory

- Site: `_pages/engineering-projects.md`, `_pages/about.md`, `_pages/teaching.md`, and `_courses/` resource metadata.
- Checkout: `Teaching/do_it_labs/Do_it_labs_cashout/Introduction.png`, `Poster.pdf`, and simulation scripts.
- Chain: `Teaching/do_it_labs/Do_it_labs_rope/doitlab1-2.pdf` (proposal, pp. 1–2); `do it lab-2.pdf` (later presentation, especially assumptions, application, and MATLAB sections).
- Student trees: `Teaching/do_it_labs/trees/Introduction.png`, `Final Report.pdf` (models pp. 2–5, results pp. 6–8, conclusions p. 9), and draft material.
- Computational extension: `Teaching/plate_with_hole/tree_knot/README.md`, `SESSION_HANDOFF.md`, `results/summary_all.csv`, and existing output-file inventory.
- Related teaching work: `Teaching/plate_with_hole/shape_study/README.md` and `stress_trajectories/README.md`.

Next content step: select the overview entries, confirm roles and credits, and write the short summaries. Layout and additional renders can follow once those stories are settled.
