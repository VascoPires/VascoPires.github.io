"""Export source CAO growth fronts and vertical growth profiles for the viewer.

Run from the website checkout with the sibling Teaching repository available.
This reads saved CAO snapshots only; it does not run a solver or render figures.
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib.path import Path as PolygonPath
import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy.spatial import cKDTree


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "Teaching" / "plate_with_hole" / "tree_knot"
OUTPUT = ROOT / "assets" / "data" / "do-it-growth.json"
CASES = ("trunk_hole", "trunk_branch40_weight")
X_GRID = np.arange(-220.0, 220.0 + 1e-9, 2.0)
CONTOUR_LEVEL = 1.2
BULGE_MM = 5.0
SMOOTH_MM = 3.0


def load_case(case):
    results = SOURCE / "results_tcao"
    history_doc = json.loads((results / f"{case}_history.json").read_text())
    history = {int(row["iteration"]): row for row in history_doc["history"]}
    files = sorted(results.glob(f"{case}_it*.npz"))
    snapshots = {}
    for path in files:
        step = int(path.stem.rsplit("_it", 1)[1])
        with np.load(path, allow_pickle=False) as archive:
            snapshots[step] = {key: archive[key] for key in archive.files}
    steps = sorted(snapshots)
    if steps != sorted(history):
        raise ValueError(f"{case}: saved snapshots and history iterations differ")
    return steps, snapshots, history


def footprint(case):
    path = SOURCE / "models_trunk2d" / f"footprint_{case}.json"
    if path.exists():
        points = np.asarray(json.loads(path.read_text())["points"], dtype=float)
        note = "Source footprint polygon from models_trunk2d."
    else:
        # plot_growth_years.py uses this same radius fallback when a footprint
        # file is absent (the woodpecker hole has radius 30 mm).
        angle = np.linspace(0.0, 2.0 * np.pi, 240, endpoint=False)
        points = np.column_stack((30.0 * np.cos(angle), 30.0 * np.sin(angle)))
        note = "No source footprint JSON exists; follows plot_growth_years.py's 30 mm circular hole-mask fallback."
    return points, PolygonPath(points), note


def extra_growth(tree, ts, x, y, mask_path):
    """Source-equivalent nearest-centroid growth, smoothed and accumulated."""
    _, nearest = tree.query(np.column_stack((x, y)))
    growth = (ts[:, nearest] - 1.0) * BULGE_MM
    axis = x if np.ptp(x) > 0 else y
    spacing = float(np.median(np.diff(axis))) if len(axis) > 1 else 0.5
    sigma = SMOOTH_MM / spacing
    growth = gaussian_filter1d(growth, sigma, axis=1, mode="nearest")
    growth = np.maximum.accumulate(np.maximum(growth, 0.0), axis=0)
    inside = mask_path.contains_points(np.column_stack((x, y)))
    growth[:, inside] = np.nan
    return growth


def export_case(case):
    steps, snapshots, history = load_case(case)
    first = snapshots[steps[0]]
    centroids = np.asarray(first["centroid"], dtype=float)
    area = np.asarray(first["area"], dtype=float)
    tree = cKDTree(centroids)
    ts = np.stack([np.asarray(snapshots[step]["t"], dtype=float) for step in steps])
    if ts.shape[1] != len(centroids) or any(len(snapshots[step]["area"]) != len(area) for step in steps):
        raise ValueError(f"{case}: saved snapshot element arrays are not aligned")

    boundary, mask_path, footprint_note = footprint(case)

    # Source growth-front triangulation: circumferential coordinate is horizontal,
    # axial coordinate vertical; omit knot-crossing and long circumferential edges.
    in_window = (np.abs(centroids[:, 0]) < 220.0) & (np.abs(centroids[:, 1]) < 160.0)
    window_points = centroids[in_window]
    tri = mtri.Triangulation(window_points[:, 1], window_points[:, 0])
    tri_points = window_points[tri.triangles]
    circum_span = np.ptp(tri_points[:, :, 1], axis=1)
    tri_x = tri_points[:, :, 0].mean(axis=1)
    tri_y = tri_points[:, :, 1].mean(axis=1)
    tri_mask = mask_path.contains_points(np.column_stack((tri_x, tri_y))) | (circum_span > 25.0)
    tri.set_mask(tri_mask)

    # Match the source's vertical-cut location: centerline at x=0, and the
    # mean circumferential location where final smoothed growth reaches 90% peak.
    lip_y = np.arange(0.0, 150.0, 0.5)
    lip_t = extra_growth(tree, ts[-1:], np.zeros_like(lip_y), lip_y, mask_path)[0]
    finite_lip = np.isfinite(lip_t)
    if not finite_lip.any() or np.nanmax(lip_t) <= 0:
        y_lip = float(np.nanmean(lip_y[finite_lip])) if finite_lip.any() else 0.0
    else:
        thick = finite_lip & (lip_t >= 0.9 * np.nanmax(lip_t))
        y_lip = float(np.mean(lip_y[thick]))
    # Match the source's 0.5 mm sample spacing for its 3 mm Gaussian filter,
    # then decimate every fourth sample to the viewer's 2 mm grid.
    fine_x = np.arange(-220.0, 220.0 + 1e-9, 0.5)
    fine_profile = extra_growth(tree, ts, fine_x, np.full_like(fine_x, y_lip), mask_path)
    profile = fine_profile[:, ::4]
    if profile.shape[1] != len(X_GRID):
        raise ValueError(f"{case}: decimated profile does not align with x grid")

    fig, ax = plt.subplots()
    states = []
    cumulative_mm3 = []
    for state_index, step in enumerate(steps):
        contour = ax.tricontour(tri, ts[state_index, in_window], levels=[CONTOUR_LEVEL])
        fronts = []
        for vertices in contour.allsegs[0]:
            if len(vertices) < 2:
                continue
            # Triangulation is (circumferential, axial); public format is
            # (axial, circumferential), matching the footprint coordinates.
            fronts.append(np.round(vertices[:, [1, 0]], 3).tolist())
        ax.clear()

        row = history[step]
        summed_mm3 = float(np.sum((ts[state_index] - 1.0) * area))
        added_mm3 = float(row["wood_added_mm3"])
        if not np.isclose(added_mm3, summed_mm3, rtol=1e-9, atol=1e-6):
            raise ValueError(f"{case} step {step}: history wood total disagrees with thickness field")
        cumulative_mm3.append(added_mm3)
        state = {
            "step": int(step),
            "fronts": fronts,
            "profile": [None if not np.isfinite(value) else round(float(value), 4)
                        for value in profile[state_index]],
            "added_cm3": round(added_mm3 / 1000.0, 6),
            "per_season_cm3": 0.0,
            "added_mm3": round(added_mm3, 6),
            "failure_index": float(row["tsai_hill_max"]),
            "failure_load": float(row["failure_load"]),
        }
        if state_index:
            state["per_season_cm3"] = round((added_mm3 - cumulative_mm3[-2]) / 1000.0, 6)
        states.append(state)
    plt.close(fig)

    return {
        "footprint": np.round(boundary, 3).tolist(),
        "footprint_note": footprint_note,
        "x": X_GRID.tolist(),
        "y_lip": round(y_lip, 3),
        "states": states,
    }


def main():
    result = {
        "units": {"coordinates": "mm", "profile": "outward growth in mm", "added": "cm3"},
        "contour_note": "Growth front is the source t = 1.2 contour; one saved CAO iteration is presented as a season, not calibrated time.",
        "profile_note": "Nearest element-centroid thickness, converted as 5 mm * (t - 1), smoothed with a 3 mm Gaussian and monotonically accumulated as in plot_growth_years.py. Null marks the knot footprint.",
        "cases": {},
    }
    for case in CASES:
        exported = export_case(case)
        result["cases"][case] = exported
        states = exported["states"]
        print(case, "steps", states[0]["step"], "to", states[-1]["step"],
              "contours", [len(state["fronts"]) for state in (states[0], states[-1])],
              "added_cm3", states[-1]["added_cm3"],
              "failure_index", states[-1]["failure_index"],
              "failure_load", states[-1]["failure_load"], flush=True)
    serialized = json.dumps(result, separators=(",", ":"), allow_nan=False)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(serialized)
    print(f"Wrote {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
