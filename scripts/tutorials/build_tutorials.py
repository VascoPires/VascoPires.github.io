"""Publish Obsidian tutorial notes to the website and to a Moodle-ready zip.

    python scripts/tutorials/build_tutorials.py [series id ...]

Reads scripts/tutorials/tutorials.yml. For every series it converts the Obsidian notes
(wiki links, embeds, callouts, math, TikZ blocks) into

  * Jekyll pages in _courses/ (rendered by GitHub Actions like the rest of the site), and
  * a self-contained HTML folder, zipped to assets/downloads/ (name set by offline_zip), that can be
    uploaded to Moodle (or opened from disk) as it is.

Needs: pyyaml, markdown, pymdown-extensions, Pillow; pdflatex + pdftocairo for TikZ blocks.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree

import markdown
import yaml
from PIL import Image

HERE = Path(__file__).resolve().parent
SITE = HERE.parents[1]
CACHE = HERE / ".cache"
VIDEO_EXT = {".mp4", ".webm"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"} | VIDEO_EXT   # everything a figure can show
CALLOUT_TITLES = {"cue": "Tip", "tip": "Tip", "hint": "Tip", "warning": "Warning", "caution": "Warning",
                  "note": "Note", "info": "Note", "important": "Important", "summary": "Summary",
                  "example": "Example", "question": "Question", "danger": "Danger"}
DROP_CALLOUTS = {"todo"}          # author notes: never published, listed in the build report
# Obsidian callout type -> class in the site's _sass/_callouts.scss (info, tip, warning, danger)
CALLOUT_CLASS = {"cue": "tip", "tip": "tip", "hint": "tip", "example": "tip", "warning": "warning",
                 "caution": "warning", "important": "warning", "danger": "danger", "error": "danger",
                 "note": "info", "info": "info", "question": "info", "summary": "info"}
CALLOUT_ICON = {"tip": "💡", "warning": "⚠️", "danger": "⛔", "info": "ℹ️"}


# --------------------------------------------------------------------------- helpers
def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower(), flags=re.UNICODE)
    return re.sub(r"[\s_-]+", "-", text).strip("-")


def heading_id(text: str) -> str:
    """Anchor of a heading as kramdown (auto_ids) and python-markdown (toc) both write it."""
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"\s+", "-", text.strip())


def image_orientation(path: Path) -> str:
    """Classify the displayed image so only horizontal figures fill the article."""
    if path.suffix.lower() == ".svg":
        root = ElementTree.parse(path).getroot()
        view_box = root.get("viewBox", "").replace(",", " ").split()
        if len(view_box) == 4:
            width, height = float(view_box[2]), float(view_box[3])
        else:
            width = float(re.match(r"[\d.]+", root.get("width", "")).group())
            height = float(re.match(r"[\d.]+", root.get("height", "")).group())
    else:
        with Image.open(path) as image:
            width, height = image.size
            if image.getexif().get(274) in (5, 6, 7, 8):
                width, height = height, width
    if width > height:
        return "landscape"
    return "portrait"


@dataclass
class Figure:
    number: int
    fig_id: str
    out_name: str          # file name in the output image folder


@dataclass
class Page:
    part: dict
    index: int
    source: Path
    title_h1: str = ""
    body: str = ""
    figures: dict = field(default_factory=dict)   # resolved source path -> Figure


class Report:
    def __init__(self):
        self.todos, self.warnings, self.held = [], [], []

    def warn(self, page, msg):
        self.warnings.append(f"[{page}] {msg}")


# --------------------------------------------------------------------------- converter
class Converter:
    def __init__(self, cfg: dict, series: dict, report: Report):
        self.vault = Path(cfg["vault"])
        if not self.vault.exists():
            drive = re.match(r"^([A-Za-z]):[/\\](.*)$", cfg["vault"])
            if drive:
                wsl_path = Path("/mnt") / drive.group(1).lower() / drive.group(2).replace("\\", "/")
                if wsl_path.exists():
                    self.vault = wsl_path
        self.series = series
        self.folder = self.vault / series["folder"]
        self.report = report
        self.images: dict[Path, str] = {}          # source file -> output file name
        self.notes = {p["note"]: p for p in series["parts"]}
        self.held = {}                                # parts with publish: false (set by build)

    # ---- resolving files ------------------------------------------------------
    def resolve(self, target: str, note_dir: Path) -> Path | None:
        target = target.split("#")[0].strip()
        cands = []
        for base in (note_dir, self.folder, self.vault):
            p = (base / target)
            cands += [p]
            if p.suffix.lower() == ".excalidraw" or target.endswith(".excalidraw"):
                cands += [p.with_name(p.name + ".light.svg"), p.with_name(p.name + ".svg"),
                          p.with_name(p.name + ".png")]
        for c in cands:
            if c.is_file() and c.suffix.lower() in IMAGE_EXT:
                return c.resolve()
        # last resort: search the vault by file name
        name = Path(target).name
        for suffix in ("", ".light.svg", ".svg", ".png"):
            hits = list(self.vault.rglob(name + suffix))
            hits = [h for h in hits if h.suffix.lower() in IMAGE_EXT]
            if hits:
                return hits[0].resolve()
        return None

    def out_name(self, src: Path) -> str:
        if src not in self.images:
            stem = src.name
            for ext in (".light.svg", ".dark.svg"):
                if stem.endswith(ext):
                    stem = stem[: -len(ext)]
                    break
            else:
                stem = src.stem
            stem = slugify(stem.replace(".excalidraw", "")) or "image"
            name = stem + (".svg" if src.name.endswith(".svg") else src.suffix.lower())
            used = set(self.images.values())
            k = 2
            while name in used:
                name = f"{stem}-{k}{Path(name).suffix}"
                k += 1
            self.images[src] = name
        return self.images[src]

    # ---- TikZ -----------------------------------------------------------------
    def tikz(self, code: str, page: str) -> Path | None:
        CACHE.mkdir(parents=True, exist_ok=True)
        h = hashlib.sha1(code.encode()).hexdigest()[:12]
        svg = CACHE / f"tikz-{h}.svg"
        if svg.exists():
            return svg
        body = code.strip()
        if "\\documentclass" not in body:
            pre = "\\documentclass[tikz,border=4pt]{standalone}\n\\usepackage{amsmath}\n"
            body = pre + body if "\\begin{document}" in body else pre + "\\begin{document}\n" + body + "\n\\end{document}"
        with tempfile.TemporaryDirectory() as tmp:
            tex = Path(tmp) / "fig.tex"
            tex.write_text(body, encoding="utf-8")
            try:
                subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "fig.tex"],
                               cwd=tmp, check=True, capture_output=True, timeout=180)
                subprocess.run(["pdftocairo", "-svg", "fig.pdf", str(svg)], cwd=tmp, check=True,
                               capture_output=True, timeout=60)
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
                self.report.warn(page, f"TikZ block could not be compiled ({e.__class__.__name__}); left out")
                return None
        return svg

    # ---- main conversion ---------------------------------------------------------
    def convert(self, page: Page, pages: dict) -> None:
        name = page.part["note"]
        text = page.source.read_text(encoding="utf-8")
        text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)         # front matter
        text = re.sub(r"%%.*?%%", "", text, flags=re.S)                    # Obsidian comments
        for edit in page.part.get("text_overrides", []):
            old, new = edit["from"], edit["to"]
            if text.count(old) != 1:
                raise ValueError(f"expected one occurrence of {old!r} in {page.source}")
            text = text.replace(old, new)
        note_dir = page.source.parent

        # first H1 becomes the page subtitle
        m = re.search(r"^# (.+)$", text, flags=re.M)
        if m:
            page.title_h1 = m.group(1).strip()
            text = text[: m.start()] + text[m.end():]

        # protect code: TikZ blocks become figures, other fences are kept verbatim
        fences = []

        def keep_fence(mm):
            lang, code = mm.group(1).strip().lower(), mm.group(2)
            if lang == "tikz":
                svg = self.tikz(code, name)
                if svg is None:
                    return ""
                return f"![[{svg.as_posix()}]]"
            fences.append(mm.group(0))
            return f"\x00FENCE{len(fences) - 1}\x00"

        text = re.sub(r"^```([^\n]*)\n(.*?)^```[ \t]*$", keep_fence, text, flags=re.S | re.M)
        spans = []

        def keep_span(mm):
            spans.append(mm.group(0))
            return f"\x00SPAN{len(spans) - 1}\x00"

        text = re.sub(r"`[^`\n]+`", keep_span, text)

        text = self.callouts(text, name)
        text = self.number_figures(page, text, note_dir)
        text = re.sub(
            r'(<figcaption class="caption">)</figcaption></figure>\s*\*\*Figure \d+:\*\*\s*(.+)$',
            lambda m: f'{m.group(1)}{self.inline_md(m.group(2).strip())}</figcaption></figure>',
            text, flags=re.M,
        )
        # A following "Figure N:" line may supply a caption; omit all remaining empty ones.
        text = text.replace('<figcaption class="caption"></figcaption>', "")
        text = self.links(page, text, note_dir, pages)
        text = self.tables(text)

        for i, s in enumerate(spans):
            text = text.replace(f"\x00SPAN{i}\x00", s)
        for i, f in enumerate(fences):
            text = text.replace(f"\x00FENCE{i}\x00", f)
        page.body = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"

    def callouts(self, text: str, page: str) -> str:
        out, lines, i = [], text.split("\n"), 0
        head = re.compile(r"^>\s*\[!(\w+)\]([-+]?)\s*(.*)$")
        while i < len(lines):
            m = head.match(lines[i])
            if not m:
                out.append(lines[i])
                i += 1
                continue
            kind, fold, title = m.group(1).lower(), m.group(2), m.group(3).strip()
            body, i = [], i + 1
            while i < len(lines) and lines[i].startswith(">"):
                body.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            # a one-line callout keeps its text on the title line
            if not body and title:
                body, title = [title], ""
            if kind in DROP_CALLOUTS:
                self.report.todos.append(f"[{page}] {' '.join([title] + body).strip()}")
                continue
            if kind == "summary" and fold == "-":
                continue                                   # Obsidian table-of-contents boxes
            label = title or CALLOUT_TITLES.get(kind, kind.capitalize())
            cls = CALLOUT_CLASS.get(kind, "info")
            if fold:                                       # [!x]- folded, [!x]+ open: a toggle the reader clicks
                out += ["", f'<details{" open" if fold == "+" else ""} markdown="1">',
                        f"<summary>{self.inline_md(label)}</summary>", ""] + body + ["", "</details>", ""]
                continue
            # same markup as the site's _sass/_callouts.scss expects
            out += ["", f'<div class="callout {cls}" markdown="1">',
                    f'<div class="callout-title"><span class="callout-icon">{CALLOUT_ICON[cls]}</span>'
                    f"<span>{self.inline_md(label)}</span></div>",
                    '<div class="callout-body" markdown="1">', ""] + body + ["", "</div>", "</div>", ""]
        return "\n".join(out)

    def number_figures(self, page: Page, text: str, note_dir: Path) -> str:
        """Number every embed that stands on its own line, so refs before it also work."""
        embed = re.compile(r"!\[\[([^\]|]+)(?:\|([^\]]*))?\]\]")
        n = 0
        for line in text.split("\n"):
            mm = embed.fullmatch(line.strip())
            if not mm:
                continue
            src = self.resolve(mm.group(1), note_dir)
            if src is None or src in page.figures:
                continue
            n += 1
            out = self.out_name(src)
            page.figures[src] = Figure(n, "fig-" + Path(out).stem, out)

        def repl(mm):
            src = self.resolve(mm.group(1), note_dir)
            opt = (mm.group(2) or "").strip()
            if src is None:
                self.report.warn(page.part["note"], f"missing image: {mm.group(1)}")
                return f"*[missing figure: {html.escape(mm.group(1))}]*"
            name = self.out_name(src)
            fig = page.figures.get(src)
            line_start = mm.string.rfind("\n", 0, mm.start()) + 1
            line_end = mm.string.find("\n", mm.end())
            if line_end < 0:
                line_end = len(mm.string)
            whole_line = (not mm.string[line_start:mm.start()].strip()
                          and not mm.string[mm.end():line_end].strip())
            width = opt if opt.isdigit() else ""
            caption = "" if opt.isdigit() else opt
            if not whole_line or fig is None:                          # small inline icon
                return f'<img class="tut-icon" src="{{IMG}}/{name}" alt="{html.escape(caption)}">'
            style = f' style="max-width:min(100%, {width}px)"' if width else ""
            if src.suffix.lower() in VIDEO_EXT:
                # silent screen recording: controls, no autoplay, loads only when played
                media = (f'<video class="img-fluid rounded" src="{{IMG}}/{name}" controls muted playsinline '
                         f'preload="metadata"{style}></video>')
            else:
                orientation = image_orientation(src)
                media = (f'<img class="img-fluid rounded tut-{orientation}" src="{{IMG}}/{name}" '
                         f'alt="{html.escape(caption)}"{style}>')
            # Keep the caption inside the figure so the site CSS adds "Figure N:".
            return (f'\n<figure class="article-figure" id="{fig.fig_id}">{media}'
                    f'<figcaption class="caption">{self.inline_md(caption)}</figcaption></figure>\n')

        return embed.sub(repl, text)

    @staticmethod
    def inline_md(s: str) -> str:
        """Format raw HTML text while preserving inline and display math from the note."""
        s = html.escape(s)
        math_spans = []

        def keep_math(match):
            delimiter, body = match.group(1), match.group(2)
            math_spans.append(f"$${body}$$" if delimiter == "$$" else rf"\({body}\)")
            return f"\x00MATH{len(math_spans) - 1}\x00"

        # Captions are raw HTML: Kramdown does not parse their math. Give MathJax
        # explicit inline delimiters, and protect TeX from the emphasis rules.
        s = re.sub(r"(?<![\\$])(\${1,2})(?!\$)(.+?)(?<!\\)\1(?!\$)", keep_math, s, flags=re.S)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
        for i, math in enumerate(math_spans):
            s = s.replace(f"\x00MATH{i}\x00", math)
        return s

    def links(self, page: Page, text: str, note_dir: Path, pages: dict) -> str:
        wiki = re.compile(r"(Figure\s+)?\[\[([^\]|]+)(?:\|([^\]]*))?\]\]")
        tables = re.findall(r"\*\*Table (\d+):\*\*", text)

        def fig_link(fig):
            return f"[Figure {fig.number}](#{fig.fig_id})"

        def repl(mm):
            had_fig, target, alias = mm.group(1), mm.group(2).strip(), (mm.group(3) or "").strip()
            pre = had_fig or ""
            if target.startswith("#fig:") or target.startswith("#^fig"):
                key = slugify(target.split(":", 1)[-1])
                aliases = page.part.get("figure_aliases", {})
                if key in aliases:
                    for fig in page.figures.values():
                        if fig.number == aliases[key]:
                            return fig_link(fig)
                for fig in page.figures.values():
                    if key and key in fig.out_name.replace("_", "-"):
                        return fig_link(fig)
                return pre + "the figure below"
            if target.startswith("#tab:"):
                return (pre or "") + (f'[{tables[0]}](#tab-{tables[0]})' if tables else "the table")
            if target.startswith("#"):
                return pre + f"[{alias or target[1:]}](#{heading_id(target[1:])})"
            note, _, anchor = target.partition("#")
            if note in self.notes:
                part = self.notes[note]
                frag = f"#{heading_id(anchor)}" if anchor else ""
                return pre + f"[{alias or part['title']}]({{PAGE:{part['slug']}}}{frag})"
            if note in self.held:                     # part not published yet: plain text, no link
                return pre + (alias or self.held[note]["title"])
            src = self.resolve(target, note_dir)
            if src is not None and src in page.figures:
                return fig_link(page.figures[src])
            if src is not None:
                return pre + (alias or Path(target).stem)
            self.report.warn(page.part["note"], f"link to a note outside the series: [[{target}]]")
            return pre + (alias or note)

        return wiki.sub(repl, text)

    @staticmethod
    def tables(text: str) -> str:
        """Blank line after every table, and `**Table N:** text` lines as the site's caption box."""
        text = re.sub(r"(^\|.*\|[ \t]*\n)(?=[^|\n])", r"\1\n", text, flags=re.M)
        return re.sub(r"^\*\*Table (\d+):\*\*[ \t]*(.*)$",
                      lambda m: f'<div class="caption table-caption" id="tab-{m.group(1)}">'
                                f"<strong>Table {m.group(1)}:</strong> {Converter.inline_md(m.group(2))}</div>",
                      text, flags=re.M)


