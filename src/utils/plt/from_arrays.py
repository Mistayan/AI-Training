from typing import List, Tuple, Set

from matplotlib import pyplot as plt
from matplotlib.figure import Figure


def display_path_on_map(_cities: List[Tuple[str, int, int]], fig_size: int, path: Set|Tuple, name=None) -> Figure:
    ns, ys, xs = [], [], []
    fig = plt.Figure()
    plt.axis([0, fig_size, 0, fig_size])
    for cn, cx, cy in _cities:
        ns.append(cn)
        xs.append(cx)
        ys.append(cy)
        plt.scatter(cx, cy, marker='o')
        plt.annotate(cn,  # this is the text
                     (cx, cy),  # these are the coordinates to position the label
                     textcoords="offset points",  # how to position the text
                     xytext=(0, 10),  # distance from text to points (x,y)
                     ha='center',
                     fontsize=8)
    x2, y2 = [], []
    for p in path:
        if isinstance(p, int):
            i = p
        else:
            i = ns.index(p)
        x2.append(xs[i])
        y2.append(ys[i])
        plt.plot(x2, y2)
    plt.show()
    return fig
