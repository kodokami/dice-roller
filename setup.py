from setuptools import setup, find_packages
from dice_roller import (
    __version__ as VERSION,
    NAME,
    COMMAND_NAME,
    DESCRIPTION
)

setup(
    name=NAME,
    version=VERSION,
    author='_kodokami',
    author_email='kodokami@protonmail.com',
    description=DESCRIPTION,
    license='MIT License',
    packages=find_packages(exclude=['tests', 'tests.*']),
    python_requires='>=3.12',
    platforms=['Unix'],
    entry_points={
        'console_scripts': [
            f'{COMMAND_NAME}=dice_roller.__main__:execute',
        ]
    }
)