# --------------------------------------------------------------------------- math
def math_for_kramdown(text: str) -> str:
    """kramdown only knows $$...$$: block math needs blank lines, inline $x$ becomes $$x$$."""
    parts = re.split(r"(\x00.*?\x00|```.*?```|`[^`\n]+`|<[^>]+>)", text, flags=re.S)
    out = []
    for p in parts:
        if not p or p.startswith(("```", "`", "<", "\x00")):
            out.append(p)
            continue
        p = re.sub(r"\$\$(.+?)\$\$", lambda m: "\n\n$$" + m.group(1).strip() + "$$\n\n"
                   if "\n" in m.group(1) else m.group(0), p, flags=re.S)
        p = re.sub(r"(?<![\$\\])\$(?!\$)([^\$\n]+?)(?<![\s\\])\$(?!\$)", r"$$\1$$", p)
        out.append(p)
    return "".join(out)


# --------------------------------------------------------------------------- writers
# Everything else (fonts, colours, captions, callouts, buttons) comes from the site's own CSS.
EXTRA_CSS = """
d-article figure.article-figure { text-align: center; margin: 1.5rem 0 0.25rem; }
d-article figure.article-figure img { display: block; width: auto; max-width: min(100%, 360px); height: auto; max-height: 1000px; margin-inline: auto; }
d-article figure.article-figure img.tut-landscape { width: 100%; max-width: 100%; max-height: none; }
d-article figure.article-figure video { width: 100%; height: auto; background: #000; }
.tutorial-nav .btn { text-transform: none; }
.tut-icon { height: 1.2em; vertical-align: -0.2em; }
.callout .callout-body > :last-child { margin-bottom: 0; }
"""
WEBSITE_CSS = """
@media (max-width: 767.98px) {
  .post.distill > d-title { padding-top: calc(56px + 2rem); }
}
"""
OVERVIEW_CSS = (".part-card .card { border: 1px solid #e5e7eb; }\n"
                ".part-card .card:hover { box-shadow: 0 6px 18px rgba(0,0,0,0.08); transform: translateY(-2px); "
                "transition: all 150ms ease; }\n"
                ".part-tag { display: inline-block; padding: 3px 8px; margin-bottom: 6px; background: #eef2ff; "
                "color: #314b8c; border-radius: 4px; font-size: 12px; font-weight: 600; letter-spacing: 0.03em; }\n")
