# Do it Labs visual sources

All images come from the local Teaching repository; no new solver runs or biological validation were performed.

- `hanging-chain-catenary.webp`: `do_it_labs/Do_it_labs_rope/do it lab-2.pdf`, page 18, MATLAB catenary plot. Extracted panel retains axes and legend. Sag differences amplified 500× in the source; time labels describe an assumed length-change scenario.
- `tree-junction-shape-stress.webp`: `do_it_labs/trees/Final Report.pdf`, page 6, Table 3. Abaqus S22 comparison with original shape labels and shared legend.
- `branch40_front_s40.webp`: `plate_with_hole/tree_knot/out/growth_years_dark/branch40_front_s40.png`.
- `hole_cut_s00/05/10/20/40.webp`: corresponding PNG files in `plate_with_hole/tree_knot/out/growth_years_dark/`. The numbers denote model iterations, not years. Full frame retained.
- `tipping-poster.webp`, `tipping.mp4`: `do_it_labs/Do_it_labs_cashout/Resources/tipping_animation_displayfix_20250609_231238.gif`. Original frames, video playback slowed 4× for readability; original parameter-box overlap is retained.

WebP files are resized/compressed display copies. Plots link to the larger display files for inspection. Original local source material stays unchanged.

## Live teaching models

- The block diagram uses a new quasi-static rigid-block model on a level accelerating belt. Incipient tipping occurs at `a = g / (height / width)`; incipient sliding at `a = mu * g`, with `mu = 0.6` chosen for this illustrative experiment. It predicts which instability starts first, not subsequent dynamic rotation/sliding. The original student animation is retained in a disclosure.
- The chain diagram solves `L = 2 a sinh(D / (2 a))` for equal-height supports, and draws the corresponding catenary with identical horizontal and vertical scales. It uses a uniform, inextensible chain, not the student elastic/creep model. The student plot remains available in a disclosure.
- The lunar animation and response plot export the existing `lunar_rover_landing_gear/optimized_landing_design.py` response functions with the comparison stiffness in `render_undamped_pretty.py` and the rounded damping ratio from `output/optimized_design_report.txt`. Regenerate with `PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/doit-mpl python scripts/generate_do_it_lab_models.py`. The spring-only model has unilateral contact and unlimited travel; it is an intentional failure case. The damped model is a spring–dashpot, not an irreversible crush cartridge. The page displays the damped lander only, with normalized height and separately normalized compression and force curves, without numerical response amplitudes or optimized design answers.
- `lunar-landing-challenge.pdf` is the existing `lunar_rover_landing_gear/documents/problem_setup_final_v3.pdf`, the student brief. Instructor worked solutions are not linked.

These are teaching models and solver-derived schematics; no new Abaqus simulation or biological/flight validation is claimed.

### Checkout dynamic playback

`packageMotion` in `assets/js/do-it-models.mjs` adds constant-acceleration motion. For tipping, a 0.5 m-wide block rotates about an ideal fixed lower corner using `I/m = (w² + h²)/3` and torque per mass `a*y_cm - g*x_cm`. RK4 integrates until first side contact at 90°; impact/bounce and changing pivot contact are not modeled. This uses mass inertia, rather than the area moment used in the original student script. Static friction selects the first onset; the subsequent tipping case assumes the pivot remains fixed, without a full friction/contact solve. Sliding is a separate flat-block model with static friction 0.6 and kinetic friction 0.5, ending after 1.5 m of relative displacement. Stable cases move with the belt.

The default 2:1 block at 5.5 m/s² tips before the static sliding threshold. Playback is slowed 3× and is opt-in. Browser integration was checked against an independent SciPy `solve_ivp` solution, endpoint contact, and halved time-step convergence. These checks verify the idealized equations, not experimental behavior.

The lunar page now shows only the damped rover with its solved compression and gear-force curves. Each curve uses its own normalized response scale; their magnitudes are not directly comparable. The plot cursor and rover use the same time index, with an exact touchdown sample to retain the dashpot force onset. Original spring-only comparison code remains in the teaching repository, but is no longer displayed on the page.

### Conveyor motion

The live checkout diagram now includes a roller bed and belt markings. Belt speed is `v=a*t` and travel is `s=0.5*a*t²`, starting at rest. Material markings follow the belt; roller axles belong to the fixed surroundings and their rotation follows belt travel divided by the drawn roller radius. The camera starts fixed, then tracks belt travel after 90 display pixels to keep the package visible. The package and tipping pivot travel with the belt; a sliding package additionally moves backwards relative to it. Camera displacement is applied to the roller bed positions, so a stable case continues to show moving surroundings and turning rollers while the camera follows the package. Speed and travel readouts use simulation time, with the existing slowed playback.

