from problem import Problem

class Reader:
    def __init__(self):
        pass

    def read(self):
        raise Exception("Need to implement 'read' method")

class ConsoleReader(Reader):
    def read(self):
        n, m, l, h = map(int, input().split())
        p = Problem(n, m, l, h)
        for i in range(n):
            row = input()
            for j in range(m):
                p.field[i][j] = row[j]
        return p

class FileReader(ConsoleReader):
    def __init__(self, file_name):
        ConsoleReader.__init__(self)
        self.file_name = file_name

    def read(self):
        with open(self.file_name,'r') as f:
            n, m, l, h = map(int, f.readline().split())
            p = Problem(n, m, l, h)
            for i in range(n):
                row = f.readline()
                for j in range(m):
                    p.field[i][j] = row[j]
            f.close()
        return p