LIVE_CSS = "https://www.vascodcpires.com/assets/css/main.css"
# repo files the offline bundle needs, copied to the same relative path
OFFLINE_ASSETS = ["assets/css/bootstrap.min.css", "assets/css/mdb.min.css",
                  "assets/css/jekyll-pygments-themes-github.css",
                  "assets/js/bootstrap.bundle.min.js", "assets/js/distillpub/template.v2.js",
                  "assets/js/distillpub/transforms.v2.js", "assets/js/distillpub/overrides.js",
                  "assets/img/web_icon.ico"]


def subtitle(pg):
    """Line under the page title: the part's `subtitle` if set (may be empty), else the note's H1 or the card text."""
    if "subtitle" in pg.part:
        return pg.part["subtitle"] or ""
    return pg.title_h1 or pg.part.get("card", "")


def nav_html(series, i, link, overview=True, back_to=None):
    """Same buttons as the site's tutorial pages (styled by .tutorial-nav in _sass/_base.scss).
    `back_to` = (page id, button text) replaces the button back to the series overview."""
    parts = series["parts"]
    target, label = back_to or (series["id"], "Back to tutorial overview")
    back = (f'<a class="btn btn-outline-primary" href="{link(target)}">&larr; {label}</a>'
            if overview else "")
    if not back and len(parts) == 1:
        return ""
    right = []
    if i > 0:
        right.append(f'<a class="btn btn-outline-primary" href="{link(parts[i - 1]["slug"])}">'
                     f"&larr; Previous: Part {i}</a>")
    if i < len(parts) - 1:
        right.append(f'<a class="btn btn-primary" href="{link(parts[i + 1]["slug"])}">Next: Part {i + 2} &rarr;</a>')
    return (f'<div class="d-flex justify-content-between flex-wrap gap-2 tutorial-nav mb-3">{back}'
            f'<div class="d-flex gap-2">{"".join(right)}</div></div>')


