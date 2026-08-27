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
