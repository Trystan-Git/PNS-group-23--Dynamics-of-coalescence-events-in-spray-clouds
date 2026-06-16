
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 09:01:12 2026

Per-track velocity and size extractor for continuous cine videos.
Tracks droplets frame-to-frame; averages size and velocity over each track.
Outputs one row per track: speed, r_area, r_vol.

@author: nathanvani
"""



from pycine.raw import read_frames
from pycine.file import read_header
from scipy import ndimage
import numpy as np
import csv
from tqdm import tqdm

# ── parameters ────────────────────────────────────────────────────────────────
PATH          = "/Users/thijm/Documents/Video_droplets/nttm/50000fps_64micron_1mlperminute_1.cine"
THRESHOLD     = 2200/16
MIN_AREA      = 900
MAX_AREA      = 2800
X_LEFT        = 100
X_RIGHT       = 650
MAX_LINK_DIST = 150
MIN_TRACK_LEN = 5
FPS           = 50000
# METERS_PER_PIXEL = 3.85e-6
# ─────────────────────────────────────────────────────────────────────────────


def measure_blob(mask):
    """Return (r_area, r_vol) in pixels for a filled boolean mask."""
    ys, xs = np.where(mask)
    r_area = np.sqrt(mask.sum() / np.pi)

    vol_px3 = 0.0
    for xi in range(xs.min(), xs.max() + 1):
        col_ys = ys[xs == xi]
        if len(col_ys) == 0:
            continue
        half_h = (col_ys.max() - col_ys.min()) / 2.0
        vol_px3 += np.pi * half_h ** 2
    r_vol = (3 * vol_px3 / (4 * np.pi)) ** (1 / 3)

    return r_area, r_vol


def detect(frame_8):
    """Return list of blob dicts with x, y, r_area, r_vol."""
    binary = frame_8 < THRESHOLD
    binary = ndimage.binary_fill_holes(binary)
    labeled, n = ndimage.label(binary)

    blobs = []
    for i in range(1, n + 1):
        mask = labeled == i
        area = mask.sum()
        if area < MIN_AREA or area > MAX_AREA:
            continue
        ys, xs = np.where(mask)
        cx = xs.mean()
        cy = ys.mean()
        if cx < X_LEFT or cx > X_RIGHT:
            continue
        r_area, r_vol = measure_blob(mask)
        blobs.append({"x": cx, "y": cy, "r_area": r_area, "r_vol": r_vol})
    return blobs


def link(prev_blobs, curr_blobs, max_dist):
    """Nearest-neighbour frame-to-frame linking. Returns list of (pi, ci) pairs."""
    if not prev_blobs or not curr_blobs:
        return []
    pairs = []
    used_curr = set()
    for pi, pb in enumerate(prev_blobs):
        best_d, best_ci = np.inf, -1
        for ci, cb in enumerate(curr_blobs):
            if ci in used_curr:
                continue
            d = np.hypot(cb["x"] - pb["x"], cb["y"] - pb["y"])
            if d < best_d:
                best_d, best_ci = d, ci
        if best_d < max_dist and best_ci >= 0:
            pairs.append((pi, best_ci))
            used_curr.add(best_ci)
    return pairs


def run(path):
    header = read_header(path)
    n_frames = header['cinefileheader'].ImageCount

    print(f"frames: {n_frames}")

    # tracks[tid] = list of (frame, x, y, r_area, r_vol)
    tracks = {}
    next_id = 0
    active = []   # list of {"id": tid, "blob": blob_dict}

    frames_gen, _, _ = read_frames(path) #, count=100)
    for fi, frame in tqdm(enumerate(frames_gen), total=n_frames):
        frame_8 = (frame / 16).astype(np.uint8)
        curr_blobs = detect(frame_8)

        pairs = link([a["blob"] for a in active], curr_blobs, MAX_LINK_DIST)
        matched_curr = {ci for _, ci in pairs}

        # extend existing tracks
        for pi, ci in pairs:
            tid = active[pi]["id"]
            cb = curr_blobs[ci]
            tracks[tid].append((fi, cb["x"], cb["y"], cb["r_area"], cb["r_vol"]))

        # build new active list
        new_active = []
        for pi, ci in pairs:
            new_active.append({"id": active[pi]["id"], "blob": curr_blobs[ci]})

        # start new tracks for unmatched blobs
        for ci, cb in enumerate(curr_blobs):
            if ci not in matched_curr:
                tracks[next_id] = [(fi, cb["x"], cb["y"], cb["r_area"], cb["r_vol"])]
                new_active.append({"id": next_id, "blob": cb})
                next_id += 1

        active = new_active

        if fi % 1000 == 0:
            print(f"  frame {fi}/{n_frames}, active tracks: {len(active)}")

    print(f"total tracks: {len(tracks)}")

    # ── extract per-track averages ────────────────────────────────────────────
    rows = []
    for tid, obs in tracks.items():
        if len(obs) < MIN_TRACK_LEN:
            continue
        frames_idx = np.array([o[0] for o in obs])
        xs         = np.array([o[1] for o in obs])
        ys         = np.array([o[2] for o in obs])
        r_areas    = np.array([o[3] for o in obs])
        r_vols     = np.array([o[4] for o in obs])

        t_span = frames_idx[-1] - frames_idx[0]
        if t_span == 0:
            continue

        vx = (xs[-1] - xs[0]) / t_span * FPS 
        vy = (ys[-1] - ys[0]) / t_span * FPS 
        speed = np.hypot(vx, vy)

        rows.append({
            "speed_m_per_s": speed,
            "r_area_px":     r_areas.mean(),
            "r_vol_px":      r_vols.mean(),
            "track_len":     len(obs),
            "cx_mean_px":    xs.mean(),
            "cy_mean_px":    ys.mean(),
        })

    # ── save ──────────────────────────────────────────────────────────────────
    out_path = path.replace(".cine", "_vel_size2.csv")
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        for r in rows:
            writer.writerow({k: f"{v:.6g}" for k, v in r.items()})

    speeds = np.array([r["speed_m_per_s"] for r in rows])
    r_vols = np.array([r["r_vol_px"] for r in rows])
    print(f"extracted {len(rows)} tracks")
    print(f"saved → {out_path}")
    print(f"mean speed : {speeds.mean():.4f}  std: {speeds.std():.4f} m/s")
    print(f"mean r_vol : {r_vols.mean():.2f}  std: {r_vols.std():.2f} px")
    print(f"σ_v/v̄     : {speeds.std()/speeds.mean():.4f}")

    return rows


run(PATH)