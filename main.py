from reader import FileReader
from writer import FileWriter
from solution import Solution
from task_07 import Pizza

from optparse import OptionParser

DEBUG = False

def scenario_A(file_in, file_out=None):
    print("Input file: {}".format(file_in))

    reader = FileReader(file_in)
    problem = reader.read()

    solver = Pizza(problem)
    print("Description:")
    print(solver.description())

    slices = solver.solve()

    is_valid, result = problem.validate_solution(slices)

    if is_valid:
        print("Solution for problem {} is correct. Score is {}".format(file_in, result))
        solution = Solution(problem)
        solution.load_slices(slices)
        if DEBUG:
            solution.print_solution()
        if file_out:
            writer = FileWriter(file_in + ".out")
            writer.write(solution)
    else:
        print("Incorrect solution. Please check the error messages below")
        for msg in result:
            print(msg)


if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("-i", "--input-file", dest="in_file", help="Input file name", metavar="FILE")
    parser.add_option("-o", "--output-file", dest="out_file", help="Output file name", metavar="FILE")
    parser.add_option("-d", "--debug", action="store_true", help="Debug mode ON", default=False)
    (options, args) = parser.parse_args()

    DEBUG = options.debug
    scenario_A("example.in")
