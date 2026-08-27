import random
import string

import click

from bishopviz.algorithm import DrunkenBishopAlgorithm
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

@click.command()
@click.option('-r', '--random_feed', is_flag=True, help="Use a random text string as the input.")
def cli(random_feed: bool) -> None:
    if random_feed:
        feed = ''.join(random.choices(string.printable, k=32))

    byte_pairs = bytes_to_pairs(encode_text(feed))

    algorithm = DrunkenBishopAlgorithm(GRAPH_WIDTH, GRAPH_HEIGHT, byte_pairs)

    for _ in range(len(byte_pairs)):
        algorithm.move()

    print_graph(GRAPH_WIDTH, GRAPH_HEIGHT, algorithm.graph, False, CHARACTERS)
