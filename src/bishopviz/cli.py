import random
import string
import time

import click

from bishopviz.algorithm import DrunkenBishopAlgorithm
from bishopviz.charsets import CHARACTER_SETS
from bishopviz.hash import bytes_to_pairs, encode_text

GRAPH_WIDTH = 17
GRAPH_HEIGHT = 9

@click.command()
@click.option('-r', '--random-feed', is_flag=True, help="Use a random text string as the input.")
@click.option('-a', '--animate', type=float, help="Display the algorithm's progress as an animation, with the specified number of seconds as the interval between frames.")
@click.option('-c', '--charset', type=str, show_default=True, default="ascii", help="Use a different character set for the graph. Options: ascii, ascii_alt, emoji, emoji2, emoji3, emoji4, greek, cyrillic, katakana, math, blocks")
@click.option('--no-start-end', is_flag=True, help="Don't show the start and end positions on the graph.")
def cli(random_feed: bool, seconds: float, charset: str, no_start_end: bool) -> None:
    if random_feed:
        feed = ''.join(random.choices(string.printable, k=32))

    byte_pairs = bytes_to_pairs(encode_text(feed))

    algorithm = DrunkenBishopAlgorithm(GRAPH_WIDTH, GRAPH_HEIGHT, byte_pairs)

    if seconds:
        for i in range(len(byte_pairs)):
            algorithm.move()
            print(f"Generation: {i + 1}")
            algorithm.print_graph(CHARACTER_SETS[charset], True, True, True)

            if i != len(byte_pairs) - 1:
                # basically this moves the cursor to the top of the box,
                # giving the illusion of an animation
                # \r is the carriage return, so it moves it to the beginning
                # of the line
                # \x1b[yA is an ANSI escape code, which moves the cursor `y`
                # lines up
                print(f'\r\x1b[{GRAPH_HEIGHT + 4}A')

            time.sleep(seconds)
    else:
        for _ in range(len(byte_pairs)):
            algorithm.move()

        algorithm.print_graph(CHARACTER_SETS[charset], not no_start_end, not no_start_end, False)
