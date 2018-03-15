# Color Quant

A Python library for quantizing the colors in an image.

It uses [k-means clustering](https://en.wikipedia.org/wiki/K-means_clustering) for image quantization.

### Usage

```sh
python get_colors.py -k <n_clusters>
```

or

```py
from get_colors import get_colors
color_weights = get_colors(4)
```

## Developing

#### Dependencies

- [Python](https://www.python.org/)
- [OpenCV](http://opencv-python-tutroals.readthedocs.io/)
- [Numpy](http://www.numpy.org/)
- [Scikit Learn](http://scikit-learn.org/stable/)


![](/screenshot.png)
