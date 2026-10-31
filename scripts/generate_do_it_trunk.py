"""Export the 2D unrolled-trunk CAIO data for the Do it Labs viewer.

Run from the website checkout with the sibling Teaching repository available:
    python scripts/generate_do_it_trunk.py

Grain paths are produced by the source project's plot_trunk2d.grain function.
No Abaqus jobs are started by this exporter.
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "Teaching" / "plate_with_hole" / "tree_knot"
OUTPUT = ROOT / "assets" / "data" / "do-it-trunk.json"
X_MIN, X_MAX = -200.0, 200.0       # axial distance along the trunk [mm]
Y_MIN, Y_MAX = -150.0, 150.0       # distance round the trunk [mm]
CASES = (
    ("trunk_hole", 60.0),
    ("trunk_branch_weight", 100.0),
)

sys.path.insert(0, str(SOURCE))
original_argv = sys.argv
sys.argv = [str(__file__), "light"]
try:
    import plot_trunk2d as trunk_plot
    from caio import read_elset, read_mesh
    from plot_tree import element_th, flat_mesh
finally:
    sys.argv = original_argv


def clip_segment(p0, p1):
    """Liang-Barsky clip of one source segment to the shared plot window."""
    x0, y0 = p0
    dx, dy = p1[0] - x0, p1[1] - y0
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x0 - X_MIN), (dx, X_MAX - x0),
                 (-dy, y0 - Y_MIN), (dy, Y_MAX - y0)):
        if abs(p) < 1e-12:
            if q < 0.0:
                return None
            continue
        r = q / p
        if p < 0.0:
            if r > t1:
                return None
            t0 = max(t0, r)
        else:
            if r < t0:
                return None
            t1 = min(t1, r)
    if t1 - t0 < 1e-12:
        return None
    return (np.array([x0 + t0 * dx, y0 + t0 * dy]),
            np.array([x0 + t1 * dx, y0 + t1 * dy]))


def clip_polyline(points):
    """Clip a polyline and preserve disconnected in-window runs."""
    points = np.asarray(points, dtype=float)
    pieces = []
    current = []
    for p0, p1 in zip(points[:-1], points[1:]):
        clipped = clip_segment(p0, p1)
        if clipped is None:
            if len(current) >= 2:
                pieces.append(np.asarray(current))
            current = []
            continue
        start, end = clipped
        if current and np.linalg.norm(current[-1] - start) <= 1e-7:
            if np.linalg.norm(current[-1] - end) > 1e-9:
                current.append(end)
        else:
            if len(current) >= 2:
                pieces.append(np.asarray(current))
            current = [start, end]
    if len(current) >= 2:
        pieces.append(np.asarray(current))
    return pieces


def decimate(points):
    """Keep every third point while retaining the clipped endpoint."""
    points = np.asarray(points, dtype=float)
    keep = points[::3]
    if np.linalg.norm(keep[-1] - points[-1]) > 1e-9:
        keep = np.vstack((keep, points[-1]))
    return np.round(keep, 3).tolist()


def triangle_intersects_window(triangle):
    x = triangle[:, 0]
    y = triangle[:, 1]
    return not (x.max() < X_MIN or x.min() > X_MAX or
                y.max() < Y_MIN or y.min() > Y_MAX)


def export_case(case, diameter):
    model_path = SOURCE / "models_trunk2d" / f"{case}.inp"
    model_text = model_path.read_text()
    nodes, elements = read_mesh(model_text)
    elements = sorted(elements)
    labels = np.asarray([element[0] for element in elements])
    wood_labels = read_elset(model_text, "plate_domain")
    keep = np.isin(labels, wood_labels)

    history = json.loads((SOURCE / "results" / f"{case}_history.json").read_text())
    history_by_iteration = {row["iteration"]: row for row in history["history"]}
    iterations = (min(history_by_iteration), max(history_by_iteration))
    snapshots = {}
    for iteration in iterations:
        path = SOURCE / "results" / f"{case}_it{iteration:02d}.npz"
        with np.load(path, allow_pickle=False) as data:
            snapshots[iteration] = {key: data[key] for key in data.files}

    mesh, triangle_owner = flat_mesh(nodes, elements)
    xy = np.column_stack((mesh.x, mesh.y))
    triangle_points = xy[mesh.triangles]
    exported_triangles = []
    exported_owners = []
    for triangle, owner in zip(triangle_points, triangle_owner):
        if keep[owner] and triangle_intersects_window(triangle):
            exported_triangles.append(np.round(triangle, 3).tolist())
            exported_owners.append(int(owner))

    # This is the exact wood-only mesh boundary used by plot_trunk2d.grain;
    # it includes the branch-core boundary as well as the outer wood edge.
    final_snapshot = snapshots[iterations[-1]]
    model = SimpleNamespace(nodes=nodes, elements=elements)
    final_lines, domain = trunk_plot.grain(model, final_snapshot["theta"], keep, diameter)
    outline = []
    for edge in domain.xy[domain.edges]:
        clipped = clip_segment(edge[0], edge[1])
        if clipped is not None:
            outline.append(np.round(np.stack(clipped), 3).tolist())

    states = []
    for iteration in iterations:
        snapshot = snapshots[iteration]
        # Reuse the final-state trace and domain computed above for the outline.
        paths = final_lines if iteration == iterations[-1] else trunk_plot.grain(
            model, snapshot["theta"], keep, diameter
        )[0]
        lines = []
        for path in paths:
            lines.extend(decimate(piece) for piece in clip_polyline(path))

        per_element_index = element_th(snapshot, len(labels))
        index = [round(float(per_element_index[owner]), 6) for owner in exported_owners]
        metrics = history_by_iteration[iteration]
        states.append({
            "step": int(iteration),
            "lines": lines,
            "index": index,
            "metrics": {
                "tsai_hill_max": float(metrics["tsai_hill_max"]),
                "sig_R_max": float(metrics["sig_R_max"]),
                "tau_LR_max": float(metrics["tau_LR_max"]),
                "iteration": int(metrics["iteration"]),
            },
        })

    case_notes = {
        "trunk_hole": "Woodpecker hole, D = 60 mm. The hole is smaller than the branch inclusions, so this is not a diameter-matched comparison.",
        "trunk_branch": "D = 100 mm branch inclusion without the added downward branch body force.",
        "trunk_branch_weight": "Same D = 100 mm branch inclusion as trunk_branch, with the source model's downward 1 kN equivalent body-force resultant; this is a prescribed load, not a measured branch mass.",
    }
    return {
        "diameter_mm": diameter,
        "note": case_notes[case],
        "triangles": exported_triangles,
        "outline": outline,
        "states": states,
    }


def main():
    if not SOURCE.is_dir():
        raise FileNotFoundError(f"Sibling Teaching source not found: {SOURCE}")
    export = {
        "units": "mm",
        "coordinates": {
            "x": "axial distance along the unrolled trunk",
            "y": "distance round the trunk circumference",
        },
        "window": {"x": [X_MIN, X_MAX], "y": [Y_MIN, Y_MAX]},
        "index_note": "Each state index is the raw maximum Tsai-Hill integration-point value for its source element, repeated for each intersecting wood triangle. The viewer may clamp color at 1; values are not capped here.",
        "grain_note": "Fiber axes and outlines are clipped to the shared window. Grain lines use plot_trunk2d.grain and keep every third point plus each clipped endpoint. Triangles are retained when their source triangle intersects the window; clip them in the viewer.",
        "comparison_note": "trunk_hole has D = 60 mm and trunk_branch_weight has D = 100 mm; geometry and load differ. The branch-weight case uses a prescribed equivalent load, not an inferred or measured branch mass.",
        "cases": {},
    }
    for case, diameter in CASES:
        exported = export_case(case, diameter)
        for state in exported["states"]:
            if len(state["index"]) != len(exported["triangles"]):
                raise ValueError(f"{case} index/triangle alignment failed at iteration {state['step']}")
        export["cases"][case] = exported
        print(case, "triangles", len(exported["triangles"]),
              "outline segments", len(exported["outline"]),
              "state lines", [len(state["lines"]) for state in exported["states"]], flush=True)

    serialized = json.dumps(export, separators=(",", ":"), allow_nan=False)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(serialized)
    print(f"Wrote {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
