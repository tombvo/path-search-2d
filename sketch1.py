from random import randint
from rich import print


import os
import colorama

colorama.init()
os.system("")

board = []
paths = []
paths_time = []

board_cols = 25
board_rows = 15

iteration = 0


class Field:
    def __init__(self, row, col):
        self.row = row
        self.col = col

        self.is_obstacle = False
        self.is_start = False
        self.is_end = False
        self.was_searched: bool = False
        self.best_way = False

    def __repr__(self):
        return f"{self.row} {self.col}"

    def give_info(self):
        return f"Row: {self.row}\nCol: {self.col}\nObstacle: {self.is_obstacle}\nStart: {self.is_start}\nEnd: {self.is_end}"


def move(x):
    print(f"\033[{x}A")


def create_board(r, c):
    l = []
    for i in range(r):
        lst = []
        for x in range(c):
            lst.append(Field(i, x))
        l.append(lst)
    global board
    board = l


def print_board(board: list):
    for x in board:
        print("")
        for i in x:
            if i.is_obstacle == True:
                print("[red]X[/] ", end="")
            elif i.is_start == True:
                print("[green]S[/] ", end="")
            elif i.is_end == True:
                print("[green]E[/] ", end="")
            elif i.best_way == True:
                print("[green]m[/] ", end="")
            elif i.was_searched == True:
                print("[blue]m[/] ", end="")
            elif i.was_searched == False:
                print("[yellow]m[/] ", end="")


def define_start_end_obstacles(start_col, end_col):
    board[0][start_col].is_start = True  # decides starting point
    board[len(board) - 1][end_col].is_end = True  # decides ending point

    for t in board:  # implements obstacles
        if t != board[0] and t != board[len(board) - 1]:
            for x in range(len(t)):
                if randint(1, 4) == 1:
                    t[x].is_obstacle = True


def search_top(field):
    if field.row != 0:
        if board[field.row - 1][field.col].is_obstacle == True:
            return False
        elif board[field.row - 1][field.col].is_start == True:
            return False
        elif board[field.row - 1][field.col].is_end == True:
            board[field.row - 1][field.col].was_searched = True
            return board[field.row - 1][field.col]
        else:
            if board[field.row - 1][field.col].was_searched == True:
                return False
            else:
                board[field.row - 1][field.col].was_searched = True
                return board[field.row - 1][field.col]
    else:
        return False


def search_right(field):
    if field.col != (board_cols - 1):
        if board[field.row][field.col + 1].is_obstacle == True:
            return False
        elif board[field.row][field.col + 1].is_start == True:
            return False
        elif board[field.row][field.col + 1].is_end == True:
            board[field.row][field.col + 1].was_searched = True
            return board[field.row][field.col + 1]

        if board[field.row][field.col + 1].was_searched == True:
            return False
        else:
            board[field.row][field.col + 1].was_searched = True
            return board[field.row][field.col + 1]
    else:
        return False


def search_left(field):
    if field.col != 0:
        if board[field.row][field.col - 1].is_obstacle == True:
            return False
        elif board[field.row][field.col - 1].is_start == True:
            return False
        elif board[field.row][field.col - 1].is_end == True:
            board[field.row][field.col - 1].was_searched = True
            return board[field.row][field.col - 1]
        else:
            if board[field.row][field.col - 1].was_searched == True:
                return False
            else:
                board[field.row][field.col - 1].was_searched = True
                return board[field.row][field.col - 1]
    else:
        return False


def search_bot(field):
    if field.row != board_rows - 1:
        if board[field.row + 1][field.col].is_obstacle == True:
            return False
        elif board[field.row + 1][field.col].is_start == True:
            return False
        elif board[field.row + 1][field.col].is_end == True:
            board[field.row + 1][field.col].was_searched = True
            return board[field.row + 1][field.col]
        else:
            if board[field.row + 1][field.col].was_searched == True:
                return False
            else:
                board[field.row + 1][field.col].was_searched = True
                return board[field.row + 1][field.col]
    else:
        return False


def get_best_way():
    for x in board:
        for p in x:
            if p.is_end:
                end_field = p

    var_compare = None
    var_final = None
    for x in paths_time:
        for i in x:
            if end_field.row == i.row and end_field.col == i.col:
                var_compare = x
                if var_final == None:
                    var_final = var_compare
                elif len(var_compare) < len(var_final):
                    var_final = var_compare

    print(f"\nBest Way: {var_final}")

    print_best_way(var_final)


def print_best_way(var_final: list):
    move(board_rows + 3)
    for x in var_final:
        board[x.row][x.col].best_way = True
        print_board(board)
        move(board_rows + 1)


def search_graph():

    for x in board:
        for p in x:
            if p.is_start:
                start_field = p

    global paths
    paths.append([start_field])
    i = 0
    cancel = False

    while i < len(paths):

        x = paths[i]

        field_test = search_top(x[-1])
        if type(field_test) != bool:
            if field_test.is_end == True:
                new_list_top = list(x)
                new_list_top.append(field_test)
                paths_time.append(list(new_list_top))
                cancel = True

            new_list_top = list(x)
            new_list_top.append(field_test)
            paths_time.append(list(new_list_top))
            del new_list_top[:]

        field_test = search_right(x[-1])
        if type(field_test) != bool:
            if field_test.is_end == True:
                new_list_right = list(x)
                new_list_right.append(field_test)
                paths_time.append(list(new_list_right))
                cancel = True

            new_list_right = list(x)
            new_list_right.append(field_test)
            paths_time.append(list(new_list_right))
            del new_list_right[:]

        field_test = search_left(x[-1])
        if type(field_test) != bool:
            if field_test.is_end == True:
                new_list_left = list(x)
                new_list_left.append(field_test)
                paths_time.append(list(new_list_left))
                cancel = True

            new_list_left = list(x)
            new_list_left.append(field_test)
            paths_time.append(list(new_list_left))
            del new_list_left[:]

        field_test = search_bot(x[-1])
        if type(field_test) != bool:
            if field_test.is_end == True:
                new_list_bot = list(x)
                new_list_bot.append(field_test)
                paths_time.append(list(new_list_bot))
                cancel = True

            new_list_bot = list(x)
            new_list_bot.append(field_test)
            paths_time.append(list(new_list_bot))
            del new_list_bot[:]

        print_board(board)

        if i == len(paths) - 1:
            global iteration
            with open("paths.txt", "a+") as f:
                f.write(f"Iteration Number: {iteration}\n")
                f.write(f"Length of paths: {len(paths)}\n")
                f.write(f"Lenght of pathtime:{len(paths_time)}\n")
                f.write(f"Paths:{paths}\n")
                f.write(f"Pathstime:{paths_time}\n")

            if cancel == True:
                break

            iteration += 1
            i = 0
            paths_length = len(paths)
            for elem in paths_time:
                paths.append(list(elem))
            del paths[:paths_length]
            del paths_time[:]
            move(board_rows + 1)
        else:
            i += 1
            move(board_rows + 1)


print("\033[0J")
with open("paths.txt", "w") as f:
    f.write("")
create_board(board_rows, board_cols)
define_start_end_obstacles(3, 18)
search_graph()
get_best_way()
