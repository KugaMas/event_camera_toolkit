import os
import time
import numpy as np
import pandas as pd
from dv import AedatFile, Event, Frame, Trigger, IMU
from numpy.lib import recfunctions as rfn


class _data():
    def __init__(self) -> None:
        self._data = {
            'size': None,
            'events': None,
            'frames': None,
            'imu':    None,
            'triggers': None,
        }
    
    def __getitem__(self, _name):
        return self._data[_name]

    def __setitem__(self, _name, _value):
        if type(_value) is np.ndarray and _value.dtype.names is not None:
            _value = np.rec.array(_value)
        self._data[_name] = _value


def load_aedat4(path):
    data = _data()

    with AedatFile(path) as f:
        data['size'] = f['events'].size

        # events
        if 'events' in f.names:
            events = np.hstack([packet for packet in f['events'].numpy()])
            events_type = [('timestamp', '<i8'), ('x', '<i2'),('y', '<i2'), ('polarity', 'i1')]
            events = np.array(rfn.drop_fields(events, ['_p1', '_p2']), dtype=events_type)
            data['events'] = events

        # frames
        if 'frames' in f.names:
            frames = [(frame.timestamp, frame.image) for frame in f['frames']]
            frames_type = [('timestamp', '<i8'), ('image','i2', frames[0][1].shape)]
            frames = np.array(frames, dtype=frames_type)
            data['frames'] = frames

    return data


def load_txt(path):
    data = _data()

    # events
    with open(path, "r+") as f:
        data['size'] = tuple(np.loadtxt(f, max_rows=1).astype(np.int_))
        events = pd.read_csv(f, sep='\s+', header=None)
        events_type = [('timestamp', '<i8'), ('x', '<i2'),('y', '<i2'), ('polarity', 'i1')]
        events = np.array(events, dtype=events_type)
        data['events'] = events
    
    return data


if __name__ == '__main__':
    main_dir = os.path.dirname(__file__)
    os.chdir(main_dir)

    st = time.time()
    data = load_aedat4(os.path.join(main_dir, "tests/demo-01.aedat4"))
    print(f"load aedat4 file ==> {time.time() - st} s")

    st = time.time()
    data = load_txt(os.path.join(main_dir, "tests/demo-02.txt"))
    print(f"load txt file ==> {time.time() - st} s")

