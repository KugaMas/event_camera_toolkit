import os
import os.path as osp
from .fio_utils import load_aedat4, load_txt


def _assert(path):
    _, extension = osp.splitext(osp.basename(path))
    assert extension in ['.h5', '.txt', '.pkl', '.zip', '.aedat4'], \
        "Unsupported file type"

    return extension


def load(path):
    extension = _assert(path)
    _load = eval(f'load_{extension[1:]}')
    data = _load(path)
    return data


def save(path):
    # TODO
    pass


def search():
    # TODO
    pass


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    data = load('tests/alley-1.aedat4', True)
