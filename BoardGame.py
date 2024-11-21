from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Initialize the grid
GRID_SIZE = 5
grid = [["green" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Starting positions for players
player_positions = {
    "red": (0, 0),  # Player 1
    "blue": (GRID_SIZE - 1, GRID_SIZE - 1),  # Player 2
}
grid[0][0] = "red"
grid[GRID_SIZE - 1][GRID_SIZE - 1] = "blue"

# Track turn
turn = "red"  # "red" for Player 1, "blue" for Player 2

def get_adjacent_spaces(position):
    """Get all valid adjacent spaces for a given position."""
    x, y = position
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),  # Vertical and Horizontal
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal
    ]
    adjacent = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[nx][ny] == "green":
            adjacent.append((nx, ny))
    return adjacent

@app.route("/")
def index():
    """Render the game board."""
    global turn
    return render_template(
        "index.html",
        grid=grid,
        turn=turn,
        get_adjacent_spaces=get_adjacent_spaces,
        player_positions=player_positions,
        enumerate=enumerate,  # Pass enumerate explicitly
    )

@app.route("/move", methods=["POST"])
@app.route("/move", methods=["POST"])
def move():
    """Handle a player move."""
    global turn, grid, player_positions

    # Get the move from the form
    x, y = int(request.form["x"]), int(request.form["y"])

    # Validate the move
    if (x, y) in get_adjacent_spaces(player_positions[turn]):
        # Update the grid and player position
        grid[x][y] = turn
        player_positions[turn] = (x, y)

        # Switch turns
        turn = "blue" if turn == "red" else "red"

    # Redirect back to the main page
    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    """Reset the game."""
    global grid, player_positions, turn
    grid = [["green" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    grid[0][0] = "red"
    grid[GRID_SIZE - 1][GRID_SIZE - 1] = "blue"
    player_positions = {"red": (0, 0), "blue": (GRID_SIZE - 1, GRID_SIZE - 1)}
    turn = "red"
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
