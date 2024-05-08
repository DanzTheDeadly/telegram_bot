from PIL import Image, ImageFilter, ImageEnhance
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np


def get_top_n_colors(img: Image, 
                     n: int) -> list[tuple[int, int, int]]:
    pixels = img.getdata()
    freqs = dict()
    for pixel in pixels:
        freqs[pixel] = 1 if not freqs.get(pixel) else freqs[pixel] + 1
    sorted_freqs = sorted(freqs, key=lambda v: freqs[v], reverse=True)
    return sorted_freqs[:n]


def main_pipeline(image_buffer: BytesIO,
                  contrast_coef: float,
                  blur_radius: int,
                  trunc_colors: int,
                  palette_size: int) -> list[tuple[int, int, int]]:
    img = Image.open(image_buffer)                            # open
    img = ImageEnhance.Contrast(img).enhance(contrast_coef)   # increase contrast
    img = img.filter(ImageFilter.BoxBlur(blur_radius))        # blur
    img = img.quantize(trunc_colors).convert('RGB')           # truncate colors
    top_n_colors = get_top_n_colors(img, palette_size)        # get N most frequent colors
    return top_n_colors


def save_colors(top_n_colors: list[tuple[int, int, int]], 
                buffer: BytesIO, 
                shape: tuple[int, int, int]):
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.imshow(np.array(top_n_colors).reshape(shape))
    fig.savefig(buffer, pad_inches=0, bbox_inches='tight')


if __name__ == '__main__':
    img_buffer = open('ava.jpeg', 'rb')
    with img_buffer:
        top_n_colors = main_pipeline(img_buffer, 1.5, 5, 64, 9)
    with open('palette.png', 'wb') as file:
        save_colors(top_n_colors, file, (3, 3, 3))
