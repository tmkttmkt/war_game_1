import numpy as np
from PIL import Image
import base64
from IPython import display as dd


def array_normalize(array: np.ndarray, max_v):
    array = array / max_v
    array *= 255
    return array.astype(np.uint8)


def array_to_img(array: np.ndarray, max_v=2, img_size=(64, 64)):
    img = Image.fromarray(array_normalize(array, max_v)).resize(img_size, Image.NEAREST).convert('P')
    return img


def arrays_to_gif(array_list,
                  save_path='sample.gif',
                  max_v=4,
                  img_size=(64, 64),
                  show=False,
                  duration=1000):
    images = [array_to_img(array, max_v, img_size) for array in array_list]
    images[0].save(save_path,
               save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=0)
    if show:
        with open(save_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")

        display(dd.HTML(f'<img src="data:image/gif;base64,{b64}" />'))