def card_html(href, img, tag, title, text):
    return f"""  <div class="col d-flex">
    <a class="w-100" href="{href}">
      <div class="card h-100 hoverable">
        <img class="card-img-top" src="{img}" alt="{tag} thumbnail">
        <div class="card-body">
          <span class="part-tag">{tag}</span>
          <h5 class="card-title mb-2">{html.escape(title.split(':', 1)[-1].strip())}</h5>
          <p class="card-text">{html.escape(text)}</p>
        </div>
      </div>
    </a>
  </div>"""


def cards_page_html(intro, cover, heading, cards):
    out = f"<p>{html.escape(intro)}</p>\n\n"
    if cover:
        out += f'<img class="img-fluid rounded mb-3" src="{cover}" alt="Cover">\n\n'
    return (out + f"<style>\n{OVERVIEW_CSS}</style>\n\n<h2>{heading}</h2>\n\n"
            '<div class="row row-cols-1 row-cols-md-3 g-3 part-card mb-4">\n' + "\n".join(cards) + "\n</div>\n")


def overview_html(series, link, asset, zip_href=None):
    cards = [card_html(link(p["slug"]), asset(p["thumb"]), f"Part {i + 1}", p["title"], p.get("card", ""))
             for i, p in enumerate(series["parts"])]
    out = cards_page_html(series.get("intro", ""), asset(series["cover"]), "Tutorial Parts", cards)
    if zip_href:
        out += ("\n<h2>Offline version</h2>\n\n"
                "<p>All parts as HTML pages in one zip file, to read without internet "
                "or to upload to Moodle.</p>\n\n"
                f'<p><a class="btn btn-primary" href="{zip_href}" download>Download the offline version (.zip)</a></p>\n')
    return out


