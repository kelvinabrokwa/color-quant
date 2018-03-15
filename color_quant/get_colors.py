#!/usr/bin/env python
"""Calculates the main colors in front of the camera and their weights
"""

import argparse
import cv2
import json

from utils import get_image
from sklearn.cluster import MiniBatchKMeans


def get_colors(image, k):
    """Given a number 3d BRG array, returns the k main colors in it
    :param image:
    :param k:
    :returns:
    """
    # stash dimensions for later reshaping
    (h, w) = image.shape[:2]

    # convert to Lab color space because differences in those colors correspond to
    # euclidean distance which is used in k-means clustering
    image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # sklearn k-means algorithms expect n_samples x n_features matrix
    # n_pixels x 3 in this case
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    # use MiniBatchKMeans for speed
    mbk = MiniBatchKMeans(n_clusters=k)
    # quantize
    labels = mbk.fit_predict(image)
    quant = mbk.cluster_centers_.astype("uint8")[labels]

    # reshape into original dimensions
    quant = quant.reshape((h, w, 3))

    # convert back to BGR
    quant = cv2.cvtColor(quant, cv2.COLOR_LAB2BGR)

    # count how many pixels fall into each color bin
    colors = {}
    for row in quant:
        for pixel in row:
            color = ','.join(map(str, pixel))
            if color in colors:
                colors[color] += 1
            else:
                colors[color] = 1

    # calculate color weights
    out = []
    total = float(sum(colors.values()))
    for color in colors:
        c = map(int, color.split(","))
        c.reverse()  # reverse to RGB
        out.append({
            "color": c,
            "weight": colors[color] / total,
        })

    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get colors')
    parser.add_argument('-k', type=int, dest="k", nargs=1, default=4, help="number of color bins")
    args = parser.parse_args()
    image = get_image()
    print(json.dumps(get_colors(image, args.k)))
