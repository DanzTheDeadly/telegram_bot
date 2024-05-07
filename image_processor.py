from PIL import Image, ImageFilter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


IMAGE_PATH = 'ava.jpeg'
RESULT_PATH = 'palette.png'
NUM_COLORS = 8
TRUNC_VAL = 40
BLUR_RADIUS = 10


def blur(img: Image, 
         r: int) -> Image:
    return img.filter(ImageFilter.BoxBlur(r))


def trunc_colors(pixels: list[tuple[int, int, int]],
                 trunc: int) -> list[tuple[int, int, int]]:
    trunc_func = lambda val: (val // trunc * trunc)
    res = []
    for pixel in pixels:
        res.append(tuple(map(trunc_func, pixel)))
    return res


def get_top_n_colors(pixels: list[tuple[int, int, int]],
                     n: int) -> list[tuple[int, int, int]]:
    freqs = dict()
    for pixel in pixels:
        freqs[pixel] = 1 if not freqs.get(pixel) else freqs[pixel] + 1
    sorted_freqs = sorted(freqs, key=lambda v: freqs[v], reverse=True)
    return sorted_freqs[:n]


def main_pipeline(image_path,
         num_colors, 
         trunc_val,  
         blur_radius):
    img = Image.open(image_path)                              # open
    img_blurred = blur(img, blur_radius)                      # blur
    pixels = img_blurred.getdata()                            # transform to list
    pixels_trunc = trunc_colors(pixels, trunc_val)            # reduce color variety
    top_n_colors = get_top_n_colors(pixels_trunc, num_colors) # get N most frequent colors
    return top_n_colors


if __name__ == '__main__':
    top_n_colors = main_pipeline(IMAGE_PATH, 
                                 NUM_COLORS, 
                                 TRUNC_VAL, 
                                 BLUR_RADIUS)
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.imshow([top_n_colors])
    fig.savefig(RESULT_PATH)