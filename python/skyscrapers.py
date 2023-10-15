#!/usr/bin/env python3.11
""""""
import collections as col
import copy as cp
import dataclasses as dc
import functools as ft
import itertools as it
import operator as op

SkyscraperData = col.namedtuple("SkyscraperData", ["perms", "visible2perms", "visible2constraints"])
Reversible = col.namedtuple("Reversible", ["front", "back"])
Index = col.namedtuple("Index", ["value", "is_row"])
Hint = col.namedtuple("Hint", ["front", "back"])


@dc.dataclass
class SkyscrapersSolver:
    board: tuple
    size: tuple
    hints: dict = dc.field(default_factory=lambda: col.defaultdict(Hint))

    @ft.cache
    def solve(self):
        if self.is_solved():
            return self

        solutions = (child.solve() for child in self.generate_children())
        return next(filter(None, solutions), None)

    @classmethod
    def empty(cls, size, clues):
        out = SkyscrapersSolver(generate_empty_board(size), size)
        clues = list(clues)

        for item in out.iter_indices():
            clue_indices = get_input_clue_from_index(item, size)
            out.hints[item] = Hint(clues[clue_indices[0]], clues[clue_indices[1]])

        out.tighten_constraints_hints()
        out.tighten_constraints_rows_and_cols()
        return out

    def is_solved(self):
        return all(map(row_solved, self.board))

    def generate_children(self) -> iter:
        location = self.choose_location()
        possible_vals = hint_get_possible_vals(self.hints[location], self.size)
        children = (self.try_fill_row(location, value) for value in possible_vals)
        yield from filter(None, children)

    def choose_location(self):
        unsolved_indices = (index for index in self.iter_indices() if not row_solved(self.lookup(index)))
        num_possible_values = lambda index: len(hint_get_possible_vals(self.hints[index], self.size))
        best_option = min(unsolved_indices, key=num_possible_values)
        return best_option

    def try_fill_row(self, row, value):
        current_heights = self.lookup(row)
        any_overwrites = not all(new in current for new, current in zip(value, current_heights))

        if any_overwrites:
            return None

        out = SkyscrapersSolver(self.board, self.size, self.hints)
        out.board = cp.deepcopy(out.board)
        row_constrain_exact(out.lookup(row), value)

        if (out := out.tighten_constraints_rows_and_cols()) is None:
            return None
        if (out := out.tighten_constraints_hints()) is None:
            return None
        return out

    def iter_indices(self):
        for i in range(self.size):
            yield Index(i, False)
            yield Index(i, True)

    def lookup(self, val) -> tuple:
        if val.is_row:
            return self.board[val.value]
        return tuple((i[val.value] for i in self.board))

    def tighten_constraints_hints(self):
        data = generate_skyscraper_data(self.size)

        for location in self.iter_indices():
            value = self.lookup(location)
            hint = self.hints[location]

            if all(map(cell_solved, value)):
                if hint_validates(hint, tuple(next(iter(i)) for i in value)):
                    continue
                return None

            if hint.front:
                row_tighten_constraints(value, data.visible2constraints.front[hint.front])
            if hint.back:
                row_tighten_constraints(value, data.visible2constraints.back[hint.back])

        return self

    def tighten_constraints_rows_and_cols(self):
        determined_indices = it.product(range(self.size), repeat=2)
        determined_indices = filter(lambda coord: len(self.board[coord[1]][coord[0]]) == 1, determined_indices)
        determined_indices = list(determined_indices)

        processed = set()

        while determined_indices:
            coord = determined_indices.pop()
            processed.add(coord)
            x, y = coord

            rook_move = it.chain(((x, yy) for yy in range(self.size)), ((xx, y) for xx in range(self.size)))
            rook_move = filter(lambda x: x != coord, rook_move)

            for other_coord in rook_move:
                o_x, o_y = other_coord
                other_value = self.board[o_y][o_x]
                other_value -= self.board[y][x]

                if not other_value:
                    return None

                if len(other_value) == 1 and other_coord not in processed:
                    determined_indices.append(other_coord)

        return self

    def __hash__(self):
        return hash(str(self.board))


cell_solved = lambda x: len(x) == 1
row_solved = lambda row: all(map(cell_solved, row))
generate_empty_board = lambda size: tuple(tuple(set(range(1, size + 1)) for _ in range(size)) for _ in range(size))
hint_validates = lambda hint, data: not (
    (hint.back and hint.back != n_visible(data[::-1])) or (hint.front and hint.front != n_visible(data))
)


@ft.cache
def hint_get_possible_vals(hint, num):
    n_data = generate_skyscraper_data(num)
    vis2perms = n_data.visible2perms
    return vis2perms.front.get(hint.front, n_data.perms) & vis2perms.back.get(hint.back, n_data.perms)


@ft.cache
def n_visible(heights):
    highest_yet = it.accumulate(heights, max)
    return sum(map(op.eq, highest_yet, heights))


@ft.cache
def generate_skyscraper_data(n):
    perms2visible = {k: n_visible(k) for k in it.permutations(range(1, n + 1))}
    perms = set(perms2visible)

    visible2perms = col.defaultdict(set)
    for k, v in perms2visible.items():
        visible2perms[v].add(k)

    layout_by_visible_reverse = {k: set(i[::-1] for i in v) for k, v in visible2perms.items()}
    transposed_layout = {k: tuple(map(set, zip(*v))) for k, v in visible2perms.items()}
    transposed_layout_reverse = {k: v[::-1] for k, v in transposed_layout.items()}

    return SkyscraperData(
        perms,
        Reversible(visible2perms, layout_by_visible_reverse),
        Reversible(transposed_layout, transposed_layout_reverse),
    )


def get_input_clue_from_index(indexer, n):
    if indexer.is_row:
        return (4 * n - (indexer.value + 1)), (n + indexer.value)
    return indexer.value, (3 * n - (indexer.value + 1))


def row_constrain_exact(left, right):
    for i, j in zip(left, right):
        i.clear()
        i.add(j)


def row_tighten_constraints(left, right):
    for i, j in zip(left, right):
        i &= j


def solve_puzzle(clues):
    solution = SkyscrapersSolver.empty(6, clues).solve().board
    return tuple(tuple(next(iter(i)) for i in tup) for tup in solution)
