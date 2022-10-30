import numpy as np
import pandas as pd

from dv import AedatFile
from numpy.lib import recfunctions as rfn


class _struct():
    def __init__(self) -> None:
        pass
    
    def __bool__(self):
        return len(vars(self)) > 0

def _data():

    data = {
        'events': _struct(),
        'frames': _struct(),
        'imu':    _struct(),
    }
    data['events'].size = None
    data['frames'].size = None

    return data


def load_aedat4(path, use_aps=True, use_imu=True):
    data = _data()

    # events
    with AedatFile(path) as f:
        data['events'].size = f['events'].size
        events = np.hstack([packet for packet in f['events'].numpy()])
        events = rfn.structured_to_unstructured(events)
    data['events'].ts = events[:, 0]
    data['events'].x  = events[:, 1]
    data['events'].y  = events[:, 2]
    data['events'].p  = events[:, 3]

    # frames
    if use_aps:
        with AedatFile(path) as f:
            data['frames'].size = f['frames'].size
            frames = [frame for frame in f['frames']]
        data['frames'].ts = [frame.timestamp for frame in frames]
        data['frames'].image = [frame.image for frame in frames]

    return data


def load_txt(path, use_aps=False, use_imu=False):
    data = _data()

    # events
    with open(path, "r+") as f:
        events = pd.read_csv(f, sep='\s+', header=None, skiprows=[0],
                            dtype={'0': np.float32, '1': np.int8, '2': np.int8, '3': np.int8})
        events = np.array(events).astype(np.uint64)
    data['events'].ts = events[:, 0]
    data['events'].x  = events[:, 1]
    data['events'].y  = events[:, 2]
    data['events'].p  = events[:, 3]
    with open(path, "r+") as f:
        data['events'].size = tuple(np.loadtxt(f, max_rows=1).astype(np.int_))
    
    return data
