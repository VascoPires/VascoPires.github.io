"""Render source tree models with alpha, then export lossless website WebP files.

Run from the website checkout. BLENDER_BIN can override the Blender executable.
Existing transparent PNGs are reused; delete them to force a fresh render.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os
import shutil
import subprocess
import sys

from PIL import Image

SITE = Path(__file__).resolve().parents[1]
TREE = SITE.parent / 'Teaching' / 'plate_with_hole' / 'tree_knot'
OUTPUT = TREE / 'out' / 'growth_years_transparent'
DEST = SITE / 'assets' / 'img' / 'do-it-labs'
BLENDER = os.environ.get('BLENDER_BIN') or shutil.which('blender') or '/mnt/c/Program Files/Blender Foundation/Blender 4.5/blender.exe'
DEVICE = os.environ.get('BLENDER_DEVICE', 'CPU')
JOBS = [(f'hole_cut_s{s:02}', f't2d_trunk_hole_it{s:02}', ['--view', 'cut', '--cut', '--season', str(s)]) for s in (0, 5, 10, 20, 40)]
JOBS.append(('branch40_front_s40', 't2d_trunk_branch40_it40', ['--view', 'front']))
JOBS.extend((f'branch40_weight_cut_s{s:02}', f't2d_trunk_branch40_weight_it{s:02}', ['--view', 'cut', '--cut', '--season', str(s)]) for s in (0, 5, 10, 20))


def render(job):
    name, stem, options = job
    png = OUTPUT / f'{name}.png'
    if not png.exists():
        samples = '128' if name.startswith('branch40_weight_cut') else '256'
        command = [BLENDER, '-b', '-t', '3', '--factory-startup', '-P', 'render_trunk2d.py', '--', stem,
                   str(png.relative_to(TREE)), '--look', 'wood', '--theme', 'dark', '--res', '75',
                   '--samples', samples, '--device', DEVICE, '--transparent', '--no-save-blend', *options]
        print(f'Rendering {name}', flush=True)
        with (OUTPUT / f'{name}.log').open('w') as log:
            subprocess.run(command, cwd=TREE, stdout=log, stderr=subprocess.STDOUT, check=True)
    with Image.open(png) as source:
        if source.mode != 'RGBA' or source.getchannel('A').getextrema() != (0, 255):
            raise RuntimeError(f'{png}: expected both transparent and opaque pixels')
        source.save(DEST / f'{name}.webp', 'WEBP', lossless=True, method=6)
    print(f'Exported {name}.webp with alpha', flush=True)


if __name__ == '__main__':
    OUTPUT.mkdir(parents=True, exist_ok=True)
    # Build missing branch textures and section rings from the saved weighted case.
    for season in (0, 5, 10, 20):
        if not (TREE / 'textures' / f't2d_trunk_branch40_weight_it{season:02}.json').exists():
            subprocess.run([sys.executable, 'trunk2d_texture.py', 'trunk_branch40_weight', str(season)], cwd=TREE, check=True)
    if not (TREE / 'textures' / 'rings_trunk_branch40_weight.npz').exists():
        subprocess.run([sys.executable, 'plot_growth_years.py', 'trunk_branch40_weight', 'dark'], cwd=TREE, check=True)
    # Serialize GPU jobs to keep this scene within small workstation VRAM budgets.
    with ThreadPoolExecutor(max_workers=2 if DEVICE == 'CPU' else 1) as pool:
        list(pool.map(render, JOBS))
