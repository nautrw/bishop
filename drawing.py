def print_graph(graph_width: int, graph_height: int, data: list[list[int]], draw_axis_numbers: bool) -> None:
    padding = 0
    padding_str = ' ' * padding

    if draw_axis_numbers:
        padding = 1
        padding_str = ' ' * padding
        top_num_padding = 2

        if graph_width >= 10:
            spaces_str = ' ' * (11 + padding)
            nums_str = ''.join([str(i)[0] for i in range(10, graph_width)])
            print(spaces_str + nums_str)

        nums_str = ''.join([str(i)[-1] for i in range(graph_width)])
        print(f"{' ' * top_num_padding}{nums_str}")

    print(f"{padding_str}+{'-' * graph_width}+")

    for y, row in enumerate(data):
        padding = y if draw_axis_numbers else padding_str
        row_str = ''.join([str(i) for i in row])
        print(f"{padding}|{row_str}|")

    print(f"{padding_str}+{'-' * graph_width}+")
