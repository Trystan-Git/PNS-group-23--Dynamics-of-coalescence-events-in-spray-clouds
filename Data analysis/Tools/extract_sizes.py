#Our supervisor provided us with this code

#!/usr/bin/env python3
"""
Per-frame droplet size extractor for snapshot cine files.
No tracking — just detect blobs in each frame and record sizes.
Outputs a CSV with one row per detected droplet.
"""

from pycine.raw import read_frames
from pycine.file import read_header
from scipy import ndimage
import numpy as np
import csv
from tqdm import tqdm

# ── parameters ────────────────────────────────────────────────────────────────
PATH        = "/Users/thijm/Documents/Video_droplets/nttm/50000fps_64micron_1mlperminute_1.cine"
PATH        = "/Users/thijm/Documents/Video_droplets/nttm/70000fps_64micron_2mlperminute_1.cine"
THRESHOLD   = 145/16            # pixels below this are "dark" (droplet)
MIN_AREA    = 64             # px², discard noise
MAX_AREA    = 2000        # px², discard frame artifacts


# ─────────────────────────────────────────────────────────────────────────────


def measure_blob(mask):
    """
    Given a filled boolean mask for one blob, return sizes in pixels.
      r_area : area-equivalent radius (px)
      r_vol  : volume-integrated radius (px), from disc-stacking along x
    """
    ys, xs = np.where(mask)

    area = mask.sum()
    r_area = np.sqrt(area / np.pi)

    vol_px3 = 0.0
    for xi in range(xs.min(), xs.max() + 1):
        col_ys = ys[xs == xi]
        if len(col_ys) == 0:
            continue
        half_h = (col_ys.max() - col_ys.min()) / 2.0
        vol_px3 += np.pi * half_h ** 2

    r_vol = (3 * vol_px3 / (4 * np.pi)) ** (1/3)

    cx = xs.mean()
    cy = ys.mean()

    return cx, cy, r_area, r_vol


def detect_frame(frame_8):
    """Threshold, fill holes, label, return list of blob measurements."""
    binary = frame_8 < THRESHOLD          # dark blobs on bright background
    binary = ndimage.binary_fill_holes(binary)
    labeled, n = ndimage.label(binary)

    results = []
    for i in range(1, n + 1):
        mask = labeled == i
        area = mask.sum()
        if area < MIN_AREA or area > MAX_AREA:
            continue
        cx, cy, r_area, r_vol = measure_blob(mask)
        if cy < 20:
            continue
        if cy > 60:
            continue
        results.append((cx, cy, r_area, r_vol))
    return results


def run(path):
    header = read_header(path)
    n_frames = header['cinefileheader'].ImageCount
    print(f"frames: {n_frames}")

    out_path = path.replace(".cine", "_sizes.csv")
    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["frame", "cx_px", "cy_px", "r_area_px", "r_vol_px"])

        frames_gen, _, _ = read_frames(path)
        for fi, frame in tqdm(enumerate(frames_gen), total=n_frames):
            frame_8 = (frame / 16).astype(np.uint8)
            blobs = detect_frame(frame_8)
            for cx, cy, r_area, r_vol in blobs:
                writer.writerow([fi, f"{cx:.1f}", f"{cy:.1f}",
                                 f"{r_area:.3f}", f"{r_vol:.3f}"])

    print(f"saved → {out_path}")


# adapt tiff file
# import tifffile

# def run_tiff(path):
    # with tifffile.TiffFile(path) as tif:
    #     frames = tif.asarray()  # shape: (n_frames, H, W) for a stack

    # n_frames = frames.shape[0]
    # print(f"frames: {n_frames}")

    # out_path = path.replace(".tif", "_sizes.csv").replace(".tiff", "_sizes.csv")

    # with open(out_path, "w", newline="") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["frame", "cx_px", "cy_px", "r_area_px", "r_vol_px"])

    #     for fi, frame in tqdm(enumerate(frames), total=n_frames):
    #         frame_8 = (frame / 16).astype(np.uint8)
    #         blobs = detect_frame(frame_8)
    #         for cx, cy, r_area, r_vol in blobs:
    #             writer.writerow([fi, f"{cx:.1f}", f"{cy:.1f}",
    #                              f"{r_area:.3f}", f"{r_vol:.3f}"])

    # print(f"saved → {out_path}")







run(PATH)
