import numpy as np
import random
import cv2

def normalize(weights):
    total = sum(weights)
    return [w / total for w in weights]

def weighted_choice(ratios):
    r = random.random()
    cum = 0
    for i, p in enumerate(ratios):
        cum += p
        if r < cum:
            return i
    return len(ratios) - 1

def blend_images(images, ratios, block_size=1):
    """
    Args:
        images (list of np.ndarray): List of images to blend as a patchwork.
        ratios (list of float): Contribution ratio of each image in the final result.
        block_size (int or (int, int) or (int, int, int, int)):
            - int: Fixed block size.
            - (min, max): Random square block size in [min, max].
            - (h_min, h_max, w_min, w_max): Height and width are randomly chosen in [h_min, h_max] and [w_min, w_max], respectively.

    Returns:
        np.ndarray: The resulting blended image.
    """

    N = len(images)
    assert N >= 1, "At least one image is required."
    assert len(ratios) == N, "Length of ratios must match the number of images."


    height, width = images[0].shape[:2]
    output = np.zeros_like(images[0])

    probs = normalize(ratios)

    if isinstance(block_size, int):
        def get_block_size():
            return block_size, block_size
    elif isinstance(block_size, tuple) and len(block_size) == 2:
        min_size, max_size = block_size
        def get_block_size():
            size = random.randint(min_size, max_size)
            return size, size
    elif isinstance(block_size, tuple) and len(block_size) == 4:
        h_min, h_max, w_min, w_max = block_size
        def get_block_size():
            h = random.randint(h_min, h_max)
            w = random.randint(w_min, w_max)
            return h, w
    else:
        raise ValueError("block_size must be int, (min,max) or (h_min,h_max,w_min,w_max)")

    y = 0
    while y < height:
        x = 0
        while x < width:
            bh, bw = get_block_size()
            h = min(bh, height - y)
            w = min(bw, width - x)

            idx = weighted_choice(probs)
            output[y:y+h, x:x+w] = images[idx][y:y+h, x:x+w]

            x += w
        y += h

    return output

import argparse

def parse_block_size(block_size_str):
    parts = list(map(int, block_size_str.split(',')))
    if len(parts) == 1:
        return parts[0]
    elif len(parts) == 2:
        return tuple(parts)
    elif len(parts) == 4:
        return tuple(parts)
    else:
        raise argparse.ArgumentTypeError("block_size must be 1, 2, or 4 comma-separated integers")

def main():
    parser = argparse.ArgumentParser(description="Blend multiple images.")
    parser.add_argument("--images", type=str, nargs='+', required=True, help="Input image paths")
    parser.add_argument("--ratios", type=float, nargs='+', default = [0.0], help="Blend ratios")
    parser.add_argument("--block_size", type=str, default="1", help="Block size: int or comma-separated (e.g. 16,32)")
    parser.add_argument("--output", type=str, default="output.png", help="Path to output image")
    args = parser.parse_args()

    images = [cv2.imread(p, cv2.IMREAD_UNCHANGED) for p in args.images]
    images = [cv2.cvtColor(img, cv2.COLOR_BGR2BGRA) for img in images]

    h, w = images[0].shape[:2]
    images = [cv2.resize(img, (w, h)) for img in images]
    
    if args.ratios == [0.0]:
        args.ratios = np.random.rand(len(images))

    block_size = parse_block_size(args.block_size)

    result = blend_images(images, args.ratios, block_size=block_size)
    cv2.imwrite(args.output, result)
    print(f"Saved output to: {args.output}")

    