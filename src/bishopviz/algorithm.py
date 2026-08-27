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

    def print_graph(self, draw_axis: bool, charset: dict[int, str]) -> None:
        padding = 0
        padding_str = ' ' * padding

        if draw_axis:
            padding = 1
            padding_str = ' ' * padding
            top_num_padding = 2

            if self.graph_width >= 10:
                spaces_str = ' ' * (11 + padding)
                nums_str = ''.join([str(i)[0] for i in range(10, self.graph_width)])
                print(spaces_str + nums_str)

            nums_str = ''.join([str(i)[-1] for i in range(self.graph_width)])
            print(f"{' ' * top_num_padding}{nums_str}")

        print(f"{padding_str}+{'-' * self.graph_width}+")

        for y, row in enumerate(self.graph):
            padding = y if draw_axis else padding_str
            row_str = ''.join([charset[i] for i in row])
            print(f"{padding}|{row_str}|")

        print(f"{padding_str}+{'-' * self.graph_width}+")
