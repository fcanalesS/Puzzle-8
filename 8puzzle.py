_goal_state = [[1, 2, 3],
               [4, 5, 6],
               [7, 8, 0]]


def index(item, seq):
    if item in seq:
        return seq.index(item)
    else:
        return -1


class EightPuzzle:
    def __init__(self):
        self._hval = 0
        self._depth = 0
        self._parent = None
        self.adj_matrix = []
        for i in range(3):
            self.adj_matrix.append(_goal_state[i][:])

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.adj_matrix == other.adj_matrix

    def __str__(self):
        res = ''
        for row in range(3):
            res += ' '.join(map(str, self.adj_matrix[row]))
            res += '\r\n'
        return res

    def _clone(self):
        p = EightPuzzle()
        for i in range(3):
            p.adj_matrix[i] = self.adj_matrix[i][:]
        return p

    def _get_legal_moves(self):
        """Retorna una lista de tuplas, que pueden darse con el espacio en blanco"""
        # esto obtiene la fila y columna del espacio en blanco
        row, col = self.find(0)
        free = []

        # Y encuentra cuales piezas pueden moverse
        if row > 0:
            free.append((row - 1, col))
        if col > 0:
            free.append((row, col - 1))
        if row < 2:
            free.append((row + 1, col))
        if col < 2:
            free.append((row, col + 1))

        return free

    def _generate_moves(self):
        free = self._get_legal_moves()
        zero = self.find(0)

        def swap_and_clone(a, b):
            p = self._clone()
            p.swap(a, b)
            p._depth = self._depth + 1
            p._parent = self
            print p  #Imprime TODAS las combinaciones, en base a una entrada dada
            return p

        return map(lambda pair: swap_and_clone(zero, pair), free)

    def _generate_solution_path(self, path):
        if self._parent == None:
            return path
        else:
            path.append(self)
            return self._parent._generate_solution_path(path)


    def solve(self, h):

        def is_solved(puzzle):
            return puzzle.adj_matrix == _goal_state

        openl = [self]
        closedl = []
        move_count = 0
        while len(openl) > 0:
            x = openl.pop(0)
            print x
            move_count += 1
            if (is_solved(x)):
                if len(closedl) > 0:
                    return x._generate_solution_path([]), move_count
                else:
                    return [x]

            succ = x._generate_moves()
            idx_open = idx_closed = -1

            for move in succ:
                idx_open = index(move, openl)
                idx_closed = index(move, closedl)
                hval = h(move)
                fval = hval + move._depth

                if idx_closed == -1 and idx_open == -1:
                    move._hval = hval
                    openl.append(move)
                elif idx_open > -1:
                    copy = openl[idx_open]
                    if fval < copy._hval + copy._depth:
                        copy._hval = hval
                        copy._parent = move._parent
                        copy._depth = move._depth
                elif idx_closed > -1:
                    copy = closedl[idx_closed]
                    if fval < copy._hval + copy._depth:
                        move._hval = hval
                        closedl.remove(copy)
                        openl.append(move)

            closedl.append(x)
            openl = sorted(openl, key=lambda p: p._hval + p._depth)

        return [], 0

    def find(self, value):
        if value < 0 or value > 8:
            raise Exception("Valor fuera de rango")

        for row in range(3):
            for col in range(3):
                if self.adj_matrix[row][col] == value:
                    return row, col

    def peek(self, row, col):
        """retorna el valor de la fila y columna especificada"""
        return self.adj_matrix[row][col]

    def poke(self, row, col, value):
        """setea el valor de la fila y columna especificada"""
        self.adj_matrix[row][col] = value

    def swap(self, pos_a, pos_b):
        """cambia 'swap' los valores que son contenidos por laas coordenadas especificadas"""
        temp = self.peek(*pos_a)
        self.poke(pos_a[0], pos_a[1], self.peek(*pos_b))
        self.poke(pos_b[0], pos_b[1], temp)

    def set(self, other): #seteo de los valores para el puzzle 8
        i = 0
        for row in range(3):
            for col in range(3):
                self.adj_matrix[row][col] = int(other[i])
                i += 1


def h_default(puzzle): # Valor de heuristica, por ahora es 0
    return 0


def main():
    p = EightPuzzle() #Instancia de la clase
    """Valores de entrada para la clase EightPuzzle()
        Probar con esta configuracion, sino se va todo al carajo =D"""
    p.set("123456708")
    print p

    path, count = p.solve(h_default)
    path.reverse()
    for i in path:
        print i

if __name__ == "__main__":
    main()
