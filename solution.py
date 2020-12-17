import hashlib
from copy import deepcopy
import random

from problem import Problem

class Solution:
    """
    Represents a solution of the Pizza problem
    """
    p = None
    slices = None
    free = None
    slice_list = None

    def __init__(self, problem):
        self.p = problem    # type: Problem
        self.slices = [[(0, 0)] * self.p.max_width for i in range(self.p.max_height)]
        self.free = [[True] * self.p.max_width for i in range(self.p.max_height)]
        self.slice_list = []

    def score(self):
        """
        Calculates the score of the solution, i.e. the total number of cells in all slices.
        :return: score value
        """
        score = 0
        for i in range(self.p.max_height):
            score += self.p.max_width - self.free[i].count(True)
        return score

    def is_OK(self):
        """
        Checks whether the solution is valid:
        For the solution to be accepted:
        - the format of the file must match the description above,
        - each cell of the pizza must be included in at most one slice,
        - each slice must contain at least ​ L ​ cells of mushroom,
        - each slice must contain at least ​ L ​ cells of tomato,
        - total area of each slice must be at most ​ H
        :return: True if the solution is valid; otherwise - False and a list of errors
        """
        is_correct, error_messages = self.p.validate_solution(self.get_all_slices())
        if not is_correct:
            return False, error_messages
        return True, "Solution is valid!"

    def print_free(self):
        """
        Prints free and occupied pizza's cells
        """
        print("\n".join(["".join(['_' if self.free[i][j]==True else 'X' for j in range(self.p.max_width)]) for i in
                         range(self.p.max_height)]))

    def _prepare_string(self):
        self.get_all_slices()
        table = [['_'] * self.p.max_width for i in range(self.p.max_height)]
        alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        alphabet_n = len(alphabet)
        k = 0
        for slice in self.slice_list:
            for i in range(slice[0], slice[0] + slice[2]):
                for j in range(slice[1], slice[1] + slice[3]):
                    table[i][j] = alphabet[k]
            k = (k + 1) % alphabet_n
        return table

    def print_solution(self):
        """
        Prints pizza with all slices marked with digits and letters
        """
        table = self._prepare_string()
        print("\n".join(["".join([table[i][j] for j in range(self.p.max_width)]) for i in range(self.p.max_height)]))

    def out(self):
        pass

    def get_hash(self, is_string=False):
        """
        Returns hash value for the solution
        :param is_string: True is you want to have a string hash value
        :return:
        """
        m = hashlib.md5()
        table = self._prepare_string()
        s = "".join(["".join([table[i][j] for j in range(self.p.max_width)]) for i in range(self.p.max_height)])
        m.update(s.encode('utf-8'))
        if is_string:
            return m.hexdigest()
        return m.digest()

    def is_free_space(self, upperi, upperj, height, width):
        """
        Checks whether a space bounded by (upperi, upperj, upperi+height-1, upperj+width-1) is free,
        i.e. does not belong to any slice
        :return: True or False
        """
        if not self.p.valid(upperi, upperj) or not self.p.valid(upperi+height-1, upperj+width-1):
            return False
        for i in range(upperi, upperi+height):
            for j in range(upperj, upperj+width):
                if self.free[i][j] != True:
                    return False
        return True

    def create_new_slice(self, upperi, upperj, height, width):
        """
        Creates a new slice bounded by (upperi, upperj, upperi+height-1, upperj+width-1)
        """
        if not self.p.valid(upperi+height-1, upperj+width-1):
            return
        self.slices[upperi][upperj] = (height, width)
        for i in range(upperi, upperi+height):
            for j in range(upperj, upperj+width):
                # self.free[i][j] = False
                self.free[i][j] = (upperi, upperj)

    def get_all_slices(self):
        """
        :return: a list of all slices
        """
        self.slice_list = []
        for i in range(self.p.max_height):
            for j in range(self.p.max_width):
                if self.slices[i][j] != (0, 0):
                    self.slice_list.append((i,j) + self.slices[i][j])
        return self.slice_list

    def load_slices(self, slices):
        """
        Load solution instance from the list of slices.
        Each slice each slice is represented by [row, column, height, width], where
                        row is an upper row of the slice
                        column is a leftmost column of the slice
                        height is a slice's height, i.e. the amount of rows in slice
                        width is a slice's width, i.e. the amount of columns in slice
        :return: N/A
        """
        self.slices = [[(0, 0)] * self.p.max_width for i in range(self.p.max_height)]
        self.free = [[True] * self.p.max_width for i in range(self.p.max_height)]
        for slice in slices:
            self.create_new_slice(slice[0], slice[1], slice[2], slice[3])

    def pick_random_slice(self):
        """
        :return: a random slice
        """
        if not self.slice_list:
            self.get_all_slices()
        return self.slice_list[random.randint(0,len(self.slice_list)-1)]

    def duplicate(self):
        """
        Duplicates the solution
        :return: a new solution that is equal to the current solution
        """
        s = Solution(self.p)
        s.slices = deepcopy(self.slices)
        s.slice_list = deepcopy(self.slice_list)
        s.free = deepcopy(self.free)
        return s

    def get_overlaps(self, upperi, upperj, height, width):
        """
        Returns a list of the slices that overlap with a box bounded by (upperi, upperj, upperi+height-1, upperj+width-1)
        Also returns a list of overlapped pizza pieces (cells)
        :param upperi:
        :param upperj:
        :param height:
        :param width:
        :return:
        """
        overlapped_slices = set()
        overlapped_pieces = []
        for i in range(upperi, upperi + height):
            if i>=self.p.max_height:
                break
            for j in range(upperj, upperj + width):
                if j>=self.p.max_width:
                    break
                if self.free[i][j] != True:
                    overlapped_pieces += [(i,j)]
                    overlapped_slices.add(self.free[i][j])
        return overlapped_slices, overlapped_pieces

    def delete_slice(self, upperi, upperj):
        """
        Deletes the slice defined by the upper-left coordinate upperi, upperj
        """
        h, w = self.slices[upperi][upperj]
        if (h, w) == (0, 0):
            return
        for i in range(upperi, upperi + h):
            for j in range(upperj, upperj + w):
                self.free[i][j] = True
        self.slices[upperi][upperj] = (0, 0)

