class Problem:
    """
    Represents an instance of the Pizza problem
    """
    max_width = 0
    max_height = 0
    L = 0
    H = 0

    field = None
    _slices_formats = None

    def __init__(self, max_height, max_width, L, H, is_debug=False):
        self.max_height = max_height
        self.max_width = max_width
        self.L = L
        self.H = H
        self.is_debug = is_debug
        self.slices_formats()

        self.field = [[0] * max_width for i in range(max_height)]

    def valid(self, i, j):
        """
        Checks whether the coordinates are valid
        :param i: row
        :param j: column
        :return: True or False
        """
        return i >= 0 and i < self.max_height and j >= 0 and j < self.max_width

    def is_valid_slice(self, upperi, upperj, height, width):
        """
        Checks whether a slice is valid
        :param upperi: upper row of the slice
        :param upperj: leftmost column of the slice
        :param height: slice's height, i.e. the amount of rows in slice
        :param width: slice's width, i.e. the amount of columns in slice
        :return: True if the slice is valid or False otherwise
        """
        # total area of each slice must be at most H
        if height * width > self.H:
            return False

        # correct slice coordinates
        if not self.valid(upperi+height-1, upperj+width-1) or not self.valid(upperi, upperj):
            return False

        # each slice must contain at least L cells of mushroom
        # each slice must contain at least L cells of tomato
        ts, ms = 0, 0
        for i in range(upperi, upperi+height):
            for j in range(upperj, upperj+width):
                if self.field[i][j] == 'T':
                    ts += 1
                elif self.field[i][j] == 'M':
                    ms += 1

        if ts < self.L or ms < self.L:
            return False

        return True

    def slices_formats(self):
        """
        Returns a list of valid slice formats
        :return: list of (h, w), where h - height and w - width of a potential slice
        """
        if not self._slices_formats:
            self._slices_formats = []
            for max_size in range(2*self.L, self.H+1):
                for i in range(1, max_size+1):
                    if max_size % i == 0:
                        self._slices_formats.append((i, max_size // i))
        return self._slices_formats[:]

    def validate_solution(self, slices):
        """
        Validates whether the provided solution (list of slices) is correct (corresponds to the problem statement)
        :param slices: list of rectangular slices;
                    each slice is prepresented by [row, column, height, width], where
                        row is an upper row of the slice
                        column is a leftmost column of the slice
                        height is a slice's height, i.e. the amount of rows in slice
                        width is a slice's width, i.e. the amount of columns in slice
        :return: tuple (a, b):
                    if solution is correct then a == True and b is the solution's score
                    otherwise a == False and b is a list of string error messages
        """

        if self.is_debug:
            print(slices)

        is_correct, error_messages, score = True, [], 0
        free_field = [[(True, -1)] * self.max_width for i in range(self.max_height)]
        overlapped = []
        for slice_idx in range(len(slices)):
            r, c, h, w = slices[slice_idx]
            if not self.valid(r + h - 1, c + w - 1):
                is_correct = False
                error_messages += ["Slice {},{} outbounds pizza size by {},{}".format(r, c, h, w)]
            if h * w > self.H:
                is_correct = False
                error_messages += ["Slice {},{},{},{} outsizes maximum size {}".format(r, c, h, w, self.H)]
            ts, ms = 0, 0
            for xr in range(r, r + h):
                for xc in range(c, c + w):
                    if free_field[xr][xc][0]:
                        free_field[xr][xc] = (False, slice_idx)
                        score += 1
                    else:
                        is_correct = False
                        j = free_field[xr][xc][1]
                        new_overlap = (min(slice_idx, j), max(slice_idx, j))
                        if new_overlap not in overlapped:
                            overlapped.append(new_overlap)
                            error_messages += [
                                "Slice {},{},{},{} overlaps with slice {},{},{},{}".format(r, c, h, w,
                                                                                           slices[j][0], slices[j][1],
                                                                                           slices[j][2], slices[j][3])]
                    if self.field[xr][xc] == 'T':
                        ts += 1
                    if self.field[xr][xc] == 'M':
                        ms += 1
            if ts < self.L:
                is_correct = False
                error_messages += [
                    "Slice {},{},{},{} has not enough tomatoes: {}, but need to have {}".format(r, c, h, w, ts,
                                                                                                self.L)]
            if ms < self.L:
                is_correct = False
                error_messages += [
                    "Slice {},{},{},{} has not enough mushrooms: {}, but need to have {}".format(r, c, h, w, ms,
                                                                                                 self.L)]

        if not is_correct:
            return False, error_messages
        return True, score
