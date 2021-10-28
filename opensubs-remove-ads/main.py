from glob import glob
from os import error
import re
from typing import List

import click
import pysrt


OPEN_SUB_REGEX = re.compile(r"OpenSubtitles")
FONT_COLOR_REGEX = re.compile(r"<font color=")


@click.command()
@click.option("-d", "--debug", is_flag=True)
@click.option("--encoding")
@click.argument("directories", type=click.Path(exists=True), nargs=-1)
def cli(directories: List[str] = ["."], encoding: str = "utf-8", debug: bool = False):
    if not directories:
        directories = ["."]
    for dir in directories:
        files = glob(dir + '/**/*.srt', recursive=True)
        for file in files:
            try:
                write_change = False
                subs = pysrt.open(file, encoding="ISO-8859-1")
                for sub in subs:
                    if OPEN_SUB_REGEX.match(sub.text) or FONT_COLOR_REGEX.match(sub.text):
                        subs.remove(sub)
                        write_change = True
                subs.clean_indexes()
                if write_change:
                    if debug:
                        print(f"Updating subtitle file: {file.split('/')[-1]}")
                    subs.save(file)
            except Exception as error:
                print(f"Error working on file\n{file.split('/')[-1]}")
                print(f"Error - {error}")


if __name__ == "__main__":
    cli()