### Chain creep playback and checkout plots

The chain now uses the supplied MATLAB `doitlab1.m` and `length_constraint.m` assumptions: fixed 3 m support span, 4 m initial length, E=200 GPa, A=5×10⁻⁵ m², mass per length 1.1 kg/m, initial strain 5×10⁻⁴ and logarithmic time term 2×10⁻⁴ ln(1+t/1 year). `chainCreep` re-solves the coupled elastic-length/catenary constraint at each time. Its support tension is `w*a*cosh(D/(2a))`; the original MATLAB comment mislabels this as tension at the lowest point. Assumed coefficients are not experimentally calibrated. Initial shape is dashed; the 500× option amplifies only the subsequent creep change, while readouts remain actual values. A reduced vertical display scale keeps that exaggerated change inside the view. Unmagnified geometry uses equal horizontal/vertical scales.

The student presentation separately reports 40→43.2 cm sag over 20 years using different creep coefficients and time units. Its stated initial length (3.212 m) is inconsistent with a 3 m span/0.4 m sag (catenary length ≈3.1378 m). The interactive model follows the reproducible MATLAB code, rather than treating that table as a validated prediction.

The checkout onset map uses `a_tip=g/(h/w)` and `a_slide=0.6*g` to identify the first instability. The onset map sits beside the conveyor animation and shares its geometry/acceleration controls. The separate time-response plot has been removed. Original student-output disclosures, report screenshots, and document downloads are removed from the page; source provenance stays in this internal file.

## Interactive fiber comparison and branch growth

`assets/data/do-it-grain.json` is exported by `scripts/generate_do_it_tree.py`
from `tree_knot/results/{circle,diamond_r1}_itNN.npz` and their history JSON.
States shown: straight grain, first reorientation, and final saved iteration.
Paths use the original `plot_tree.grain_lines` orientation-tensor tracer, with
0.7 mm seeding, central 54 mm cropping and every third traced point retained.
The field represents unoriented fiber axes, not directional vectors. Meshes
come from `shape_study/models/shape_circle.inp` and `diamond_r1p00.inp`.
The graph uses saved predicted first-failure loads at every iteration; those
are Tsai-Hill predictions with assumed spruce properties under one tensile
load case, not measured failure loads. CAIO does not optimize strength.

Branch growth frames 5, 10, 20, 40 are converted from
`tree_knot/out/growth_years_dark/branch40_front_sNN.png`. There is no saved
branch frame 0 in that render sequence. Growth controls use actual available
steps, and these are model iterations, not calendar years.

## Hole, branch, and branch-weight comparison

`assets/data/do-it-trunk.json` is generated by
`scripts/generate_do_it_trunk.py` from `tree_knot/results/trunk_*_itNN.npz`
and matching histories, using meshes in `tree_knot/models_trunk2d`.
The displayed cases are `trunk_hole` and `trunk_branch_weight`.
Initial and final saved fiber states are displayed. Source `plot_trunk2d.grain`
traces the wood-only orientation-tensor field with mirrored line pairs.
The view shows a common 300 mm circumferential by 400 mm axial window;
the source surface is unrolled, not a 3D branch bending simulation.
Tsai-Hill maps use the maximum integration-point index per wood element,
on the same display scale 0–1 for every case. Higher values saturate the
map while peak readouts preserve the actual maximum over all trunk wood.
The branch inclusion is excluded from the wood failure index. The focused
export omits the unused unloaded-branch case.

The hole diameter is 60 mm; the branch diameter is 100 mm. This comparison
changes both geometry and loading. In
`build_trunk2d.py`, the 1 mm plane-stress model uses 10 MPa axial tension;
branch weight is a uniform downward body force whose resultant is
`SIGMA_NOM * D * thickness = 1000 N`. It is an assumed load, not a mass
inferred from branch geometry. The inclusion uses fixed end-grain material;
only trunk wood is reoriented by CAIO. The UI compares actual failure indices
and transverse tensile stress instead of implying a separately varied axial
failure load for the combined-load case.

## Seasonal growth explorer

