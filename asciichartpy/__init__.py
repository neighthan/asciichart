"""
"""

# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------

from __future__ import division
from math import ceil, floor

# -----------------------------------------------------------------------------

__all__ = ['plot']

# -----------------------------------------------------------------------------

def plot(series, cfg=None, title=None):
    """
    :param series: a sequence of numeric values
    :param cfg: possible cfg parameters are 'minimum', 'maximum', 'height' and 'format'.
    :param title: the title for the plot. It will be centered over the main (non-axis)
      region of the plot if possible. If the title is too long, it begins just after the
      y-axis.

    Usage:
    ```
    print(plot([1, 3, 10 7], {'height': 10}))
    ```
	"""
    cfg = cfg or {}
    minimum = cfg['minimum'] if 'minimum' in cfg else min(series)
    maximum = cfg['maximum'] if 'maximum' in cfg else max(series)
    if minimum > maximum:
        raise ValueError('The minimum value cannot exceed the maximum value.')

    interval = maximum - minimum
    height = cfg['height'] if 'height' in cfg else ceil(interval)
    width = cfg.get('width', None)
    if title:
        height -= 1
    ratio = interval / (height - 1)

    n_decimals = 2
    n_digits_max = len(str(int(max(series))))
    placeholder = cfg['format'] if 'format' in cfg else f'{{:{n_digits_max + n_decimals + 1}.{n_decimals}f}} '
    offset = cfg['offset'] if 'offset' in cfg else 3
    if offset:
        placeholder = ' ' * offset + placeholder
    axis_len = len(placeholder.format(max(series))) + 1 # + 1 for the ┤
    if width:
        series = series[-(width - axis_len):]
    else:
        width = len(series) + axis_len
    result = [[' '] * width for i in range(height)]

    # axis and labels
    for i in range(height):
        label = placeholder.format(minimum + i * ratio)
        for j, char in enumerate(label):
            result[i][j] = char
        result[i][axis_len - 1] = '┼' if i == 0 else '┤'

    y0 = int((series[0] - minimum) / ratio)
    result[y0][axis_len - 1] = '┼' # first value

    for i in range(len(series) - 1): # plot the line
        y0 = round((series[i] - minimum) / ratio)
        y1 = round((series[i + 1] - minimum) / ratio)
        if y0 == y1:
            result[y0][i + axis_len] = '─'
        else:
            result[y1][i + axis_len] = '╰' if y0 > y1 else '╭'
            result[y0][i + axis_len] = '╮' if y0 > y1 else '╯'
            start = min(y0, y1) + 1
            end = max(y0, y1)
            for y in range(start, end):
                result[y][i + axis_len] = '│'

    plot_string = '\n'.join([''.join(row) for row in result[::-1]])
    if title:
        # Center the title over the non-axis portion of the plot.
        # If the title is too long, start just after axis ends.
        axis_idx = min(plot_string.index('┤'), plot_string.index('┼'))
        plot_length = plot_string.index('\n') - axis_idx
        n_padding = axis_idx + max((plot_length - len(title)) // 2, 1)
        title = ' ' * n_padding + title
        plot_string = '\n'.join((title, plot_string))
    return plot_string
