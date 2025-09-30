import tkinter as tk
import time
import random
from PIL import Image, ImageTk

HEIGHT = WIDTH = 600
FONT = ("Poppins", 60, 'italic')

OCCUPIED_GRIDS = []
grid = {}
game_over = False
user_tic = 'x'
def position_tics(canvas, tic, x1, y1, x2, y2):
    x_pos, y_pos = (x1 + x2) / 2, (y1 + y2) / 2
    canvas.create_text(int(x_pos), int(y_pos),
                       text=tic, fill="pink", font=FONT)


def draw_line(grid: dict, position: list, color: str):
    start = grid[position[0]]
    end = grid[position[2]]
    canvas.create_line(start[0][0], start[0][1],
                       end[1][0], end[1][1], fill=color, width=5)


def check_win(canvas, all_plays: list, grid: dict):
    global game_over
    if game_over:
        return True
    winning_positions = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                         [0, 4, 8], [2, 4, 6],
                         [0, 3, 6], [1, 4, 7], [2, 5, 8]]
    x_plays = [v for d in all_plays for k, v in d.items() if k == 'x']
    o_plays = [v for d in all_plays for k, v in d.items() if k == 'o']

    def display_outcome(winner_char, win_pos=None):
        nonlocal canvas
        global game_over
        if win_pos:
            draw_line(grid, win_pos, 'white')
        if user_tic == winner_char:
            canvas.create_text(HEIGHT / 2, WIDTH / 2, text='You Win', fill="Yellow", font=FONT)
        else:
            canvas.create_text(HEIGHT / 2, WIDTH / 2, text='You Lose', fill="Red", font=FONT)
        root.after(2000, root.quit)
    for position in winning_positions:
        if set(position).issubset(x_plays):
            display_outcome('x', position)
            game_over = True
            return True
        if set(position).issubset(o_plays):
            display_outcome('o', position)
            game_over = True
            return True
    if len(o_plays + x_plays) == 9:
        canvas.create_text(HEIGHT/2, WIDTH/2, text='Draw', fill="White", font=FONT)
        root.after(2000, root.quit)
        game_over = True
        return True
    return False

def initialize_grid():
    """Initializes the grid coordinates for the game board."""
    x_beginning, y_beginning = 77, 84
    x_end, y_end = 224, 207
    return {
        # for row 1
        0: ((x_beginning, y_beginning), (x_end, y_end)),
        1: ((x_end, y_beginning), (x_end + 130, y_end)),
        2: ((x_end + 130, y_beginning), (x_end + 260, y_end)),
        # for row 2
        3: ((x_beginning, y_end), (x_end, y_end + 130)),
        4: ((x_end, y_end), (x_end + 130, y_end + 130)),
        5: ((x_end + 130, y_end), (x_end + 260, y_end + 130)),
        # for row 3
        6: ((x_beginning, y_end + 130), (x_end, y_end + 290)),
        7: ((x_end, y_end + 130), (x_end + 130, y_end + 290)),
        8: ((x_end + 130, y_end + 130), (x_end + 260, y_end + 290))
    }

def get_computer_play():
        global OCCUPIED_GRIDS, grid, user_tic
        occupied_pos = [value for d in OCCUPIED_GRIDS for value in d.values()]
        available_grids = {key: value for key, value in grid.items() if key not in occupied_pos}
        if not available_grids:
            return
        computer_tic = 'o' if user_tic == 'x' else 'x'
        computer_play = random.choice(list(available_grids.keys()))
        ((x1, y1), (x2, y2)) = available_grids[computer_play]
        position_tics(canvas, computer_tic, x1, y1, x2, y2)
        OCCUPIED_GRIDS.append({computer_tic: computer_play})
        check_win(canvas, OCCUPIED_GRIDS, grid)


def user_play(event):
    global canvas, user_tic, grid
    if game_over:
        return
    print(f'{user_tic} pos x={event.x}, y={event.y}')
    if 77 <= event.x <= 465 and 84 <= event.y <= 500:
        for i, cell in grid.items():
            x1, y1 = cell[0]
            x2, y2 = cell[1]
            if (x1 <= event.x <= x2 and y1 <= event.y <= y2 and i not in
                    [value for d in OCCUPIED_GRIDS for value in d.values()]):
                position_tics(canvas, user_tic, x1, y1, x2, y2)
                OCCUPIED_GRIDS.append({user_tic: i})

                if not check_win(canvas, OCCUPIED_GRIDS, grid):
                    root.after(1000, get_computer_play)
                break


def setup_game(canvas):
    """Initializes and starts the game."""
    global grid, user_tic
    grid = initialize_grid()
    # Get user's tic selection (e.g., 'x' or 'o')
    # Check if the computer plays first
    # if user_tic == 'o':
    #     root.after(500, get_computer_play())
    # Bind the mouse click event to the user's turn handler
    canvas.bind("<Button-1>", user_play)

# initializing window
root = tk.Tk()

# setting up display
root.title("TicTacToe")
root.geometry(f"{HEIGHT}x{WIDTH}")
root.resizable(False, False)

pil_image = Image.open('images/TicTacToe.jpg').convert('RGBA')

tk_image = ImageTk.PhotoImage(pil_image)
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.create_image(0, 0, anchor="nw", image=tk_image)

canvas.place(x=0, y=0, relwidth=1, relheight=1)

setup_game(canvas)
root.mainloop()
