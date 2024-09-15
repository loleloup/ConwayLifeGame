from random import randint


class ConwayTable:
    def __init__(self, width, height):
        self.table = [[False for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height

    def display(self):
        for i in range(self.height):
            print(self.table[i])

    def update(self):
        new_table = [[False for _ in range(self.width)] for _ in range(self.height)]

        for i in range(self.height):
            for j in range(self.width):
                neighbours_count = self._adjacent_count(i, j)
                if (
                    neighbours_count == 2 and self.table[i][j]
                ) or neighbours_count == 3:
                    new_table[i][j] = True

        self.table = new_table

    def _adjacent_count(self, i, j):
        count = 0
        for v in range(3):
            for h in range(3):
                if (
                    0 <= i - 1 + v < self.height
                    and 0 <= j - 1 + h < self.width
                    and self.table[i - 1 + v][j - 1 + h]
                ):
                    count += 1
        if self.table[i][j]:
            count -= 1
        return count

    def save(self, path):
        with open(path, "w") as file:
            file.write(str(self.height) + "," + str(self.width) + "\n")
            for i in range(self.height):
                for j in range(self.width):
                    file.write(str(int(self.table[i][j])))

    def load(self, file):
        line = file.readline()
        i = 0
        j = 0
        for char in line:
            if int(char):
                self.table[i][j] = True
            j += 1
            if j == self.width:
                j = 0
                i += 1

    def randomize(self, rate):
        for i in range(self.height):
            for j in range(self.width):
                rand = randint(0, 100)
                if rand < rate:
                    self.table[i][j] = True