def write_jekyll(series, pages, conv, *, include_offline=True, course=None):
    img_url = f"../../assets/img/tutorials/{series['id']}"
    web_link = lambda slug: f"../{slug}/"
    for pg in pages:
        body = pg.body.replace("{IMG}", img_url)
        body = re.sub(r"\{PAGE:([\w-]+)\}", lambda m: web_link(m.group(1)), body)
        body = math_for_kramdown(body)
        nav = nav_html(series, pg.index, web_link,
                       back_to=(course["id"], "Back to course overview") if course else None)
        fm = {
            "layout": "distill",
            "title": pg.part["title"],
            "description": subtitle(pg),
            "img": pg.part.get("thumb", ""),
            "permalink": f"/courses/{pg.part['slug']}/",
            "date": str(series.get("date", "")),
            "tags": series.get("tags", []),
            "giscus_comments": False,
            "hidden": True,
            "nav": False,
        }
        text = ("---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True)
                + "_styles: >\n" + "".join("  " + l + "\n" for l in (EXTRA_CSS + WEBSITE_CSS).strip().split("\n"))
                + "---\n\n<!-- Generated by scripts/tutorials/build_tutorials.py from the Obsidian note "
                + f"\"{pg.part['note']}\". Edit the note, not this file. -->\n\n"
                + "{% raw %}\n" + nav + "\n\n" + body + "\n" + nav + "\n{% endraw %}\n")
        (SITE / "_courses" / f"{pg.part['slug']}.md").write_text(text, encoding="utf-8")

    fm = {"layout": "page", "title": series["title"], "img": series.get("cover", ""),
          "importance": series.get("importance", 4)}
    if series.get("resource_section"):
        fm["resource_section"] = series["resource_section"]
    fm |= {"tags": series.get("tags", []), "giscus_comments": False,
           "date": str(series.get("date", "")), "toc": False,
           "permalink": f"/courses/{series['id']}/"}
    if course:                     # listed on the course page, not on the teaching page
        fm["hidden"] = True
    zip_name = series.get("offline_zip", f"{series['id']}_offline.zip")
    content = overview_html(series, web_link, lambda p: "../../" + p,
                            zip_href=f"../../assets/downloads/{zip_name}"
                            if include_offline and series.get("show_offline_download", True) else None)
    text = ("---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n\n"
            "<!-- Generated by scripts/tutorials/build_tutorials.py. Edit tutorials.yml, not this file. -->\n\n"
            "{% raw %}\n" + content + "{% endraw %}\n")
    (SITE / "_courses" / f"{series['id']}.md").write_text(text, encoding="utf-8")


