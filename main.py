import tkinter as tk
import time
import random
from PIL import Image, ImageTk

OCCUPIED_GRIDS = []
HEIGHT = WIDTH = 600
FONT = ("Poppins", 60, 'italic')
def position_tics(canvas, tic, x1, y1, x2, y2):
    x_pos, y_pos = (x1 + x2) / 2, (y1 + y2) / 2
    canvas.create_text(int(x_pos), int(y_pos),
                       text=tic, fill="pink", font=FONT)


def draw_line(grid: dict, position: list, color: str):
    starting_coord = grid[position[0]]
    end_coord = grid[position[2]]
    canvas.create_line(starting_coord[0][0], starting_coord[0][1],
                       end_coord[1][0], end_coord[1][1], fill=color, width=5)


def check_win(canvas, all_plays: list, grid: dict):
    winning_positions = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                         [0, 4, 8], [2, 4, 6],
                         [0, 3, 6], [1, 4, 7], [2, 5, 8]]
    x_plays, o_plays = [], []
    print('ALL PLAYS', all_plays)
    for play_dict in all_plays:
        for tic, position in play_dict.items():
            if tic == 'x':
                x_plays.append(position)
            elif tic == 'o':
                o_plays.append(position)
    for position in winning_positions:
        if set(position).issubset(x_plays):
            print("X wins")
            draw_line(grid, position, 'White')
            canvas.create_text(HEIGHT/2, WIDTH/2, text='You Win', fill="Yellow", font=FONT)
            root.after(2000, root.quit)
            return True
        if set(position).issubset(o_plays):
            draw_line(grid, position, 'Red')
            canvas.create_text(HEIGHT/2, WIDTH/2, text='You Lose', fill="Red", font=FONT)
            root.after(2000, root.quit)
            return True
    if len(o_plays + x_plays) == 9:
        canvas.create_text(HEIGHT/2, WIDTH/2, text='Draw', fill="White", font=FONT)
        root.after(2000, root.quit)
        return True
    return False


def play(event, tic='x'):
    global canvas, ALL_PLAYS
    print(f'{tic} pos x={event.x}, y={event.y}')
    x_beginning, y_beginning = 77, 84
    x_end, y_end = 224, 207
    grid = {
        # for row 1
        0: ((x_beginning, y_beginning), (x_end, y_end)),
        1: ((x_end, y_beginning), (x_end + 130, y_end)),
        2: ((x_end + 130, y_beginning), (x_end + 260, y_end)),
        # for row 2
        3: ((x_beginning, y_end), (x_end, y_end + 130)),
        4: ((x_end, y_end), (x_end + 130, y_end + 130)),
        5: ((x_end + 130, y_end), (x_end + 240, y_end + 130)),
        # for row 3
        6: ((x_beginning, y_end + 130), (x_end, y_end + 290)),
        7: ((x_end, y_end + 130), (x_end + 130, y_end + 290)),
        8: ((x_end + 130, y_end + 130), (x_end + 260, y_end + 290))
    }

    def get_computer_play():
        global OCCUPIED_GRIDS
        time.sleep(1)

        occupied_pos = [value for d in OCCUPIED_GRIDS for value in d.values()]
        available_grids = {key: value for key, value in grid.items() if key not in occupied_pos}
        try:
            computer_play = random.choice(list(available_grids.keys()))
            position_tics(canvas, 'o', available_grids[computer_play][0][0],
                          available_grids[computer_play][0][1],
                          available_grids[computer_play][1][0],
                          available_grids[computer_play][1][1])
            OCCUPIED_GRIDS.append({'o': computer_play})
            check_win(canvas, OCCUPIED_GRIDS, grid)

        except IndexError: ...


    if 77 <= event.x <= 465 and 84 <= event.y <= 500:
        for i, cell in grid.items():
            x1, y1 = cell[0]
            x2, y2 = cell[1]
            if (x1 <= event.x <= x2 and y1 <= event.y <= y2 and i not in
                    [value for d in OCCUPIED_GRIDS for value in d.values()]):
                position_tics(canvas, tic, x1, y1, x2, y2)
                OCCUPIED_GRIDS.append({'x': i})
                check_win(canvas, OCCUPIED_GRIDS, grid)
                # ALL_PLAYS.append({'x': i})
                print(f"From grid {i + 1}")
                get_computer_play()
                break


# initializing window
root = tk.Tk()

# setting up display
root.title("TicTacToe")
root.geometry(f"{HEIGHT}x{WIDTH}")

pil_image = Image.open('images/TicTacToe.jpg').convert('RGBA')

tk_image = ImageTk.PhotoImage(pil_image)
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.place(x=0, y=0, relwidth=1, relheight=1)
canvas.create_image(0, 0, anchor="nw", image=tk_image)

canvas.focus_set()
canvas.bind('<Button-3>', play)  # support with right click


root.mainloop()
