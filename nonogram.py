from copy import deepcopy

class Constraint:
    def __init__(self, board, is_row, index, limits):
        self.board = board
        self.is_row = is_row
        self.index = index
        self.limits = limits
        self.is_done = False

    def get_points(self):
        points = 0
        for limit in self.limits:
            points += limit + 1

        if self.is_row:
            for col in range(size):
                if self.board[self.index][col] != 'x':
                    points += 1
        else:
            for row in range(size):
                if self.board[row][self.index] != 'x':
                    points += 1

        points = points // len(self.limits)

        return points

    def find_sols(self):
        init_row = []
        if self.is_row:
            init_row = self.board[self.index]
        else:
            for row in range(size):
                init_row.append(self.board[row][self.index])

        # IS IT A SOLUTION ALREADY?
        build = []
        prev_was_one = False
        for elem in init_row:
            if elem == '1':
                if prev_was_one:
                    build[-1] += 1
                else:
                    build.append(1)
                prev_was_one = True
            else:
                prev_was_one = False

        # Yes, there is a solution already
        if build == self.limits:
            for yolo in range(size):
                if init_row[yolo] != '1':
                    if self.is_row:
                        self.board[self.index][yolo] = 'x'
                    else:
                        self.board[yolo][self.index] = 'x'
            self.is_done = True
            return True

        sols = self.find_sols_inner(init_row, self.limits, 0)

        if len(sols) == 0:
            return False

        if len(sols) == '1':
            self.is_done = True

        for iz in range(size):
            is_same = True
            first_item = sols[0][iz]

            for sol in sols:
                if sol[iz] != first_item:
                    is_same = False
                    break

            if is_same:
                if self.is_row:
                    self.board[self.index][iz] = first_item
                else:
                    self.board[iz][self.index] = first_item

        return True

    def find_sols_inner(self, init_row, limits, lim_index):

        if not limits:

            build = []
            prev_was_one = False
            for elem in init_row:
                if elem == '1':
                    if prev_was_one:
                        build[-1] += 1
                    else:
                        build.append(1)
                    prev_was_one = True
                else:
                    prev_was_one = False

            if build != self.limits:
                return []

            for ie in range(size):
                if init_row[ie] is not '1':
                    init_row[ie] = 'x'
            return [init_row]

        diz = limits[0]

        sols = []

        if size - diz >= lim_index:
            for i in range(lim_index, size - diz + 1):

                valid = True

                if i + diz < size and init_row[i + diz] == '1':
                    valid = False

                # Is the current placement overlapping an x?
                for j in range(diz):
                    if init_row[i + j] == 'x':
                        valid = False
                        break

                if valid:

                    temp = init_row.copy()
                    for j in range(diz):
                        temp[i + j] = '1'
                    rest = self.find_sols_inner(temp, limits[1:], i + diz + 1)

                    for oz in rest:
                        sols.append(oz)

        return sols

def generate_start_board():
    board = []
    for y in range(size):
        row = []
        for x in range(size):
            row.append(0)
        board.append(row)
    return board


def print_board(board):
    cy = 0
    print(' ', end=' ')
    for ik in range(size):
        if ik > 9:
            print(ik, end='')
        else:
            print(ik, end=' ')
    print('')
    for row in range(size):
        if cy > 9:
            print(cy, end='')
        else:
            print(cy, end=' ')
        for col in range(size):
            if board[row][col] == '1':
                print(u"\u25A0", end=' ')
            elif board[row][col] == 'x':
                print('x', end=' ')
            else:
                print(' ', end=' ')
        print('')
        cy += 1


def node(board):

    global constraints
    global mut_count
    global tocker

    while len(constraints) > 0:

        constraints = sorted(constraints, key=lambda obj: obj.get_points(), reverse=True)

        prev_board = deepcopy(board)

        for con in constraints:
            if con.get_points() > tocker:
                con.board = board
                found = con.find_sols()
                if not found:
                    return False

        for con in constraints:
            if con.is_done:
                constraints.remove(con)

        if board == prev_board:
            if tocker > 0:
                tocker -= 1
            else:
                missing = False
                for y in range(size):
                    for x in range(size):
                        if board[y][x] == 0:
                            missing = True
                            mod_board = deepcopy(board)
                            mod_board[y][x] = '1'

                            mut_count += 1
                            print('')
                            print('')
                            print('MUTATE')
                            print('')
                            print('')
                            ans = node(mod_board)
                            if ans is not False:
                                return ans
                mut_count -= 1
                if not missing:
                    return board
                else:
                    return False

        print_board(board)
        print('-------------')

    return board

row_cons = [
    [4,2],
    [4,2],
    [4,4,4],
    [3,3,4,1],
    [1,3,2,2],

    [1,4,2,5],
    [1,2,2,7],
    [2,2,2,4],
    [1,3,5,3],
    [3,2,1,1],

    [2,3,2],
    [2,4,1],
    [2,4,1,3],
    [2,6,1,1],
    [1,6,2,1,1],

    [9,1,1,5],
    [7,1,3,1],
    [6,1],
    [1,1],
    [1,1],

    [2,2],
    [3,3],
    [3,2,2,2,3],
    [1,1,1,4,4],
    [2,1,9,8],
]

col_cons = [
    [3,1],
    [2,2,2],
    [2,2,1],
    [2,3,3],
    [8,3,1],

    [2,1,1,4,1],
    [2,1,2,5,1,1],
    [2,2,1,6,4],
    [2,1,1,4,1,1,2],
    [2,1,1,3,2,2,2],

    [2,2,1,4,4,2],
    [1,1,1,2,4,1],
    [1,2,1,4,1,1,1],
    [1,1,2,3,1,1],
    [1,2,1,2,1],

    [3,1,1,6,1],
    [2,1,2,1,3,1],
    [2,3,1,1,1],
    [1,1,1,1,1,2,1],
    [1,1,1,1,2,3],

    [1,4,4,3],
    [1,5,2],
    [1,4,2],
    [1,4,1],
    [5],
]

mut_count = 0
size = 25
constraints = []
start_board = generate_start_board()

tocker = 0

for i in range(size):
    constraints.append(Constraint(start_board, True, i, row_cons[i]))

for i in range(size):
    constraints.append(Constraint(start_board, False, i, col_cons[i]))

for con in constraints:
    print(str(con.index) + ' - ' + str(con.get_points()))

final_board = node(start_board)

if final_board:
    print_board(final_board)
else:
    print('Could not resolve puzzle')



