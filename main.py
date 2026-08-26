GRAPH_WIDTH = 17
GRAPH_HEIGHT = 9

initial_graph = [[0 for _ in range(GRAPH_WIDTH)] for _ in range(GRAPH_HEIGHT)]

def print_graph(data: list[list[int]], draw_axis_numbers: bool) -> None:
    padding = 0
    padding_str = ' ' * padding

    if draw_axis_numbers:
        padding = 1
        padding_str = ' ' * padding
        top_num_padding = 2

        if GRAPH_WIDTH >= 10:
            spaces_str = ' ' * (11 + padding)
            nums_str = ''.join([str(i)[0] for i in range(10, GRAPH_WIDTH)])
            print(spaces_str + nums_str)

        nums_str = ''.join([str(i)[-1] for i in range(GRAPH_WIDTH)])
        print(f"{' ' * top_num_padding}{nums_str}")

    print(f"{padding_str}+{'-' * GRAPH_WIDTH}+")

    for y, row in enumerate(data):
        padding = y if draw_axis_numbers else padding_str
        row_str = ''.join([str(i) for i in row])
        print(f"{padding}|{row_str}|")

    print(f"{padding_str}+{'-' * GRAPH_WIDTH}+")

print_graph(initial_graph, True)
