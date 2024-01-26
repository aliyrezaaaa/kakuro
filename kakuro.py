import copy
import pickle


class Cell:

    def __init__(self, black_box, row_sum, column_sum):
        self.black_box = black_box
        self.row_sum = row_sum
        self.column_sum = column_sum
        self.number = 0


def initialize_puzzle(path):
    puzzle = []
    num_rows = int(input())
    num_columns = int(input())
    for i in range(num_rows):
        row = []
        for j in range(num_columns):
            black_box = int(input())
            row_sum = -1
            column_sum = -1
            if black_box == 1:
                row_sum = int(input())
                column_sum = int(input())
            row.append(Cell(black_box, row_sum, column_sum))
        puzzle.append(row)

    with open(path, "wb") as file:
        pickle.dump(puzzle, file)
        file.close()


def print_puzzle(p):
    num_rows = len(p)
    num_columns = len(p[0])
    for i in range(num_rows):
        for j in range(num_columns):
            cell = p[i][j]
            if cell.black_box == 1:
                print(cell.column_sum, cell.row_sum)
            else:
                print("number", cell.number)


def complete(assigment):
    num_rows = len(assigment)
    num_columns = len(assigment[0])
    for i in range(num_rows):
        for j in range(num_columns):
            cell = assigment[i][j]
            if cell.black_box == 0:
                if cell.number == 0:
                    return False
    return True


def mrv(variable, csp):
    # return -1
    return len(csp[variable[0]][variable[1]])


def select_variable(assignment, csp):
    selected_variable = None
    least_mrv = 10
    num_rows = len(assignment)
    num_columns = len(assignment[0])

    for i in range(num_rows):
        for j in range(num_columns):
            cell = assignment[i][j]

            if cell.black_box == 0:
                if cell.number == 0:

                    minimum_remaining_value = mrv([i, j], csp)
                    if minimum_remaining_value < least_mrv:
                        least_mrv = minimum_remaining_value
                        selected_variable = [i, j]

    return selected_variable


def update_domain(variable, assignment, csp):
    row = variable[0]
    column = variable[1]

    row_sum = 0
    column_sum = 0
    min_row_sum = 0
    max_row_sum = 0
    min_column_sum = 0
    max_column_sum = 0

    for i in range(column):
        cell_column = column - i - 1
        cell = assignment[row][cell_column]
        if cell.black_box == 1:
            row_sum += cell.row_sum
            max_row_sum += cell.row_sum
            min_row_sum += cell.row_sum
        else:
            value = cell.number
            if value != 0:
                row_sum -= value
                max_row_sum -= value
                min_row_sum -= value
                if value in csp[row][column]:
                    csp[row][column].remove(value)
            else:
                max_row_sum -= 1
                min_row_sum -= 9

    for i in range(row):
        cell_row = row - i - 1
        cell = assignment[cell_row][column]
        if cell.black_box == 1:
            column_sum += cell.column_sum
            max_column_sum += cell.column_sum
            min_column_sum += cell.column_sum
        else:
            value = cell.number
            if value != 0:
                column_sum -= value
                max_column_sum -= value
                min_column_sum -= value
                if value in csp[row][column]:
                    csp[row][column].remove(value)
            else:
                max_column_sum -= 1
                min_column_sum -= 9

    max_domain = 0
    if max_row_sum > max_column_sum:
        max_domain = max_row_sum
    else:
        max_domain = max_column_sum

    min_domain = 0
    if min_column_sum < min_row_sum:
        min_domain = min_column_sum
    else:
        min_domain = min_row_sum

    if min_domain < 1:
        min_domain = 1
    if max_domain > 9:
        max_domain = 9
    if min_domain > 9:
        return False
    if max_domain < 0:
        return False

    csp_new = []
    for i in range(min_domain, max_domain + 1):
        if i in csp[row][column]:
            csp_new.append(i)
    if len(csp_new) == 0:
        return False
    csp[row][column] = csp_new
    return True


def initialize_csp(assignment):
    csp = []
    num_rows = len(assignment)
    num_columns = len(assignment[0])
    for i in range(num_rows):
        row = []
        for j in range(num_columns):
            row.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
        csp.append(row)

    for i in range(num_rows):
        for j in range(num_columns):
            ret = update_domain([i, j], assignment, csp)
            if not ret:
                return None

    return csp


def lcv(variable, value, assignment, csp):

    return -1


def order_values(variable, assignment, csp):
    return csp[variable[0]][variable[1]]


def inference(variable, assigment, csp):
    num_rows = len(assigment)
    num_columns = len(assigment[0])

    for i in range(num_rows):
        if i != variable[0]:
            ret = update_domain([i, variable[1]], assigment, csp)
            if not ret:
                return False

    for i in range(num_columns):
        if i != variable[1]:
            ret = update_domain([variable[0], i], assigment, csp)
            if not ret:
                return False

    return True


def back_track(assignment, csp):

    if complete(assignment):
        return assignment

    variable = select_variable(assignment, csp)
    for value in order_values(variable, assignment, csp):

        assignment_copy = copy.deepcopy(assignment)
        csp_copy = copy.deepcopy(csp)

        assignment_copy[variable[0]][variable[1]].number = value
        successful = inference(variable, assignment_copy, csp_copy)
        if successful:
            result = back_track(assignment_copy, csp_copy)
            if result is not None:
                return result

    return None


if __name__ == "__main__":
    # initialize_puzzle()
    with open("puzzle.bin", "rb") as f:
        kakuro = pickle.load(f)
        f.close()
    csp = initialize_csp(kakuro)
    back_track(kakuro, csp)
