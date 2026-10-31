"""Export actual CAIO grain paths and result history for the teaching viewer.
Run from the website checkout; requires the sibling Teaching checkout and SciPy.
"""
import json
import sys
from pathlib import Path
from types import SimpleNamespace
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / 'Teaching/plate_with_hole/tree_knot'
sys.path.insert(0, str(SOURCE))
# The source plot module accepts a theme argument during import.
sys.argv = [sys.argv[0], 'light']
from plot_tree import grain_lines, read_mesh

export = {}
for case in ('circle', 'diamond_r1'):
    hist = json.loads((SOURCE / f'results/{case}_history.json').read_text())['history']
    mesh = SOURCE.parent / f"shape_study/models/{'shape_circle' if case == 'circle' else 'diamond_r1p00'}.inp"
    nodes, elements = read_mesh(mesh.read_text())
    model = SimpleNamespace(nodes=nodes, elements=elements)
    states = []
    for step in (0, 1, hist[-1]['iteration']):
        result = np.load(SOURCE / f'results/{case}_it{step:02d}.npz')
        paths, domain = grain_lines(model, result['theta'], spacing=0.7)
        # Keep the displayed central 54 mm; paths retain the source tracer geometry.
        segments = []
        for path in paths:
            inside = np.abs(path[:, 0]) <= 27
            cuts = np.flatnonzero(np.diff(np.r_[False, inside, False]))
            for start, end in zip(cuts[::2], cuts[1::2]):
                part = path[start:end]
                if len(part) > 2:
                    part = np.vstack([part[::3], part[-1]])
                    segments.append(np.round(part, 3).tolist())
        states.append({'step': step, 'lines': segments})
        print(case, step, len(segments), flush=True)
    edges = domain.xy[domain.edges]
    edges = edges[np.all(np.abs(edges[:, :, 0]) < 27, axis=1)]
    export[case] = {'states': states, 'outline': np.round(edges, 3).tolist(),
                    'history': [{k: row[k] for k in ('iteration', 'failure_load', 'tau_LR_max')} for row in hist]}
(ROOT / 'assets/data/do-it-grain.json').write_text(json.dumps(export, separators=(',', ':')))
for step in ('05', '10', '20', '40'):
    img = Image.open(SOURCE / f'out/growth_years_dark/branch40_front_s{step}.png')
    img.thumbnail((1440, 810))
    img.save(ROOT / f'assets/img/do-it-labs/branch40_front_s{step}.webp', quality=85)
