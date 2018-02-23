#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""pytests for primaltextures"""
from typing import Tuple, Any, List

import pytest

import os

from PIL import Image

from primaltextures.__main__ import make_primitive_image, \
    make_primitive_image_list, to_gif, to_animated_spritesheet


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
IMG_PATH = os.path.join(BASE_DIR, "the_future.png")


def make_temp_primitive_image(tmpdir_factory) -> Tuple[Any, Image.Image]:
    """"""
    fn = tmpdir_factory.mktemp('temp').join("out.png")
    image = make_primitive_image(
        IMG_PATH,
        str(fn),
        3,
    )
    return fn, image

@pytest.fixture(scope='session')
def primitive_images(tmpdir_factory) -> Tuple[Any, List[Image.Image]]:
    fn = tmpdir_factory.mktemp('temp')
    images = make_primitive_image_list(
        IMG_PATH,
        str(fn),
        3,
        3,
    )
    return fn, images


def test_to_gif(primitive_images):
    """test to_gif"""
    fn, images = primitive_images
    to_gif(
        os.path.join(str(fn), "out.gif"),
        images,
        duration=5
    )


def test_to_spritesheet(primitive_images):
    """test to_spritesheet"""
    fn, image_paths = primitive_images
    to_animated_spritesheet(
        os.path.join(str(fn), "out.png"),
        image_paths,
    )