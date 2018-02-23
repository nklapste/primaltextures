#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""Main argparse/entrypoint module for primaltextures"""

import argparse
import os
import subprocess
from tempfile import TemporaryDirectory
from typing import List

from PIL import Image


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

    image = Image.open(args.input)

    with TemporaryDirectory() as tempdir:
        pass

    if args.output_folder:
        os.makedirs(args.output_folder, exist_ok=True)


def make_primitive_image(input_image_path: str, output_image_path: str,
                         shape_number: int, **kwargs) -> Image.Image:
    """Use fogleman/primitive to make a primitive image

    Store them in a temporary directory for later processing

    :param input_image_path:
    :type input_image_path: str

    :param output_image_path:
    :type output_image_path: str

    :param shape_number:
    :type shape_number: int

    :param kwargs:
    :type kwargs: dict
    """
    primitive_command = ["%primitive%", "-i", input_image_path, "-o",
                         output_image_path, "-n", str(shape_number)]

    # run the primitive command
    subprocess.run(
        primitive_command,
        stdout=subprocess.PIPE,
        shell=True
    )
    return Image.open(output_image_path)


def make_primitive_image_list(input_image: str, output_dir: str,
                              image_number: int, shape_number: int,
                              **kwargs) -> List[Image.Image]:
    """Make some primitive images and return a list of their paths

    :param input_image:
    :param output_dir:
    :param image_number:
    :param shape_number:
    :param kwargs:
    :return images:
    """
    images = []
    for i in range(image_number):
        output_filename = os.path.join(output_dir, "temp{}.png".format(i))
        images.append(make_primitive_image(input_image, output_filename, shape_number))
    return images


def to_gif(filename: str, images: List[Image.Image], duration: float):
    """Convert primitive images into a .gif format
    :param filename:
    :param images:
    :param duration:
    """
    widths, heights = zip(*(i.size for i in images))
    max_width = max(widths)
    max_height = max(heights)
    new_im = Image.new(images[0].mode, (max_width, max_height))

    # paste the first image in to remove black frame
    new_im.paste(images[0])
    new_im.save(
        filename,
        save_all=True,
        append_images=images,
        duration=duration,
        loop=0,
        version="GIF89a",
        disposal=1
    )


def to_animated_spritesheet(filename: str, images: List[Image.Image]):
    """Convert primitive images to a animated spritesheet
    :param filename:
    :param images:
    """
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    new_im = Image.new(images[0].mode, (total_width, max_height))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    new_im.save(filename)


images = make_primitive_image_list(
    "C:/Users/Nathan/GenericProjects/primaltextures/primaltextures/the_future.png",
    "C:/Users/Nathan/GenericProjects/primaltextures/primaltextures/",
    image_number=10,
    shape_number=50,
)

to_gif(
    "out.gif",
    images,
    10
)

for image in images:
    os.remove(image.filename)
