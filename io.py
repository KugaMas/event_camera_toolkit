import os
import pickle

import numpy as np
import pandas as pd
import os.path as osp

from dv import AedatFile
from scipy.io import savemat
from numpy.lib import recfunctions as rfn


def _assert(path):
    ext = osp.splitext(osp.basename(path))[1]
    assert ext in ['.h5', '.txt', '.pkl', '.aedat4'], "Unsupported file type"
    return ext


def load(path, aps=False, imu=False, size=None):
    ev, fr, gyro, accel = None, None, None, None
    ext = _assert(path)

    if ext == '.aedat4':
        with AedatFile(path) as f:
            ev = np.hstack([packet for packet in f['events'].numpy()])
            ev = rfn.structured_to_unstructured(ev)[1:, :4].astype(np.uint64)
            size = f['events'].size[::-1] if size is None else size
    if ext == '.txt':
        with open(path, "r+") as f:
            ev = pd.read_csv(f, sep='\s+', header=None, skiprows=[0],
                             dtype={'0': np.float32, '1': np.int8, '2': np.int8, '3': np.int8})
            ev = np.array(ev).astype(np.uint64)
        with open(path, "r+") as f:
            size = tuple(np.loadtxt(f, max_rows=1).astype(np.int_)) if size is None else size
    if ext == '.pkl':
        with open(path, "rb+") as f:
            ev = pd.read_pickle(f)['events']
            ev = np.array(ev).astype(np.uint64)
        with open(path, "rb+") as f:
            size = pd.read_pickle(f)['size'] if size is None else size

    if aps:
        if ext == '.aedat4':
            with AedatFile(path) as f:
                fr = [[np.array(packet.image).squeeze(), packet.timestamp] for packet in f['frames']]
        if ext == '.pkl':
            with open(path, "rb+") as f:
                fr = [[np.array(packet[0]), packet[1]] for packet in pd.read_pickle(f)['frames']]

    return ev, fr, size


def save(ev, fr=None, size=None, params=None, path='./results.txt'):
    ext = _assert(path)

    dir, file = osp.split(path)

    if not osp.exists(dir):
        os.makedirs(dir)
        if params is not None:
            os.makedirs(f"{dir}/.params")

    if ext == '.pkl':
        with open(path, 'wb+') as f:
            pickle.dump(dict(events=ev, frames=fr, size=size), f)

    if ext == '.txt':
        with open(path, 'wt') as f:
            f.write('%3d %3d\n' % (size[0], size[1]))
        with open(path, 'at') as f:
            np.savetxt(f, ev, fmt="%16d %3d %3d %1d", delimiter=' ', newline='\n')

    if params is not None:
        savemat(f"{dir}/.params/{file.replace(ext, '.mat')}", params)


def search(file, path):
    return
