import json
import re
from pathlib import Path
from html import escape

DATA_FILE = Path("data/contributions.json")
OUTPUT_FILE = Path("contrib-heatmap.svg")

data = json.loads(DATA_FILE.read_text(encoding="utf-8"))

html = data["html"]

# Extract GitHub contribution cells
matches = re.findall(
    r'<td[^>]*data-date="([^"]+)"[^>]*data-level="([^"]+)"[^>]*>',
    html,
)

if not matches:
    raise RuntimeError("Could not find contribution data on GitHub.")

# Keep the most recent 365 days
matches = matches[-365:]

cell_size = 12
gap = 3
columns = 53
rows = 7

width = columns * (cell_size + gap)
height = rows * (cell_size + gap) + 35

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'viewBox="0 0 {width} {height}" '
    f'role="img">',
    '<rect width="100%" height="100%" fill="#0d1117"/>',
    '<text x="10" y="20" fill="#c9d1d9" '
    'font-family="monospace" font-size="12">'
    f'{escape(data["username"])} // contribution activity'
    '</text>',
]

colors = {
    "0": "#161b22",
    "1": "#0e4429",
    "2": "#006d32",
    "3": "#26a641",
    "4": "#39d353",
}

for index, (date, level) in enumerate(matches):
    column = index // rows
    row = index % rows

    x = 10 + column * (cell_size + gap)
    y = 28 + row * (cell_size + gap)

    color = colors.get(level, colors["0"])

    svg.append(
        f'<rect x="{x}" y="{y}" width="{cell_size}" '
        f'height="{cell_size}" rx="2" fill="{color}">'
        f'<title>{escape(date)} — level {escape(level)}</title>'
        '</rect>'
    )

svg.append("</svg>")

OUTPUT_FILE.write_text("\n".join(svg), encoding="utf-8")

print(f"Created {OUTPUT_FILE}")