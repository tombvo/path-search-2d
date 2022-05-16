#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Implementation of classes
"""


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

    def equals(self, field: "Field"):
        return True if (self.row == field.row) and (self.col == field.col) else False
