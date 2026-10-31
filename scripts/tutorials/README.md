# Tutorials: Obsidian → website + Moodle zip

The tutorial text lives in Obsidian. One script turns the notes into

1. **website pages** in `_courses/` (built and published by GitHub Actions on push), and
2. **an offline zip** in `assets/downloads/` (named by `offline_zip`, or `<series>_offline.zip` by default): plain HTML pages, ready to upload to
   Moodle or open from disk. Set `show_offline_download: false` in `tutorials.yml` to omit the
   offline section and download button from the website overview while still generating the ZIP.
   Set `offline_overview: false` to leave the overview with cards out of the ZIP; the first part is
   then `index.html` itself (used for the one-page beam/shell/solid series).

## Everyday use

1. Write / edit the notes in Obsidian (`800 Teaching/Abaqus Tutorials/...`).
2. Run, from the repository root:

   ```bash
   python scripts/tutorials/build_tutorials.py
   ```

3. Read the report it prints: missing images, links to notes outside the series, and the `[!todo]`
   callouts it left out.
4. Check the offline preview it names (`scripts/tutorials/.cache/offline/<series>/index.html`, open it in a
   browser). It has the same content as the website pages.
5. Commit and push. GitHub Actions rebuilds the site; the zip is published with it.

Never edit the generated files (`_courses/abaqus_*.md`, `assets/img/tutorials/`, the zip): they are
overwritten on every run.

To prepare website pages for review before creating a Moodle ZIP, run:

```bash
python scripts/tutorials/build_tutorials.py abaqus_plate_with_hole --website-only
```

This updates the website pages and media only. Existing ZIPs and the offline preview are left
untouched. The plate-with-hole overview omits the offline download section in all build modes.

## Adding things

- **A new part**: add an entry under `parts:` in `tutorials.yml` (note name, slug, title, one-line card
  text, thumbnail). The order in the file is the order of the parts and of the Previous/Next buttons.
- **A new series**: copy the whole series block in `tutorials.yml` and change the fields.
- **Thumbnails / cover**: any image in the repo, path given in `tutorials.yml`.
- **Subtitle**: the line under a page title is the note's first `# Heading`, else the card text. Set
  `subtitle:` on a part to replace it, or `subtitle: ""` to show none.
- **Figure aliases / publication corrections**: a part can define `figure_aliases` for source figure
  labels that have no exported anchor, or `text_overrides` for a specific correction to a read-only source
  note. Each override must match exactly once when the builder runs.

The current custom thumbnail folder is `assets/img/plate_hole/`: `cover.svg`, `tut1.svg` through
`tut3.svg` for Parts 1–3, `part4.svg` for Part 4, and `part5.svg` for Part 5. The older `tut4.svg`
and `tut5.svg` filenames predate the six-part series; use the mapping in `tutorials.yml` rather
than inferring the part number from those filenames.

## What is converted

| In Obsidian | On the page |
|---|---|
| `![[Files/img.png\|Caption]]` on its own line | numbered figure: **Figure N:** Caption |
| `![[Files/img.png]]` on its own line | figure without a caption box |
| `![[Files/img.png\|600]]` | figure, at most 600 px wide, without a caption box |
| Portrait image | centered at its natural width, up to 360 px wide and 1000 px tall; landscape images fill the article width |
| `![[Files/video.mp4\|Caption]]` on its own line | numbered figure with a video player (muted, no autoplay). Remove the sound and shrink it first with `blender -b --factory-startup -P reencode_video.py -- in.mp4 out.mp4` (script in `Teaching/plate_with_hole/plate_tutorial_2/`) |
| `![[Files/icon.png]]` inside a sentence | small inline icon |
| `![[Files/drawing.excalidraw]]` | the exported `drawing.excalidraw.light.svg` (or `.svg` / `.png`) next to it |
| `Figure [[Files/img.png]]`, `[[Files/img.png]]` | "Figure N" link to that figure |
| `[[Part 3 - ...]]`, `[[Part 3 - ...\|text]]`, `[[Part 3 - ...#Heading]]` | link to that part |
| `> [!cue]`, `> [!tip]`, `> [!warning] Title`, `> [!note]` | coloured box (title = given title or Tip/Warning/Note) |
| `> [!todo] ...` | **left out** (author notes, e.g. missing screenshots), listed in the report |
| `>[!SUMMARY]-` boxes | left out (Obsidian tables of contents) |
| `$...$`, `$$...$$` | Inline math and display math respectively, including in figure/table captions |
| ` ```tikz ` blocks | compiled with pdflatex to SVG (cached in `.cache/`) |
| `%% comment %%` | left out |
| first `# Heading` of the note | page subtitle |

Excalidraw drawings need their SVG export: in the Excalidraw plugin settings turn on
*Embedding Excalidraw into your Notes and Exporting → Export settings → Auto-export SVG*, or use the
command *Export to SVG* on the drawing.

## Putting the zip on Moodle

1. In the course, turn editing on → *Add an activity or resource* → **File**.
2. Drag the ZIP named by `offline_zip` in `tutorials.yml` into the file box.
3. Click the zip in the box → **Unzip**. Then click `index.html` → **Set main file**. (The zip itself can
   be deleted from the box.)
4. *Appearance → Display*: **Open** (or *New window*). Save.

Students then click the resource and get the overview page with links to all parts. The pages only use
relative links, so the same folder also works when opened straight from disk.

The offline pages keep the tutorial title and Previous/Next/Overview buttons, but omit the website's
top header. They reuse its typography, CSS and distill scripts. Fonts, MathJax,
and the page libraries are included in the zip, so figures, captions, and formulas render without a
connection. External reference links still need internet. `main.css` is downloaded from the live site on
every build and kept in `site_main.css` as a fallback. The local tutorial dependencies live in `vendor/`.

## Continuing this series

The source notes are in the Obsidian vault named by `vault` and `folder` in `tutorials.yml`.
The same file lists the published parts, their display titles, thumbnails, and the output ZIP name.
Parts 1–4 are enabled for the website and Moodle ZIP. Parts 5–6 have `publish: false`; keep that
setting until each part is ready. The current Moodle package is
`assets/downloads/abaqus_plate_with_hole_moodle_parts_1_4_without_header.zip`.
The older Parts 1–2 archives remain unchanged.

After changing a note or this builder, run
`python scripts/tutorials/build_tutorials.py abaqus_plate_with_hole` from the repository root.
After website approval, this refreshes the website pages, offline preview, copied media, and Moodle ZIP together. If the
configured ZIP is open in Windows and cannot be overwritten, choose a new `offline_zip` name in
`tutorials.yml`, update the Moodle instruction above, and rerun. Do not edit generated pages or ZIP
contents by hand.

Before handing it out, open the preview's `index.html` and every enabled part with the network disabled.
Check the Overview/Previous/Next buttons, figure labels and captions, formulas, local fonts, video,
and desktop/mobile image sizes. Portrait images are capped at 360 px wide and 1000 px tall;
landscape images fill the article width. Check the ZIP has the overview plus one HTML page per enabled part and that
its relative links and assets resolve after extraction.

## Requirements

```bash
python -m pip install --user pyyaml markdown pymdown-extensions pillow
```

plus `pdflatex` and `pdftocairo` (MiKTeX) for TikZ blocks. The vault path is set at the top of
`tutorials.yml`.
