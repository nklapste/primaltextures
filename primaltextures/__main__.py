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
                    "fogleman/primitive to create funny/simple textures.")

    parser.add_argument("-i", "--input", type=str, required=True,
                        help="input file to be used for generating primitive "
                             "images")

    group = parser.add_argument_group(title="primitive image options")
    group.add_argument("-n", "--shape-number", type=int, dest="shape_number",
                       help="number of shapes to use to generate "
                            "primitive images")

    group = parser.add_argument_group(title="normal image generation")
    group.add_argument("-m", "--image-number", type=int, dest="image_number",
                       help="number of primitive images to generate")
    group.add_argument("-o", "--output", type=str,
                       help="specify a path to generate a primitive image")
    group.add_argument("-f", "--output-folder", type=str, dest="output_folder",
                       help="specify a directory generate multiple "
                            "primitive images")

    group = parser.add_argument_group(title="gif output options")
    group.add_argument("-g", "--gif", type=str,
                       help="specify a path to output a .gif with each frame "
                            "being rendered primitive image")
    group.add_argument("-F", "--frame-number", type=int, dest="frame_number",
                       help="number of primitive images to generate frames"
                            "for the .gif")
    group.add_argument("-d", "--duration", type=int, default=10,
                       help="duration of the .gif")

    group = parser.add_argument_group(title="spritesheet output options")
    group.add_argument("-s", "--spritesheet", type=str,
                       help="specify a path to output a x by y spritesheet "
                            "with each tile being rendered primitive image")
    group.add_argument("-x", "--cols", type=int,
                       help="amount of tile columns for output spritesheet")
    group.add_argument("-y", "--rows", type=int,
                       help="amount of tile rows for output spritesheet")

    args = parser.parse_args()

    if args.output:
        make_primitive_image(
            args.input,
            args.output,
            shape_number=args.shape_number
        )

    if args.output_folder:
        os.makedirs(args.output_folder, exist_ok=True)
        make_primitive_image_list(
            args.input,
            args.output_folder,
            image_number=args.image_number,
            shape_number=args.shape_number,
        )

    with TemporaryDirectory() as tempdir:
        if args.gif:
            images = make_primitive_image_list(
                args.input,
                tempdir,
                image_number=args.frame_number,
                shape_number=args.shape_number,
            )

            to_gif(
                args.gif,
                images,
                duration=args.duration
            )

        if args.spritesheet:
            images = make_primitive_image_list(
                args.input,
                tempdir,
                image_number=args.cols * args.rows,
                shape_number=args.shape_number,
            )

            to_x_by_y_spritesheet(
                args.spritesheet,
                images,
                cols=args.cols,
                rows=args.rows
            )


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
        images.append(
            make_primitive_image(input_image, output_filename, shape_number))
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


def to_x_by_y_spritesheet(filename: str, images: List[Image.Image],
                          cols: int, rows: int):
    """Create a cols by rows spritesheet filling row first

    :param filename:
    :param images:
    :param cols:
    :param rows:
    :return:
    """
    if len(images) != cols * rows:
        raise ValueError("{} images cannot be represented by a {} by {} "
                         "tiled spritesheet".format(len(images), cols, rows))

    # grab a ref image
    width, height = images[0].size

    total_width = width * cols
    total_height = height * rows

    new_im = Image.new(images[0].mode, (total_width, total_height))
    x_pos = 0
    y_pos = 0
    for im in images:

        new_im.paste(im, (width * x_pos, height * y_pos))
        x_pos += 1
        if x_pos % cols == 0:
            y_pos += 1
            x_pos = 0
    new_im.save(filename)


if __name__ == "__main__":
    main()

