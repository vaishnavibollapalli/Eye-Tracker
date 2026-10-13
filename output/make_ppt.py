"""
=============================================================================
Build the clustering-comparison PowerPoint deck
=============================================================================
One slide per poster: poster name, the three methods' cluster images side by
side (winner badge on the winning one), a side note naming the best method
and why, plus that winning method's path.jpg and path_animation.mp4
(embedded, click-to-play) from output/Poster Summary/<poster>/.

Run compare_methods.py and make_path_animations.py first.

Usage:
    python make_ppt.py
=============================================================================
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hierarchical_common import POSTERS

HERE = Path(__file__).resolve().parent
COMPARISON_CSV = HERE / "Hierarchical Clustering" / "method_comparison.csv"
SUMMARY_DIR = HERE / "Poster Summary"
OUT_PPTX = HERE / "Eye_Tracking_Clustering_Comparison.pptx"

METHOD_DIRS = {
    "DBSCAN":        HERE / "DBSCAN output",
    "Agglomerative": HERE / "Hierarchical Clustering" / "Agglomerative",
    "Divisive":      HERE / "Hierarchical Clustering" / "Divisive",
}
METHOD_IMG = {
    "DBSCAN": "dbscan_clusters.png",
    "Agglomerative": "agglomerative_clusters.png",
    "Divisive": "divisive_clusters.png",
}
METHOD_ORDER = ["DBSCAN", "Agglomerative", "Divisive"]

# --- palette -----------------------------------------------------------
INK = RGBColor(0x14, 0x25, 0x23)
MUTED = RGBColor(0x5C, 0x71, 0x6E)
ACCENT = RGBColor(0x1F, 0x6F, 0x63)
ACCENT_BG = RGBColor(0xDC, 0xEE, 0xEA)
BG_DARK = RGBColor(0x14, 0x20, 0x1F)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BORDER = RGBColor(0xDB, 0xE4, 0xE3)


def add_title_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = BG_DARK

    tb = slide.shapes.add_textbox(Inches(0.8), Inches(2.5), Inches(11.73), Inches(1.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Eye-Tracking Region Clustering"
    p.font.size = Pt(44); p.font.bold = True; p.font.color.rgb = WHITE
    p.font.name = "Georgia"

    p2 = tf.add_paragraph()
    p2.text = "DBSCAN vs. Agglomerative vs. Divisive Hierarchical Clustering"
    p2.font.size = Pt(22); p2.font.color.rgb = RGBColor(0xB9, 0xED, 0xE1)
    p2.space_before = Pt(10)

    p3 = tf.add_paragraph()
    p3.text = "15 posters · 48 participants · fixation regions compared across three clustering methods"
    p3.font.size = Pt(14); p3.font.color.rgb = RGBColor(0x9B, 0xB0, 0xAC)
    p3.space_before = Pt(14)
    return slide


def add_bullet_slide(prs, title, bullets, sub_bullets_char="–"):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = WHITE

    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.35), Inches(12.33), Inches(0.7))
    p = tb.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = INK
    p.font.name = "Georgia"

    body = slide.shapes.add_textbox(Inches(0.6), Inches(1.15), Inches(12.1), Inches(6.0))
    tf = body.text_frame
    tf.word_wrap = True
    first = True
    for item in bullets:
        if isinstance(item, tuple):
            text, level = item
        else:
            text, level = item, 0
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.text = ("• " if level == 0 else f"    {sub_bullets_char} ") + text
        p.font.size = Pt(17 if level == 0 else 14)
        p.font.color.rgb = INK if level == 0 else MUTED
        p.font.bold = level == 0
        p.space_after = Pt(8 if level == 0 else 4)
    return slide


def add_results_table_slide(prs, comparison: pd.DataFrame):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = WHITE

    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.33), Inches(0.6))
    p = tb.text_frame.paragraphs[0]
    p.text = "Results at a Glance"
    p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = INK
    p.font.name = "Georgia"

    rows = len(comparison) + 1
    cols = 6
    table_shape = slide.shapes.add_table(rows, cols, Inches(0.5), Inches(1.05),
                                         Inches(12.33), Inches(6.1))
    table = table_shape.table
    headers = ["Poster", "Winner", "k", "Silhouette", "Davies-Bouldin", "Noise %"]
    widths = [3.6, 2.3, 0.7, 1.7, 1.9, 1.5]
    for i, w in enumerate(widths):
        table.columns[i].width = Inches(w)
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(12)
        cell.text_frame.paragraphs[0].font.color.rgb = WHITE
        cell.fill.solid(); cell.fill.fore_color.rgb = ACCENT

    for r, (_, row) in enumerate(comparison.iterrows(), start=1):
        w = row["winner"]
        pfx = f"{w}_"
        vals = [row["poster"].replace("poster_", ""), w,
               str(int(row[f"{pfx}k"])), f"{row[f'{pfx}silhouette']:.3f}",
               f"{row[f'{pfx}davies_bouldin']:.3f}",
               f"{row[f'{pfx}noise_pct']:.1f}" if row[f"{pfx}noise_pct"] > 0.05 else "0.0"]
        for c, v in enumerate(vals):
            cell = table.cell(r, c)
            cell.text = v
            cell.text_frame.paragraphs[0].font.size = Pt(11)
            cell.text_frame.paragraphs[0].font.color.rgb = INK
            cell.fill.solid()
            cell.fill.fore_color.rgb = ACCENT_BG if r % 2 == 0 else WHITE
    return slide


def add_poster_slide(prs, poster_key: str, label: str, comparison_row: pd.Series):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = WHITE

    winner = comparison_row["winner"]
    reason = comparison_row["reason"]

    # title
    tb = slide.shapes.add_textbox(Inches(0.3), Inches(0.12), Inches(12.73), Inches(0.55))
    p = tb.text_frame.paragraphs[0]
    p.text = label
    p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = INK
    p.font.name = "Georgia"

    # row 1: three method thumbnails
    thumb_w = 2.833
    thumb_h = thumb_w / 1.5
    row1_top = 0.78
    gap = 0.12
    for i, method in enumerate(METHOD_ORDER):
        left = 0.3 + i * (thumb_w + gap)
        img_path = METHOD_DIRS[method] / poster_key / METHOD_IMG[method]
        is_winner = method == winner
        if img_path.exists():
            pic = slide.shapes.add_picture(str(img_path), Inches(left), Inches(row1_top),
                                           width=Inches(thumb_w))
            if is_winner:
                pic.line.color.rgb = ACCENT
                pic.line.width = Pt(3)
        label_box = slide.shapes.add_textbox(Inches(left), Inches(row1_top + thumb_h + 0.02),
                                             Inches(thumb_w), Inches(0.26))
        lp = label_box.text_frame.paragraphs[0]
        lp.text = ("★ " if is_winner else "") + method
        lp.font.size = Pt(12); lp.font.bold = is_winner
        lp.font.color.rgb = ACCENT if is_winner else MUTED
        lp.alignment = PP_ALIGN.CENTER

    # note box (right side, aligned with row 1)
    note_left = 0.3 + 3 * (thumb_w + gap) + 0.05
    note_w = 13.333 - note_left - 0.3
    note = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(note_left), Inches(row1_top),
                                  Inches(note_w), Inches(thumb_h + 0.3))
    note.fill.solid(); note.fill.fore_color.rgb = ACCENT_BG
    note.line.color.rgb = ACCENT; note.line.width = Pt(1)
    tf = note.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.15); tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.1); tf.margin_bottom = Inches(0.1)
    p = tf.paragraphs[0]
    p.text = f"Best method: {winner}"
    p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = ACCENT
    p2 = tf.add_paragraph()
    p2.text = reason
    p2.font.size = Pt(11); p2.font.color.rgb = INK
    p2.space_before = Pt(6)

    # row 2: path jpg + animation video
    media_w = 4.6
    media_h = media_w / 1.5
    row2_top = row1_top + thumb_h + 0.3 + 0.2
    total_w = media_w * 2 + 0.3
    row2_left = (13.333 - total_w) / 2

    sdir = SUMMARY_DIR / poster_key
    jpg_path = sdir / "path.jpg"
    mp4_path = sdir / "path_animation.mp4"

    if jpg_path.exists():
        slide.shapes.add_picture(str(jpg_path), Inches(row2_left), Inches(row2_top), width=Inches(media_w))
    cap1 = slide.shapes.add_textbox(Inches(row2_left), Inches(row2_top + media_h + 0.03),
                                    Inches(media_w), Inches(0.3))
    c1p = cap1.text_frame.paragraphs[0]
    c1p.text = f"Path ({winner})"
    c1p.font.size = Pt(12); c1p.font.italic = True; c1p.font.color.rgb = MUTED
    c1p.alignment = PP_ALIGN.CENTER

    video_left = row2_left + media_w + 0.3
    if mp4_path.exists():
        poster_frame = str(jpg_path) if jpg_path.exists() else None
        slide.shapes.add_movie(str(mp4_path), Inches(video_left), Inches(row2_top),
                               Inches(media_w), Inches(media_h),
                               poster_frame_image=poster_frame, mime_type="video/mp4")
    cap2 = slide.shapes.add_textbox(Inches(video_left), Inches(row2_top + media_h + 0.03),
                                    Inches(media_w), Inches(0.3))
    c2p = cap2.text_frame.paragraphs[0]
    c2p.text = f"Animation ({winner}) — click to play"
    c2p.font.size = Pt(12); c2p.font.italic = True; c2p.font.color.rgb = MUTED
    c2p.alignment = PP_ALIGN.CENTER

    return slide


def main():
    if not COMPARISON_CSV.exists():
        sys.exit(f"{COMPARISON_CSV} not found -- run compare_methods.py first")
    comparison = pd.read_csv(COMPARISON_CSV).set_index("poster", drop=False)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    add_title_slide(prs)

    add_bullet_slide(prs, "Methodology — Parameters Changed From Library Defaults", [
        "Outlier filtering (applied before any clustering, identically for all 3 methods)",
        ("Not a library default — custom pre-filter: a fixation is dropped if its distance to its "
         "10th-nearest neighbour exceeds median + 3×MAD (robust z-score cutoff)", 1),
        ("Removes stray/isolated fixations (4–10% per poster) that would otherwise stretch a "
         "region's boundary or anchor their own spurious micro-cluster", 1),
        "DBSCAN (sklearn.cluster.DBSCAN)",
        ("Default eps=0.5, min_samples=5 are meaningless at 1936×1208 pixel scale — grid-searched "
         "eps ∈ {18…80}px × min_samples ∈ {8…30} instead", 1),
        ("k (region count) chosen from a narrowed 3–5 range (not the default unconstrained "
         "cluster count DBSCAN would otherwise find)", 1),
        ("Selection criterion is a combined silhouette + Davies-Bouldin \"separation\" score, not "
         "silhouette alone — and the noise-fraction gate (2–25%, capped at 40% on fallback) "
         "stops DBSCAN from \"winning\" via a tiny ultra-dense core with most points discarded", 1),
        "Agglomerative (scipy.cluster.hierarchy.linkage)",
        ("Linkage changed from scipy's default 'single' (chains nearest-neighbour pairs into long, "
         "stringy clusters) to 'ward' (minimizes within-cluster variance → compact, convex regions)", 1),
        ("Cut height (k) chosen 3–5 by the same combined separation score", 1),
        "Divisive (bisecting k-means — hand-built; scikit-learn has no divisive clustering class)",
        ("Each 2-way split's inner KMeans uses n_init=10 (explicit, not version-dependent 'auto') "
         "and random_state=42 (sklearn default is None / non-reproducible)", 1),
        ("Split-selection rule is deliberate: always bisect the cluster with the largest current SSE, "
         "so splits are spent where they most increase separation", 1),
        ("k chosen 3–5 by the same combined separation score", 1),
    ])

    add_results_table_slide(prs, comparison.reset_index(drop=True))

    for poster_key, (label, _img) in POSTERS.items():
        if poster_key not in comparison.index:
            print(f"  ! no comparison row for {poster_key}, skipped")
            continue
        add_poster_slide(prs, poster_key, label, comparison.loc[poster_key])
        print(f"  added slide: {poster_key}")

    prs.save(OUT_PPTX)
    print(f"\nSaved {OUT_PPTX}")


if __name__ == "__main__":
    main()