def published_parts(series):
    return [p for p in series["parts"] if p.get("publish", True)]


def write_course(course, cfg):
    """Course page: one card per class (a series). A one-part class links straight to its page."""
    by_id = {s["id"]: s for s in cfg["series"]}
    cards = []
    for n, sid in enumerate(course["classes"], 1):
        series, parts = by_id[sid], published_parts(by_id[sid])
        one = len(parts) == 1
        cards.append(card_html(f"../{parts[0]['slug'] if one else sid}/", "../../" + series["cover"],
                               f"Class {n}", series["title"],
                               parts[0].get("card", "") if one else series.get("intro", "")))
    fm = {"layout": "page", "title": course["title"], "img": course.get("cover", ""),
          "importance": course.get("importance", 4)}
    if course.get("resource_section"):
        fm["resource_section"] = course["resource_section"]
    fm |= {"tags": course.get("tags", []), "giscus_comments": False, "toc": False,
           "permalink": f"/courses/{course['id']}/"}
    content = cards_page_html(course.get("intro", ""), "../../" + course["cover"] if course.get("cover") else "",
                              "Classes", cards)
    text = ("---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n\n"
            "<!-- Generated by scripts/tutorials/build_tutorials.py. Edit tutorials.yml, not this file. -->\n\n"
            "{% raw %}\n" + content + "{% endraw %}\n")
    (SITE / "_courses" / f"{course['id']}.md").write_text(text, encoding="utf-8")


