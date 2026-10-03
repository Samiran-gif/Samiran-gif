from pathlib import Path
import re

FILE = Path("contrib-heatmap.svg")

svg = FILE.read_text(encoding="utf-8")

# Remove the previous CSS animation if it exists.
svg = re.sub(
    r"<style>\s*@keyframes contributionReveal.*?</style>",
    "",
    svg,
    flags=re.DOTALL,
)

# Remove old animation classes/styles.
svg = svg.replace('class="heat-cell"', "")
svg = re.sub(r'\sstyle="animation-delay:[^"]*"', "", svg)

# Find all rectangles.
pattern = re.compile(r"<rect\b[^>]*?(?:/>|>.*?</rect>)", re.DOTALL)

matches = list(pattern.finditer(svg))

output = []
last_end = 0
cell_number = 0

for index, match in enumerate(matches):
    rect = match.group(0)

    # Preserve the first two rectangles as background/border.
    if index >= 2 and "<rect" in rect:
        # Add a small SVG-native fade animation.
        delay = cell_number * 0.015

        animation = (
            f'<animate attributeName="opacity" '
            f'values="0;1" '
            f'dur="0.45s" '
            f'begin="{delay:.3f}s" '
            f'fill="freeze"/>'
        )

        if rect.endswith("/>"):
            rect = rect[:-2] + ">" + animation + "</rect>"
        else:
            rect = rect.replace(">", ">" + animation, 1)

        cell_number += 1

    output.append(svg[last_end:match.start()])
    output.append(rect)
    last_end = match.end()

output.append(svg[last_end:])

FILE.write_text("".join(output), encoding="utf-8")

print(f"Animated heatmap created: {FILE}")
print(f"Animated cells: {cell_number}")