The UI now focuses the nongrowing trunk comparison on the hole and loaded
branch. Force arrows pointing downward and the standalone unloaded-branch
view were removed. The failure map offers a common close-up and full window,
with a square-root color scale (ticks 0, 0.25, 1) to expose small index values.
The underlying indices remain unchanged; saturation above 1 is labeled.

`assets/data/do-it-growth.json` comes from `scripts/generate_do_it_growth.py`,
using `results_tcao/trunk_hole_it00..40.npz` and
`results_tcao/trunk_branch40_weight_it00..20.npz` plus matching histories.
No later weighted-branch snapshots are present, so its timeline stops at 20.
Growth-front contours are the source plot's `t = 1.2` threshold on the masked
centroid triangulation, not a moving biological boundary. Fronts can have
several disconnected pieces. Earlier contours are drawn faintly.

The vertical layers reproduce the source sampling: nearest centroid,
0.5 mm samples, 3 mm Gaussian smoothing, nonnegative monotonic accumulation,
then display samples at 2 mm. Profiles use 5 mm outward displacement per
extra thickness unit, matching `plot_growth_years.py`. This conversion is for
visualization and differs from the original 1 mm-thick plane-stress model.
Per-season and accumulated model wood volumes are calculated from thickness
and element area and checked against `wood_added_mm3` histories. The paired
failure-index plot uses saved peak Tsai-Hill indices, not predicted calendar
aging. One model iteration is called a season as a teaching picture, not a
calibrated year. The hole 3D cutaway uses available saved frames at steps
0, 5, 10, 20, 40; its displayed saved step is explicitly labeled while the
front, layers, and plots advance at every saved iteration. There is no saved
weighted-branch render; that case uses its actual computed layer profiles.

## Compact viewer revision

The close-up transform/control and wood-layer plot are removed. The trunk
maps use their full shared window. Seasonal plots and the saved hole cutaway
now share one compact viewer; narrow screens select a panel while retaining
the same season controls. The loaded branch has no saved cutaway render, so
its 3D view is disabled. The profile data remain in the export for provenance
but are not drawn in the page. Fronts, volume, failure index, and season
ranges keep the same saved data and interpretation.

### Transparent tree renders

The website's five `hole_cut_s00/05/10/20/40.webp` frames and
`branch40_front_s40.webp` are now re-rendered from `tree_knot/render_trunk2d.py`
into `out/growth_years_transparent/`, with the same geometry, camera, materials,
dark-theme lighting and 256 Cycles samples. Render size is 1440 × 810. Blender's
transparent film and RGBA PNG output provide real alpha; WebP exports preserve
it losslessly. Original opaque source renders remain available.

Regenerate/export with `python scripts/render_do_it_tree_assets.py` (requires
Blender and Pillow). `BLENDER_BIN` overrides the executable. Cached transparent
PNGs are reused; remove those files to force re-rendering. This is a rendering
change only; no solver results changed.

### Loaded 40° branch cutaways

`branch40_weight_cut_s00/05/10/20.webp` use the actual saved
`trunk_branch40_weight` snapshots, through iteration 20, with their matching
wood textures and section-growth bands. These are additional transparent Blender
renders, not substitutes from the unloaded branch. The shared season viewer now
shows both cases with matching cutaways. Saved render states are 0, 5, 10, 20;
between them the cutaway holds the preceding saved state while plots follow each
available model iteration.

The branch sequence uses 1440 × 810 RGBA renders with 128 Cycles samples and denoising.
The horizontal section closes the sliced branch with a solid end-grain surface.
The branch cross-section uses the renderer's 40° illustrative branch geometry;
its old-wood ring pattern is decorative, as on the trunk. The added-growth bands
and outer trunk growth come from saved thickness fields. No new solver run or
physical branch-growth validation is implied. Regenerate with
`BLENDER_DEVICE=CUDA python scripts/render_do_it_tree_assets.py`, or omit the
environment variable for CPU rendering. Originals remain intact.

#### Joined horizontal branch sections

Both branch and trunk wood sections are now exactly at `z = 0`; the earlier
0.5 mm branch offset is removed. The branch surface is flat shaded and faces up.
The trunk section is triangulated with the actual cut branch boundary as a
constraint, then trimmed outside that boundary. This removes the covered trunk
faces rather than overlaying two wood surfaces. All four branch frames are
re-rendered with this geometry. Previous offset PNGs are kept in
`out/growth_years_transparent/offset_sections_backup/`. Hole frames are unchanged.