# Offline pages reuse the live site's typography and layout assets, without its site header.
OFFLINE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<title>{title} | Vasco D. C. Pires</title>
<link rel="stylesheet" href="assets/css/bootstrap.min.css">
<link rel="stylesheet" href="assets/css/mdb.min.css">
<link rel="stylesheet" href="assets/css/jekyll-pygments-themes-github.css">
<link rel="shortcut icon" href="assets/img/web_icon.ico">
<link rel="stylesheet" href="assets/css/tutorial-fonts.css">
<link rel="stylesheet" href="assets/css/main.css">
<style>{extra_css}</style>
<script src="assets/vendor/jquery.min.js"></script>
<script>window.MathJax = {{ tex: {{ tags: "ams" }} }};</script>
<script defer src="assets/vendor/mathjax/tex-mml-chtml.js"></script>
{head_extra}
</head>
<body>
{front_matter}
{main}
<footer class="sticky-bottom mt-5" role="contentinfo"><div class="container">
&copy; Vasco D. C. Pires &middot; also online at
<a href="https://vascodcpires.com/" target="_blank" rel="noopener">vascodcpires.com</a>
</div></footer>
<script src="assets/js/bootstrap.bundle.min.js"></script>
<script src="assets/vendor/mdb.min.js"></script>
</body>
</html>
"""
DISTILL_HEAD = ('<script src="assets/js/distillpub/template.v2.js"></script>\n'
                '<script src="assets/js/distillpub/transforms.v2.js"></script>\n'
                '<script src="assets/js/distillpub/overrides.js"></script>')
DISTILL_FRONT = ('<d-front-matter><script async type="text/json">{{"title": {title}, "description": {desc}, '
                 '"authors": []}}</script></d-front-matter>')


def site_css() -> str:
    """The live site's compiled main.css; a copy is kept next to this script for offline builds."""
    import urllib.request
    keep = HERE / "site_main.css"
    try:
        with urllib.request.urlopen(LIVE_CSS, timeout=20) as r:
            css = r.read().decode("utf-8")
        keep.write_text(css, encoding="utf-8")
        return css
    except Exception as e:                                       # no internet: use the last copy
        if keep.exists():
            print(f"  (could not download {LIVE_CSS}: {e}; using the saved copy)")
            return keep.read_text(encoding="utf-8")
        raise SystemExit(f"cannot get the site CSS from {LIVE_CSS} and there is no saved copy: {e}")


