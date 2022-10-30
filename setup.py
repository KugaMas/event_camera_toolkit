import os
from setuptools import setup, find_packages


def _process_requirements():
    packages = open('config/requirements.txt').read().strip().split('\n')
    return [pkg for pkg in packages]

setup(
    name='utils',
    version='1.0.0',
    author='KugaMax',
    description="simple toolkit for event-based data",
    py_modules=['kutils'],
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=_process_requirements()
)
