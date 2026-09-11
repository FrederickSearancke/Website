"""Render the saved EBM term using user-selected equal square buckets.

Run with Python from any directory. Source CSV is the unchanged exported
native-bin table. Missing/unknown outer bins were excluded by its exporter.
The axes represent ordered bins, not equal numerical volatility intervals.
Points follow the same within-bin mapping. Scores remain unchanged.
"""
from pathlib import Path
import csv
import json
from html import escape
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ASSET = HERE.parent / 'dist/assets/ebm-paired-interaction.svg'
CHART_ASSET = HERE.parent / 'dist/assets/ebm-paired-interaction-chart.svg'
CSV = HERE / 'ebm-interaction-grid.csv'
WIDTH, HEIGHT = 660, 526
LEFT, TOP, CELL, N = 128, 28, 26, 14
# Tighten the colour range from +/-2 to +/-1.5 pp: 33% more colour contrast,
# with the true scale shown in the legend and no clipping of this term.
LIMIT = 1.5
BG = '#0C2A4E'
INK = '#E7F1FF'
MUTED = '#ADC1DB'
NEGATIVE = '#307AB0'
ZERO = '#D6E2EB'
POSITIVE = '#F4B352'


def rgb(color):
    return tuple(int(color[k:k+2], 16) for k in (1, 3, 5))


def color(score):
    assert -LIMIT <= score <= LIMIT, 'Do not silently clip learned values'
    fraction = abs(score) / LIMIT
    a, b = rgb(ZERO), rgb(POSITIVE if score >= 0 else NEGATIVE)
    return '#' + ''.join(f'{round(x + fraction*(y-x)):02x}' for x, y in zip(a, b))


def scene():
    """Shared exact geometry for SVG, PNG inspection, and PDF export."""
    rows = list(csv.DictReader(CSV.open(encoding='utf-8', newline='')))
    cells = {(int(r['first_feature_bin_index']), int(r['second_feature_bin_index'])): float(r['score']) for r in rows}
    assert len(rows) == len(cells) == N*N
    assert set(cells) == {(i, j) for i in range(N) for j in range(N)}
    data = json.loads((HERE / 'ebm-interaction-observations.json').read_text(encoding='utf-8'))
    xe, ye = data['x_edges'], data['y_edges']
    assert len(xe) == len(ye) == N+1 and xe[0] == ye[0] == 0
    shapes = [('rect', 0, 0, WIDTH, HEIGHT, BG)]
    for (i, j), score in sorted(cells.items()):
        shapes.append(('cell', LEFT+i*CELL, TOP+(N-1-j)*CELL,
                       CELL, CELL, color(score), i, j, score))
    for i in range(N+1):
        x, y = LEFT+i*CELL, TOP+i*CELL
        shapes += [('line', x, TOP, x, TOP+N*CELL, '#AFBECD', .35),
                   ('line', LEFT, y, LEFT+N*CELL, y, '#AFBECD', .35)]
    observations = data['points']
    assert len(observations) == 653
    for p in observations:
        shapes.append(('dot', LEFT+p['x_bucket_position']*CELL,
                       TOP+(N-p['y_bucket_position'])*CELL, 1.3, '#102B42', .42,
                       p['x_value'], p['y_value']))
    shapes += [('text', LEFT, 414, 'LOW', 13, MUTED, 'start'),
               ('text', LEFT+N*CELL, 414, 'HIGH', 13, MUTED, 'end'),
               ('text', LEFT+N*CELL/2, 441, '09:00–09:29 volatility', 18, INK, 'middle'),
               ('rotate_text', 47, TOP+N*CELL/2, '09:30–09:59 volatility', 18, INK),
               ('text', 111, TOP+12, 'HIGH', 13, MUTED, 'end'),
               ('text', 111, TOP+N*CELL-2, 'LOW', 13, MUTED, 'end')]
    # The legend is continuous; the model surface is not interpolated.
    legend_x, legend_y, legend_w, legend_h = 520, TOP, 13, N*CELL
    for k in range(182):
        value = LIMIT - 2*LIMIT*k/181
        shapes.append(('rect', legend_x, legend_y+k*legend_h/182, legend_w, legend_h/182, color(value)))
    for v, label in [(1.5, '+1.5'), (0, '0'), (-1.5, '−1.5')]:
        y = legend_y+(LIMIT-v)/(2*LIMIT)*legend_h
        shapes += [('line', legend_x+legend_w+3, y, legend_x+legend_w+8, y, MUTED, 1),
                   ('text', legend_x+legend_w+14, y+5, label, 15, INK, 'start')]
    shapes += [('rotate_text', 606, TOP+N*CELL/2, 'Forecast contribution (pp)', 16, MUTED),
               ('text', WIDTH/2, 485, 'Premarket × opening · Learned interaction', 15, INK, 'middle'),
               ('text', WIDTH/2, 510, 'Ordered volatility buckets · 653 observed days', 14, MUTED, 'middle')]
    return shapes


def render_svg():
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Term 1: premarket and opening volatility</title>',
        '<desc id="desc">Term 1 from page 1 of Latest EBM Learned Functions, 756-observation window, seed 20260901. Inputs: 09:00–09:29 and 09:30–09:59 volatility. Each of 14 by 14 equal square cells is one native bucket pair. Axes show ordered buckets, not equal numerical ranges; the 653 observed training-day points follow the same within-bin mapping. Blue lowers the forecast and amber raises it. The colour scale is minus 1.5 to plus 1.5 percentage points to make the pattern clearer, without clipping or altering any term score.</desc>']
    for shape in scene():
        kind, *v = shape
        if kind in ('rect', 'cell'):
            x, y, w, h, fill, *extra = v
            attrs = ''
            if extra:
                i, j, score = extra
                attrs = f' data-bin-x="{i}" data-bin-y="{j}" data-score="{score!r}"'
            parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{attrs}/>')
        elif kind == 'dot':
            x, y, radius, fill, opacity, raw_x, raw_y = v
            parts.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" opacity="{opacity}" data-observed-x="{raw_x!r}" data-observed-y="{raw_y!r}"/>')
        elif kind == 'line':
            x1, y1, x2, y2, stroke, width = v
            parts.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{stroke}" stroke-width="{width}"/>')
        elif kind == 'text':
            x, y, label, size, fill, anchor = v
            parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-family="Arial, sans-serif">{escape(label)}</text>')
        elif kind == 'rotate_text':
            x, y, label, size, fill = v
            parts.append(f'<text transform="translate({x} {y}) rotate(-90)" font-size="{size}" fill="{fill}" text-anchor="middle" font-family="Arial, sans-serif">{escape(label)}</text>')
    parts.append('</svg>')
    full_svg = '\n'.join(parts)
    ASSET.write_text(full_svg, encoding='utf-8')
    # The homepage omits the axis titles, legend title, and image footer. Keep
    # the Low/High directions and colour scale; model geometry is unchanged.
    # Captions are ordinary HTML beside the image in the first project row.
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    chart = ET.fromstring(full_svg)
    chart.set('viewBox', '0 0 660 430')
    chart.set('height', '430')
    homepage_omitted_labels = {'09:00–09:29 volatility', '09:30–09:59 volatility', 'Forecast contribution (pp)'}
    for element in list(chart):
        if element.tag.endswith('}text') and (
            float(element.get('y', '0')) >= 480 or element.text in homepage_omitted_labels
        ):
            chart.remove(element)
    CHART_ASSET.write_text(ET.tostring(chart, encoding='unicode'), encoding='utf-8')
    return ASSET


if __name__ == '__main__':
    print(render_svg())
