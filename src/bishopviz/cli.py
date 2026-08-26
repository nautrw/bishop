from bishopviz.drawing import print_graph
from bishopviz.hash import bytes_to_pairs, encode_text

GRAPH_WIDTH = 17
GRAPH_HEIGHT = 9

CHARACTERS = {
    0: " ",
    1: ".",
    2: "o",
    3: "+",
    4: "=",
    5: "*",
    6: "B",
    7: "0",
    8: "X",
    9: "@",
    10: "%",
    11: "&",
    12: "#",
    13: "/",
    14: "^",
    15: "S",
    16: "E",
}


def run_algorithm(byte_pairs: list[str]) -> tuple[list[list[int]], tuple[int, int]]:
    graph = [[0 for _ in range(GRAPH_WIDTH)] for _ in range(GRAPH_HEIGHT)]
    bishop_x = GRAPH_WIDTH // 2
    bishop_y = GRAPH_HEIGHT // 2


    for pair in byte_pairs:
        bishop_x += 1 if pair[1] == "1" else -1
        bishop_y += 1 if pair[0] == "1" else -1

        bishop_x = max(bishop_x, 0)
        bishop_y = max(bishop_y, 0)
        bishop_x = min(bishop_x, GRAPH_WIDTH - 1)
        bishop_y = min(bishop_y, GRAPH_HEIGHT - 1)

        graph[bishop_y][bishop_x] += 1
    
    graph[GRAPH_HEIGHT // 2][GRAPH_WIDTH // 2] = 15 # start is always marked 15
    graph[bishop_y][bishop_x] = 16 # same with end but 16
    end_point = (bishop_x, bishop_y)

    return graph, end_point

bytes = bytes_to_pairs(encode_text("SHA256:s6N0OwlTDKjDez98kZRwUGZbTYaQUArv+EYC6sigFwA ben@eshwil"))
data = run_algorithm(bytes)
print_graph(GRAPH_WIDTH, GRAPH_HEIGHT, data[0], True, CHARACTERS)
