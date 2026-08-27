import click

from bishopviz.charsets import COLORS


class DrunkenBishopAlgorithm:
    def __init__(
        self,
        graph_width: int,
        graph_height: int,
        byte_pairs: list[str],
    ):
        self.graph_width = graph_width
        self.graph_height = graph_height
        self.graph = [
            [0 for _ in range(self.graph_width)] for _ in range(self.graph_height)
        ]

        self.bishop_x = self.graph_width // 2
        self.bishop_y = self.graph_height // 2

        self.byte_pairs = byte_pairs
        self.pair_index = 0

        self.start_point = (self.bishop_x, self.bishop_y)
        self.end_point = (-1, -1)  # placeholder

    def move(self):
        self.bishop_x += 1 if self.byte_pairs[self.pair_index][1] == "1" else -1
        self.bishop_y += 1 if self.byte_pairs[self.pair_index][0] == "1" else -1

        self.bishop_x = max(self.bishop_x, 0)
        self.bishop_y = max(self.bishop_y, 0)
        self.bishop_x = min(self.bishop_x, self.graph_width - 1)
        self.bishop_y = min(self.bishop_y, self.graph_height - 1)

        self.graph[self.bishop_y][self.bishop_x] += 1
        self.pair_index += 1

        if self.pair_index == len(self.byte_pairs):
            self.end_point = (self.bishop_x, self.bishop_y)

    def print_graph(self, charset: dict[int | str, str], show_start: bool = True, show_end: bool = True, show_current_position: bool = False, accomodate_large_chars: bool = False, colorize: bool = False) -> None:
        graph_width = self.graph_width * 2 if accomodate_large_chars else self.graph_width

        print(f"+{'-' * graph_width}+")

        # for row in self.graph:
        #     row_str = ''.join([charset[i] for i in row])
        #     print(f"|{row_str}|")

        for y, row in enumerate(self.graph):
            row_arr = []

            for x, tile in enumerate(row):
                position = (x, y)
                bishop_pos = (self.bishop_x, self.bishop_y)

                if show_end and position == self.end_point:
                    row_arr.append(charset[16])
                elif show_start and position == self.start_point:
                    row_arr.append(charset[15])
                elif show_current_position and position == bishop_pos:
                    row_arr.append(charset["bishop"])
                else:
                    if colorize:
                        row_arr.append(click.style(charset[tile], fg=COLORS[tile]))
                    else:
                        row_arr.append(charset[tile])

            print(f"|{''.join(row_arr)}|")

        print(f"+{'-' * graph_width}+")
