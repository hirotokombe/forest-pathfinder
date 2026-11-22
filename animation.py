from PIL import Image, ImageDraw, ImageFont

def save_path_gif(grid, path, out_path="animation.gif", cell=32, delay_ms=400):
    """
    Creates and saves an animated GIF visualizing an agent moving along a path
    on a grid. Each frame shows the agent at the next position in the path.

    Parameters:
        grid (list[list[str]]): 2D grid representation of the environment
        path (list[tuple]): Sequence of (row, col) positions for the agent
        out_path (str): Output filename for the GIF
        cell (int): Pixel size of each grid cell
        delay_ms (int): Delay between frames in milliseconds
    """
    rows, cols = len(grid), len(grid[0])
    w, h = cols * cell, rows * cell

    # Color mapping for grid tiles
    colors = {
        ".": (235, 235, 235),
        "#": (40, 40, 40),
        "f": (255, 170, 80),
        "F": (255, 90, 70),
        "S": (120, 200, 120),
        "*": (120, 140, 255),
    }
    agent_color = (255, 215, 0)

    frames = []
    for i, (ar, ac) in enumerate(path):
        img = Image.new("RGB", (w, h), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        # Draw the grid for the current frame
        for r in range(rows):
            for c in range(cols):
                x0, y0 = c * cell, r * cell
                x1, y1 = x0 + cell, y0 + cell
                tile = grid[r][c]
                draw.rectangle([x0, y0, x1, y1], fill=colors.get(tile, (200, 200, 200)), outline=(180, 180, 180))

        # Draw the agent at its current position
        x0, y0 = ac * cell, ar * cell
        x1, y1 = x0 + cell, y0 + cell
        pad = cell // 6
        draw.ellipse([x0 + pad, y0 + pad, x1 - pad, y1 - pad], fill=agent_color)

        frames.append(img)

    # Save frames as an animated GIF
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=delay_ms,
        loop=0,
    )