def write_offline(series, pages, conv, out_dir: Path) -> Path:
    import json
    if out_dir.exists():
        shutil.rmtree(out_dir)
    img_rel = f"assets/img/tutorials/{series['id']}"
    (out_dir / img_rel).mkdir(parents=True)
    for rel in OFFLINE_ASSETS + [p["thumb"] for p in series["parts"]] + [series.get("cover", "")]:
        if rel and (SITE / rel).is_file():
            (out_dir / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(SITE / rel, out_dir / rel)
    for folder in ("fonts", "webfonts"):
        for source in (SITE / "assets" / folder).iterdir():
            if source.is_file() and source.suffix.lower() in {".woff2", ".woff", ".ttf", ".otf"}:
                target = out_dir / "assets" / folder / source.name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
    for source in (HERE / "vendor").rglob("*"):
        if source.is_file() and source.name != "fonts.css":
            target = out_dir / "assets/vendor" / source.relative_to(HERE / "vendor")
            if source.parent.name == "fonts":
                target = out_dir / "assets/fonts/tutorials" / source.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    (out_dir / "assets/css/tutorial-fonts.css").write_text(
        (HERE / "vendor/fonts.css").read_text(encoding="utf-8"), encoding="utf-8")
    css = site_css().replace('url("/assets/fonts/', 'url("../fonts/')
    (out_dir / "assets/css/main.css").write_text(css, encoding="utf-8")
    for src, name in conv.images.items():
        shutil.copy(src, out_dir / img_rel / name)

    md = markdown.Markdown(extensions=["tables", "md_in_html", "fenced_code", "toc", "attr_list",
                                       "pymdownx.arithmatex", "pymdownx.tilde", "sane_lists"],
                           extension_configs={"pymdownx.arithmatex": {"generic": True}})
    # offline_overview: false -> no card page; the first part itself is index.html
    overview = series.get("offline_overview", True)
    home = series["id"] if overview else series["parts"][0]["slug"]
    link = lambda slug: "index.html" if slug == home else f"{slug}.html"
    for pg in pages:
        body = pg.body.replace("{IMG}", img_rel)
        body = re.sub(r"\{PAGE:([\w-]+)\}", lambda m: link(m.group(1)), body)
        md.reset()
        nav = nav_html(series, pg.index, link, overview)
        desc = subtitle(pg)
        sub = f"<p>{html.escape(desc)}</p>" if desc else ""
        main = ('<div class="post distill">\n'
                f"<d-title><h1>{html.escape(pg.part['title'])}</h1>{sub}</d-title>\n"
                f"<d-article>\n{nav}\n{md.convert(body)}\n{nav}\n</d-article>\n</div>")
        front = DISTILL_FRONT.format(title=json.dumps(pg.part["title"]), desc=json.dumps(desc))
        (out_dir / link(pg.part["slug"])).write_text(OFFLINE_HTML.format(
            title=html.escape(pg.part["title"]), extra_css=EXTRA_CSS, head_extra=DISTILL_HEAD,
            front_matter=front, main=main, series_id=series["id"]), encoding="utf-8")

    if not overview:
        return out_dir
    content = overview_html(series, link, lambda p: p)
    main = ('<div class="container mt-4" role="main"><div class="post">\n<header class="post-header">'
            f'<h1 class="post-title sedgwick-ave-regular" style="font-size: 50px; font-weight: 500;">'
            f"{html.escape(series['title'])}</h1></header>\n<article>\n{content}</article>\n</div></div>")
    (out_dir / "index.html").write_text(OFFLINE_HTML.format(
        title=html.escape(series["title"]), extra_css="", head_extra="", front_matter="", main=main,
        series_id=series["id"]), encoding="utf-8")
    return out_dir


def build(cfg, series, report, *, website_only=False):
    # parts with `publish: false` are left out everywhere (pages, cards, buttons, zip);
    # links to them become plain text, and their old generated pages are removed
    held = [p for p in series["parts"] if not p.get("publish", True)]
    series = dict(series, parts=[p for p in series["parts"] if p.get("publish", True)])
    report.held = [p["title"] for p in held]
    for p in held:
        old = SITE / "_courses" / f"{p['slug']}.md"
        if old.exists() and "Generated by scripts/tutorials/build_tutorials.py" in old.read_text(encoding="utf-8"):
            old.unlink()
    conv = Converter(cfg, series, report)
    conv.held = {p["note"]: p for p in held}
    pages = []
    for i, part in enumerate(series["parts"]):
        src = conv.folder / f"{part['note']}.md"
        if not src.exists():
            raise SystemExit(f"note not found: {src}")
        pages.append(Page(part, i, src))
    by_slug = {p.part["slug"]: p for p in pages}
    for pg in pages:
        conv.convert(pg, by_slug)

    # images for the website (folder owned by this script)
    img_dir = SITE / "assets" / "img" / "tutorials" / series["id"]
    if img_dir.exists():
        shutil.rmtree(img_dir)
    img_dir.mkdir(parents=True)
    for src, name in conv.images.items():
        shutil.copy(src, img_dir / name)

    course = next((c for c in cfg.get("courses", []) if series["id"] in c["classes"]), None)
    write_jekyll(series, pages, conv, include_offline=not website_only, course=course)

    if website_only:
        return len(pages), len(conv.images), None, None

    off = CACHE / "offline" / series["id"]
    write_offline(series, pages, conv, off)
    zip_name = series.get("offline_zip", f"{series['id']}_offline.zip")
    zpath = SITE / "assets" / "downloads" / zip_name
    zpath.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(off.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(off).as_posix())
    return len(pages), len(conv.images), zpath, off


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("series", nargs="*", help="Series IDs from tutorials.yml; defaults to all series")
    parser.add_argument("--website-only", action="store_true",
                        help="Generate website pages and media without creating an offline preview or ZIP")
    args = parser.parse_args(argv)
    cfg = yaml.safe_load((HERE / "tutorials.yml").read_text(encoding="utf-8"))
    wanted = set(args.series)
    for series in cfg["series"]:
        if wanted and series["id"] not in wanted:
            continue
        report = Report()
        n, nimg, zpath, off = build(cfg, series, report, website_only=args.website_only)
        if args.website_only:
            print(f"{series['id']}: {n} pages, {nimg} media files -> _courses/ (website only; no ZIP created)")
        else:
            size = zpath.stat().st_size / 1e6
            print(f"{series['id']}: {n} pages, {nimg} images -> _courses/, {zpath.relative_to(SITE)} ({size:.1f} MB)")
            print(f"  preview: {off / 'index.html'}")
        if report.held:
            print(f"  not published yet (publish: false): {', '.join(report.held)}")
        for w in report.warnings:
            print("  WARNING", w)
        if report.todos:
            print(f"  {len(report.todos)} todo callout(s) left out of the published pages:")
            for t in report.todos:
                print("   -", t)
    for course in cfg.get("courses", []):
        write_course(course, cfg)
        print(f"{course['id']}: course page with {len(course['classes'])} classes -> _courses/")


if __name__ == "__main__":
    main(sys.argv[1:])
