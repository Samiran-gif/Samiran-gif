import json
import re
from pathlib import Path

from PIL import Image, ImageDraw

DATA_FILE = Path("data/contributions.json")
OUTPUT_FILE = Path("contrib-heatmap.gif")

CELL_SIZE = 12
GAP = 3
PADDING = 20
FRAME_DURATION = 35

LEVEL_COLORS = {
    0: (22, 27, 34),
    1: (14, 68, 41),
    2: (0, 109, 78),
    3: (38, 166, 65),
    4: (57, 211, 83),
}


def load_cells():
    with DATA_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    html = data["html"]

    pattern = re.compile(
        r'<td\b[^>]*'
        r'data-date="([^"]+)"[^>]*'
        r'data-level="(\d+)"[^>]*'
        r'[^>]*class="ContributionCalendar-day"[^>]*>',
        re.DOTALL,
    )

    cells = pattern.findall(html)

    if not cells:
        # More flexible fallback: find every contribution cell
        pattern = re.compile(
            r'<td\b(?=[^>]*class="ContributionCalendar-day")'
            r'(?=[^>]*data-date="([^"]+)")'
            r'(?=[^>]*data-level="(\d+)")[^>]*>',
            re.DOTALL,
        )

        cells = pattern.findall(html)

    if not cells:
        raise RuntimeError(
            "Could not find GitHub contribution cells in contributions.json"
        )

    return [(date, int(level)) for date, level in cells]


def main():
    cells = load_cells()

    print(f"Contribution cells found: {len(cells)}")

    rows = 7
    columns = (len(cells) + rows - 1) // rows

    width = (
        PADDING * 2
        + columns * CELL_SIZE
        + (columns - 1) * GAP
    )

    height = (
        PADDING * 2
        + rows * CELL_SIZE
        + (rows - 1) * GAP
    )

    frames = []

    for visible_column in range(columns):
        image = Image.new(
            "RGB",
            (width, height),
            (13, 17, 23),
        )

        draw = ImageDraw.Draw(image)

        for index, (_, level) in enumerate(cells):
            column = index // rows
            row = index % rows

            if column > visible_column:
                continue

            x = PADDING + column * (CELL_SIZE + GAP)
            y = PADDING + row * (CELL_SIZE + GAP)

            draw.rounded_rectangle(
                (
                    x,
                    y,
                    x + CELL_SIZE,
                    y + CELL_SIZE,
                ),
                radius=2,
                fill=LEVEL_COLORS.get(level, LEVEL_COLORS[0]),
            )

        frames.append(image)

    frames[0].save(
        OUTPUT_FILE,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION,
        loop=0,
        optimize=False,
    )

    print(f"Animated heatmap created: {OUTPUT_FILE}")
    print(f"Frames: {len(frames)}")


if __name__ == "__main__":
    main()