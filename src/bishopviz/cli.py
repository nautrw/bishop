import random
import string
import subprocess
import sys
import time
from pathlib import Path

import click

from bishopviz.algorithm import DrunkenBishopAlgorithm
from bishopviz.charsets import CHARACTER_SETS
from bishopviz.hash import bytes_to_pairs, text_md5

GRAPH_WIDTH = 17
GRAPH_HEIGHT = 9

@click.command()
@click.option('-r', '--random-feed', is_flag=True, help="Use a random text string as the input.")
@click.option('-a', '--animate', type=float, help="Display the algorithm's progress as an animation, with the specified number of seconds as the interval between frames.")
@click.option('-c', '--charset', type=str, show_default=True, default="ascii", help="Use a different character set for the graph. Options: ascii, ascii_alt, emoji, emoji2, emoji3, emoji4, greek, cyrillic, katakana, math, blocks, faces, cars, plants")
@click.option('-C', '--colors', is_flag=True, help="Whether to colorize the output.")
@click.option('-d', '--data', is_flag=True, help="Will open a Streamlit app in the web browser to show statistics and graphs from the algorithm.")
@click.option('--no-start-end', is_flag=True, help="Don't show the start and end positions on the graph.")
def cli(random_feed: bool, animate: float, charset: str, colors: bool, data: bool, no_start_end: bool,) -> None:
    if data:
        subprocess.Popen([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(Path(__file__).parent / "data.py"),
            "--server.headless=true",
            "--browser.gatherUsageStats=false"
        ])
    else:
        accomodate_large_chars = False

        if charset not in CHARACTER_SETS:
            raise click.ClickException("You must select one of the character set options. To view the available options, run `bishopviz --help`.")
        elif charset in ["emoji", "emoji2", "emoji3", "emoji4", "katakana", "faces", "cars", "plants"]:
            accomodate_large_chars = True

        if random_feed:
            feed = ''.join(random.choices(string.printable, k=32))

        hash = text_md5(feed)
        print(f'Hash: {hash.hexdigest()}')

        byte_pairs = bytes_to_pairs(hash.digest())
        algorithm = DrunkenBishopAlgorithm(GRAPH_WIDTH, GRAPH_HEIGHT, byte_pairs)

        if animate:
            for i in range(len(byte_pairs)):
                algorithm.move()
                print(f"Generation: {i + 1}")
                algorithm.print_graph(CHARACTER_SETS[charset], show_start=not no_start_end, show_end=not no_start_end, show_current_position=True, accomodate_large_chars=accomodate_large_chars, colorize=colors)

                if i != len(byte_pairs) - 1:
                    # basically this moves the cursor to the top of the box,
                    # giving the illusion of an animation
                    # \r is the carriage return, so it moves it to the beginning
                    # of the line
                    # \x1b[yA is an ANSI escape code, which moves the cursor `y`
                    # lines up
                    print(f'\r\x1b[{GRAPH_HEIGHT + 4}A')

                time.sleep(animate)
        else:
            for _ in range(len(byte_pairs)):
                algorithm.move()

            algorithm.print_graph(CHARACTER_SETS[charset], show_start=not no_start_end, show_end=not no_start_end, show_current_position=False, accomodate_large_chars=accomodate_large_chars, colorize=colors)
