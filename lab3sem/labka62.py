import math
from copy import deepcopy
from Graph import Graph


def fill_list(size, item):
    return [item] * size


class Hungarian:
    def __init__(self, matrix):
        self.start_matrix = matrix
        self.matrix = deepcopy(matrix)

        self.selected_zero_in_row = fill_list(len(self.matrix), -1)
        self.selected_zero_in_col = fill_list(len(self.matrix[0]), -1)

        self.row_is_covered = fill_list(len(self.matrix), 0)
        self.col_is_covered = fill_list(len(self.matrix[0]), 0)
        self.alternative_zeroes_in_row = fill_list(len(self.matrix), -1)

    def get_optimal_value(self, optimal_assignment=None):
        result = 0
        if optimal_assignment is None:
            optimal_assignment = self.find_optimal_assignment()
        for cell in optimal_assignment:
            result += self.start_matrix[cell[0]][cell[1]]
        return result, optimal_assignment

    def find_optimal_assignment(self):
        self._reduce_matrix()
        # [print(row) for row in self.matrix]
        self._mark_unique_zeroes()
        self._cover_columns_with_marked_zero()

        while not self._are_all_columns_covered():
            print('Зачеркнул:', sum(self.row_is_covered))
            main_zero = self._get_first_uncovered_zero_position()
            while main_zero is None:
                self._use_smallest_uncovered_value()
                main_zero = self._get_first_uncovered_zero_position()

            if self.selected_zero_in_row[main_zero[0]] == -1:
                # в строке main_zero нет отметки
                self._apply_alternative_zeroes(main_zero)
                self._cover_columns_with_marked_zero()
            else:
                # в строке main_zero есть отметка
                self.row_is_covered[main_zero[0]] = 1  # покрываем строку main_zero
                self.col_is_covered[self.selected_zero_in_row[main_zero[0]]] = 0  # не покрываем столбец main_zero
                self._use_smallest_uncovered_value()
        print("-------")
        print("Оптимальное решение найдено!")
        optimal_assignment = []
        for i in range(len(self.selected_zero_in_col)):
            optimal_assignment.append([i, self.selected_zero_in_col[i]])

        return optimal_assignment

    def _are_all_columns_covered(self):
        for i in self.col_is_covered:
            if i == 0:
                return False
        return True

    # Подготовка матрицы к использованию в алгоритме
    def _reduce_matrix(self):
        # Поиск максимального числа в строке
        for i in range(len(self.matrix)):
            row_max = max(self.matrix[i])
            for j in range(len(self.matrix[i])):
                self.matrix[i][j] = - (self.matrix[i][j] - row_max)

        # Поиск минимального числа в строке
        for i in range(len(self.matrix)):
            row_min = min(self.matrix[i])
            if row_min != 0:
                for k in range(len(self.matrix[i])):
                    self.matrix[i][k] -= row_min

        # Поиск минимального столбца в матрице
        for j in range(len(self.matrix[0])):
            col_min = min([x[j] for x in self.matrix])
            if col_min != 0:
                for k in range(len(self.matrix)):
                    self.matrix[k][j] -= col_min

    def _mark_unique_zeroes_in_row(self, row_index, row_has_square, col_has_square):
        for j in range(len(self.matrix[row_index])):
            if self.matrix[row_index][j] == 0 and row_has_square[row_index] == 0 and col_has_square[j] == 0:
                row_has_square[row_index] = 1
                col_has_square[j] = 1
                self.selected_zero_in_row[row_index] = j  # save the row-position of the zero
                self.selected_zero_in_col[j] = row_index  # save the column-position of the zero
                return

    def _mark_unique_zeroes(self):
        row_has_square = fill_list(len(self.matrix), 0)
        col_has_square = fill_list(len(self.matrix[0]), 0)

        for i in range(len(self.matrix)):
            self._mark_unique_zeroes_in_row(i, row_has_square, col_has_square)

    def _cover_columns_with_marked_zero(self):
        for i in range(len(self.selected_zero_in_col)):
            if self.selected_zero_in_col[i] != -1:
                self.col_is_covered[i] = 1
            else:
                self.col_is_covered[i] = 0

    def _get_smallest_uncovered_value(self):
        min_value = math.inf
        for i in range(len(self.matrix)):
            if self.row_is_covered[i] == 1:
                continue
            for j in range(len(self.matrix[0])):
                if self.col_is_covered[j] == 0 and self.matrix[i][j] < min_value:
                    min_value = self.matrix[i][j]
        return min_value

    def _use_smallest_uncovered_value(self):
        min_uncovered_value = self._get_smallest_uncovered_value()
        if min_uncovered_value <= 0:
            return

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.row_is_covered[i] == 1 and self.col_is_covered[j] == 1:
                    # Add min to all twice-covered values
                    self.matrix[i][j] += min_uncovered_value
                elif self.row_is_covered[i] == 0 and self.col_is_covered[j] == 0:
                    # Subtract min from all uncovered values
                    self.matrix[i][j] -= min_uncovered_value

    def _get_first_uncovered_zero_position(self):
        for i in range(len(self.matrix)):
            if self.row_is_covered[i] == 0:
                for j in range(len(self.matrix[i])):
                    if self.matrix[i][j] == 0 and self.col_is_covered[j] == 0:
                        self.alternative_zeroes_in_row[i] = j  # mark as 0*
                        return [i, j]
        return None

    def _apply_alternative_zeroes(self, main_zero):
        i = main_zero[0]
        j = main_zero[1]

        K = [main_zero]
        while True:
            if self.selected_zero_in_col[j] != -1:
                K.append([self.selected_zero_in_col[j], j])
            else:
                break

            i = self.selected_zero_in_col[j]
            j = self.alternative_zeroes_in_row[i]
            # add the new Z_0 to K
            if j != -1:
                K.append([i, j])
            else:
                break

        for zero in K:  # replace selected zeros to alternative
            if self.selected_zero_in_col[zero[1]] == zero[0]:
                self.selected_zero_in_col[zero[1]] = -1
                self.selected_zero_in_row[zero[0]] = -1

            if self.alternative_zeroes_in_row[zero[0]] == zero[1]:
                self.selected_zero_in_row[zero[0]] = zero[1]
                self.selected_zero_in_col[zero[1]] = zero[0]

        self._remove_all_marks()

    def _remove_all_marks(self):
        self.alternative_zeroes_in_row = fill_list(len(self.alternative_zeroes_in_row), -1)
        self.row_is_covered = fill_list(len(self.row_is_covered), 0)
        self.col_is_covered = fill_list(len(self.col_is_covered), 0)


if __name__ == '__main__':
    graph = Graph(vert=100, avgEdges=40, type='matrix')
    matrix = graph.get_graph()
    print("-------")
    hung = Hungarian(matrix)
    optimal_value, optimal_assignment = hung.get_optimal_value()
    print("-------")
    print("Связи между вершинами в разных долях:")
    # (v1,v2), где v1 - вершина в первой доле, v2 - вершина во второй доле;
    for el in optimal_assignment:
        print(el)
    print("\nРезультат максимального паросочетания: ", optimal_value)
