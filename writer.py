from solution import Solution

class Writer:

    def write(self, solution):
        """
        :param solution: Solution to be written
         @type solution: Solution
        :return:
        """
        raise Exception("Need to implement 'write' method")

class ConsoleWriter(Writer):

    def write(self, solution):
        """
        :param solution: Solution to be written
         @type solution: Solution
        :return:
        """
        solution.get_all_slices()
        print("{}".format(len(solution.slice_list)))
        for slice in solution.slice_list:
            print("{} {} {} {}".format(slice[0], slice[1], slice[0]+slice[2]-1, slice[1]+slice[3]-1))

class FileWriter(Writer):

    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, solution):
        """
        :param solution: Solution to be written
         @type solution: Solution
        :return:
        """
        f = open(self.file_name, 'w')
        solution.get_all_slices()
        f.write("{}\n".format(len(solution.slice_list)))
        for slice in solution.slice_list:
            f.write("{} {} {} {}\n".format(slice[0], slice[1], slice[0]+slice[2]-1, slice[1]+slice[3]-1))
        f.close()