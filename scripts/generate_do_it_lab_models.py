"""Export teaching-page landing responses from the existing lab solver.

Run with --labs-root PATH if Teaching is outside the sibling checkout.
The public display uses a shared, normalized height scale, without solution
force/stiffness/stroke values. This is the lab's 1-DOF educational comparison.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--labs-root', type=Path, default=ROOT.parent / 'Teaching/do_it_labs')
args = parser.parse_args()
path = args.labs_root / 'lunar_rover_landing_gear/optimized_landing_design.py'
import sys
spec = importlib.util.spec_from_file_location('landing_source', path)
model = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = model
spec.loader.exec_module(model)
k = 10356.838963373199  # existing render_undamped_pretty.py comparison stiffness
zeta = .78  # rounded damping ratio in the existing optimized_design_report.txt
c, v, reaction, eq, damping = model.contact_response(k, zeta)
assert c.max() <= .1801
assert reaction.min() >= -.2
assert np.max(np.abs(c[model.RESPONSE_TIME >= 2] - eq)) < .001
assert np.max(np.abs(v[model.RESPONSE_TIME >= 2])) < .01
# Check the source unilateral spring solver with its native time step.
t_u, y_u, c_u, r_u = model.full_undamped_history(k)
# Check the conservative spring response against total mechanical energy.
dt = t_u[1]-t_u[0]
v_u = np.gradient(y_u, dt)
e = .5*model.MASS*v_u**2 + model.MASS*model.G_MOON*y_u + .5*k*c_u**2
assert (e.max()-e.min()) / e[0] < .015
assert np.any((t_u > .5) & (y_u > model.LEG_LENGTH + .1))
# Use full_animation_history only to get its common pre-contact trajectory.
design = model.DynamicDesign(k, zeta, damping, float(reaction.max()), float(c.max()), eq, 0)
t_d, y_d, compression_d, reaction_d = model.full_animation_history(design)
time = np.linspace(max(t_u[0], t_d[0]), 2.3, 241)
time[np.searchsorted(time, 0)] = 0
y0 = np.interp(time, t_u, y_u)
y1 = np.interp(time, t_d, y_d)
post = time >= 0
cp = np.zeros_like(time); force = np.zeros_like(time)
cp[post], _, force[post], _, _ = model.contact_response(k, zeta, time[post])
y1[post] = model.LEG_LENGTH - cp[post]
# Fixed shared normalization preserves relative motion without publishing scales.
scale = max(y0.max(), y1.max())
result = {'time': [round(float(t), 4) for t in time],
          'damped': [round(float(y/scale), 6) for y in y1],
          'compression': [round(float(x/compression_d.max()), 6) for x in cp],
          'force': [round(float(x/reaction_d.max()), 6) for x in force],
          'rest': round(model.LEG_LENGTH/scale, 6),
          'contactIndex': int(np.searchsorted(time, 0)),
          'description': 'Normalized chassis height; separately normalized compression and gear force from the 1-DOF spring-dashpot model.'}
output = ROOT/'assets/data/do-it-landing.json'
output.write_text(json.dumps(result,separators=(',',':'))+'\n')
print('Landing export: contact retained and settled in damped model; spring rebounds; energy drift below 1.5%.')
print(f'{len(time)} frames exported to {output}')
