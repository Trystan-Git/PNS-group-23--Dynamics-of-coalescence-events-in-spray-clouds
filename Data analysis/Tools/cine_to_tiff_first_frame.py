#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 09:53:59 2026

@author: nathanvani
"""

from pycine.raw import read_frames
import tifffile
import numpy as np

frames, setup, bpp = read_frames(r"\Users\thijm\Documents\Video_droplets\nttm\scale1.cine", count=1)
frame_list = [f for f in frames]
tifffile.imwrite(r"\Users\thijm\Documents\Video_droplets\nttm\scale1.tiff", np.array(frame_list))