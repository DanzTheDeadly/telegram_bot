from PIL import Image, ImageFilter
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np



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


def main_pipeline(image_buffer,
                  num_colors, 
                  trunc_val,  
                  blur_radius):
    img = Image.open(image_buffer)                            # open
    img_blurred = blur(img, blur_radius)                      # blur
    pixels = img_blurred.getdata()                            # transform to list
    pixels_trunc = trunc_colors(pixels, trunc_val)            # reduce color variety
    top_n_colors = get_top_n_colors(pixels_trunc, num_colors) # get N most frequent colors
    return top_n_colors


def save_colors(top_n_colors: list[tuple[int, int, int]], buffer, shape):
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.imshow(np.array(top_n_colors).reshape(shape))
    fig.savefig(buffer, pad_inches=0, bbox_inches='tight')


if __name__ == '__main__':
    img_buffer = open('ava.jpeg', 'rb')
    with img_buffer:
        top_n_colors = main_pipeline(img_buffer, 8, 40, 10)
    with open('palette.png', 'wb') as file:
        save_colors(top_n_colors, file, (4, 2, 3))
