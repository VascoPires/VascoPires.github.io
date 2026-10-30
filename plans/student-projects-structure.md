# Student projects within Teaching

Current direction, 2026-10-02: retain the existing Teaching style. The rejected Teaching-layout previews were removed. The broader portfolio proposal is historical context, not a current implementation instruction.

## Navigation

Teaching keeps its original tools and tutorials and adds one **Student projects** section using the same card renderer.

- **Do it Labs** → `/teaching/do-it-labs/`
  - Checkout stability → sliding/tipping and acceleration histories.
  - Hanging chains → catenary geometry and modeled length changes.
  - Tree mechanics → earlier student branch/junction shape analysis; knots, holes, and grain; ongoing simulated growth.
- **Student supervision** → `/teaching/student-supervision/`
  - Research-oriented student projects will be grouped by research topic when their actual details are supplied.

Trees are one Do it Labs theme. The growth and hole studies are not separate portfolio entries or a separate teaching category. Their student-investigation or computational-extension context is retained within the group.

## Content structure

`_data/do_it_labs.yml` stores `themes`, each with `id`, `title`, `question`, `summary`, `introduction`, and `studies`. Each study has a title, context, and description. Add later cohorts or related studies inside the relevant theme; add a new theme only for a substantially different question. Figures, reports, and contributor details can be added later.

`_data/student_supervision.yml` currently has an empty project list because no specific supervision inventory was supplied. Future entries use `theme`, `title`, `context`, `summary`, and optional `url`. A context can identify the degree level, year, contributors, and supervision role after confirmation. The destination page already groups entries by topic; there are no invented project titles.

The Do it Labs and supervision destination pages live in `_courses/` with `resource_section: student-projects`. This uses the existing Teaching metadata and renderer. Existing styles, visible/hidden course logic, global navigation, and other pages are preserved.

## Current scope

This pass establishes grouping, entry points, and page structure. It does not publish student reports or contact details, add new renders, verify student numerical conclusions, or establish biological validation of the tree models. The chain length-change work is described as a numerical scenario, and growth as simulated iterations.

Local review: `http://localhost:8098/teaching/`, `/teaching/do-it-labs/`, and `/teaching/student-supervision/`. Nothing is committed or deployed.

Validation: Jekyll build, theme navigation, resource links, and desktop/mobile layout checks passed. The tree family contains all three intended strands. The accessibility scan also reports contrast limitations inherited from the current dark theme's card text and links; this structure pass does not alter the global theme.

## Do it Labs visual direction

The destination page now follows three visual stories rather than a grid of theme cards. Existing Teaching typography, navigation, and colors provide the frame; all new layout styles are scoped to `.doit-flow`.

- Checkout stability pairs the student model with a controllable tipping video.
- Hanging chains pairs the question with the actual MATLAB catenary output.
- Tree mechanics connects the earlier junction-shape comparison to the ongoing grain, hole, and growth models. A keyboard-accessible slider explores saved cutaway renders at model steps 0, 5, 10, 20, and 40.

The content remains extensible by theme. Additional student outputs can sit within a story as figures or studies, without adding more overview cards. Research-oriented supervision retains its own destination. Image provenance and modeling limits are recorded in `assets/img/do-it-labs/SOURCES.md`; original Teaching source files are unchanged.

## Lunar landing and live mechanics

The fourth theme is lunar landing. It keeps the page’s question-led rhythm and adds a shared play/pause/scrub timeline comparing the existing spring-only and spring–dashpot response models. The student brief is linked; worked solution values are not displayed. Motion is initiated explicitly and pauses when the experiment leaves the viewport or the tab is hidden.

Checkout and chain figures now use native SVG mechanics diagrams with range inputs, while original student outputs remain in disclosures. `assets/js/do-it-models.mjs` holds the pure block-onset and catenary solvers; `scripts/generate_do_it_lab_models.py` exports normalized landing histories from the existing lab code and checks contact, settling, rebound, and energy consistency. Tree studies retain their authentic student contours and render timeline.

The current page replaces the lunar comparison with one damped lander and synchronized solved-response curves. Checkout now integrates constant-acceleration rigid-block tipping, or flat sliding, with play/pause, reset, and time scrubbing. The previous static threshold view remains the initial stability diagram; dynamic assumptions are explained below the figure.

The chain view now keeps initial length fixed at the supplied MATLAB scenario and animates years under sustained load, with play/pause, reset, and timeline scrubbing. A labeled magnification option makes the small modeled creep change visible without changing numeric readouts. Checkout adds an onset map and a response curve synchronized to its animation. Original-work disclosures, the student-report image, document downloads, and the long checkout caption are no longer shown.

Checkout now groups the conveyor animation and onset map directly together, with shared controls underneath. The time-response plot has been removed. Both remain linked to the same package proportions and acceleration; the map updates when those controls change.

Tree additions: a source-derived fiber viewer compares rounded/sharp knot holes
in straight, first-reoriented and final grain states. An adjacent first-failure
history shows why stress following is not a strength optimum. The growth viewer
also switches between trunk-hole and branch-junction render sequences.

Trunk cases are organized in one comparison: empty hole, branch inclusion,
branch inclusion with downward load. Shared controls select straight/adapted
trunk fibers and grain/failure-index views. Both branch cases share geometry
and material; the hole's different diameter is stated. Common crop and color
scale support inspection without treating the hole as a controlled geometric
comparison. Keep these grouped separately from growth iterations.

Seasonal growth revision: remove the standalone unloaded branch from the
comparison and the downward force arrow. Give failure maps a common knot
close-up and a labeled square-root color scale. Replace the render-only
growth timeline with a linked growth-front, wood-layer, seasonal-volume,
and failure-index explorer. Show all available hole seasons 0–40 and loaded
40-degree branch seasons 0–20; label the growth-iteration teaching analogy
and the source's profile-displacement conversion. Retain hole renders at
explicitly labeled saved steps only, with no unrelated branch render.

Compact growth viewer: remove the knot close-up control and wood-layer plot.
Keep the front, saved 3D cutaway, wood-per-season chart, and failure-index
chart beside the same season controls. Desktop uses front/model with two
stacked charts; narrow screens use a view selector with persistent controls.
The loaded branch has no cutaway render, so that view is disabled and returns
to the growth front if the model changes. The viewer has a direct tree-growth
anchor. Source model data and season ranges are unchanged.
