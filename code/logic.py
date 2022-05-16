#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Implementation of 2d_path_search
"""
import colorama
from random import randint
from rich import print
from classes import Field


colorama.init()  # On Windows, will filter ANSI escape sequences out of any text sent to stdout or stderr, and replace them with equivalent Win32 calls.

# Globals
board = []
paths = []
paths_second = []

board_rows: int
board_cols: int

start_field: Field
end_field: Field

iteration = 0


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


def define_start_end_obstacles(start_field: Field, end_field: Field):
    board[start_field.row][end_field.row].is_start = True  # decides starting point
    board[end_field.row][end_field.col].is_end = True  # decides ending point

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
    for x in paths_second:
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
                paths_second.append(list(new_list_top))
                cancel = True

            new_list_top = list(x)
            new_list_top.append(field_test)
            paths_second.append(list(new_list_top))
            del new_list_top[:]

        field_test = search_right(x[-1])
        if type(field_test) != bool:
            if field_test.is_end == True:
                new_list_right = list(x)
                new_list_right.append(field_test)
                paths_second.append(list(new_list_right))
                cancel = True

            new_list_right = list(x)
            new_list_right.append(field_test)
            paths_second.append(list(new_list_right))
            del new_list_right[:]

        field_test = search_left(x[-1])
        if type(field_test) != bool:
            if field_test.is_end == True:
                new_list_left = list(x)
                new_list_left.append(field_test)
                paths_second.append(list(new_list_left))
                cancel = True

            new_list_left = list(x)
            new_list_left.append(field_test)
            paths_second.append(list(new_list_left))
            del new_list_left[:]

        field_test = search_bot(x[-1])
        if type(field_test) != bool:
            if field_test.is_end == True:
                new_list_bot = list(x)
                new_list_bot.append(field_test)
                paths_second.append(list(new_list_bot))
                cancel = True

            new_list_bot = list(x)
            new_list_bot.append(field_test)
            paths_second.append(list(new_list_bot))
            del new_list_bot[:]

        print_board(board)

        if i == len(paths) - 1:
            global iteration
            with open("paths.txt", "a+") as f:
                f.write(f"Iteration Number: {iteration}\n")
                f.write(f"Length of paths: {len(paths)}\n")
                f.write(f"Lenght of pathtime:{len(paths_second)}\n")
                f.write(f"Paths:{paths}\n")
                f.write(f"Pathstime:{paths_second}\n")

            if cancel == True:
                break

            iteration += 1
            i = 0
            paths_length = len(paths)
            for elem in paths_second:
                paths.append(list(elem))
            del paths[:paths_length]
            del paths_second[:]
            move(board_rows + 1)
        else:
            i += 1
            move(board_rows + 1)


def ask_user_start_end():

    global start_field
    global end_field

    starting_point_row: int
    starting_point_col: int

    ending_point_row: int
    ending_point_col: int

    print("Now, please choose the starting point: ")
    while True:
        while True:
            try:
                starting_point_row = int(input("Row: "))
                if starting_point_row < 0 or starting_point_row > board_rows:
                    print(f"Sorry, number has to be in the range from 0-{board_rows}!")
                    continue
            except ValueError:
                print("[red]Make sure you enter a correct, positive Number for rows.")
                continue
            break

        while True:
            try:
                starting_point_col = int(input("Col: "))
                if starting_point_col < 0 or starting_point_col > board_cols:
                    print(f"Sorry, number has to be in the range from 0-{board_cols}!")
                    continue
            except ValueError:
                print(
                    "[red]Make sure you enter a correct, positive Number for columns."
                )
                continue
            break

        start_field = Field(starting_point_row, starting_point_col)

        print("Now, please choose the ending point: ")
        while True:
            try:
                ending_point_row = int(input("Row: "))
                if ending_point_row < 0 or ending_point_row > board_rows:
                    print(f"Sorry, number has to be in the range from 0-{board_rows}!")
                    continue
            except ValueError:
                print("[red]Make sure you enter a correct, positive Number for rows.")
                continue
            break

        while True:
            try:
                ending_point_col = int(input("Col: "))
                if ending_point_col < 0 or ending_point_col > board_cols:
                    print(f"Sorry, number has to be in the range from 0-{board_cols}!")
                    continue
            except ValueError:
                print(
                    "[red]Make sure you enter a correct, positive Number for columns."
                )
                continue
            break

        end_field = Field(ending_point_row, ending_point_col)

        if start_field.equals(end_field):
            print(
                "[red]Ending point cannot equal Starting point's coordinates!\nStart all over again!"
            )
        else:
            break


def ask_user_board_size():
    print("\033[0J")  # erase from cursor until end of screen
    print(
        "Hello, this is a 2d-search-path visualization in the terminal.\n You can now decide the size of the board."
    )
    rows: str
    cols: str

    while True:
        try:
            rows = int(input("Rows: "))
        except ValueError:
            print("[red]Make sure you enter a correct, positive Number for rows.")
            continue
        break

    while True:
        try:
            cols = int(input("Columns: "))
        except ValueError:
            print("[red]Make sure you enter a correct, positive number for columns.")
            continue
        break

    global board_rows
    global board_cols

    board_rows = rows
    board_cols = cols


def main():
    ask_user_board_size()
    ask_user_start_end()
    create_board(board_rows, board_cols)
    define_start_end_obstacles(start_field, end_field)
    search_graph()
    get_best_way()
