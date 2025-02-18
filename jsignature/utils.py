"""
    Very inspired by zivezab's django-autograph
    https://github.com/zivezab/django-autograph/blob/master/autograph/utils.py
"""
import json
from itertools import chain
from PIL import Image, ImageDraw, ImageOps

AA = 5  # super sampling gor antialiasing
LINE_WIDTH = 1
COLOR = "#000F55"

def draw_signature(data, as_file=False):
    """ Draw signature based on lines stored in json_string.
        `data` can be a json object (list in fact) or a json string
        if `as_file` is True, a temp file is returned instead of Image instance
    """

    def _remove_empty_pts(pt):
        return {
            'x': list(filter(lambda n: n is not None, pt['x'])),
            'y': list(filter(lambda n: n is not None, pt['y']))
        }

    if type(data) is str:
        drawing = json.loads(data, object_hook=_remove_empty_pts)
    elif type(data) is list:
        drawing = data
    else:
        raise ValueError

    # Compute box
    width = int(round(max(chain(*[d['x'] for d in drawing])))) + 10
    height = int(round(max(chain(*[d['y'] for d in drawing])))) + 10

    # Draw image
    im = Image.new("RGBA", (width * AA, height * AA))
    draw = ImageDraw.Draw(im)
    # Decor Line
    draw.line([(0, 0.85*height* AA), (width* AA, 0.85*height* AA)], fill="#000000", width=LINE_WIDTH * AA)
    # Draw handwriting
    for line in drawing:
        len_line = len(line['x'])
        points = [(line['x'][i] * AA, line['y'][i] * AA)
                  for i in range(0, len_line)]
        draw.line(points, fill=COLOR, width=LINE_WIDTH * AA)
    im = ImageOps.expand(im)
    # Smart crop
    bbox = im.getbbox()
    if bbox:
        im.crop(bbox)

    im.thumbnail((width, height), Image.Resampling.LANCZOS)

    if as_file:
        ret = im._dump(format='PNG')
    else:
        ret = im

    return ret
