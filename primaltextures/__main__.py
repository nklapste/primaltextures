#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""Main argparse/entrypoint module for primaltextures"""

import argparse
from tempfile import TemporaryDirectory

import os


def main():
    """Main argparse function for primaltextures"""

    parser = argparse.ArgumentParser(
        description="primaltextures: A python script that utilizes "
                    "fogleman/primitive and ImageMagick to create "
                    "funny/simple textures."
    )

    group = parser.add_argument_group(title="input options")
    group.add_argument("-i", "--input", help="input file to be used for "
                                             "generating primaltextures")

    group = parser.add_argument_group(title="output options")
    group.add_argument("-o", "--output", help="location to save generated "
                                              "primaltextures")
    group.add_argument("-f", "--output-folder", dest="output_folder",
                       help="folder to where generated primaltextures and "
                            "additional content will be saved. Overrides "
                            "'-o' '--output-folder'")

    args = parser.parse_args()

    with TemporaryDirectory() as tempdir:
        pass

    if args.output_folder:
        os.makedirs(args.output_folder, exist_ok=True)


def generate_primal_textures():
    """Use fogleman/primitive to generate primitive textures

    Store them in a temporary directory for later processing
    """


def to_gif():
    """Convert primal textures into a .gif format"""


def to_animated_spritesheet():
    """Convert primal textures to a animated spritesheet"""
    # TODO modify for use
    # import sys
    # from PIL import Image
    #
    # images = map(Image.open, ['Test1.jpg', 'Test2.jpg', 'Test3.jpg'])
    # widths, heights = zip(*(i.size for i in images))
    #
    # total_width = sum(widths)
    # max_height = max(heights)
    #
    # new_im = Image.new('RGB', (total_width, max_height))
    #
    # x_offset = 0
    # for im in images:
    #   new_im.paste(im, (x_offset,0))
    #   x_offset += im.size[0]
    # new_im.save('test.jpg')