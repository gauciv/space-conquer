from setuptools import setup, find_packages

setup(
    name="space_conquer",
    version="2.0.0",  # Updated to version 2.0.0
    packages=find_packages(),
    install_requires=[
        "pygame",
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "space-conquer=src.game_manager:main",  # Updated path
        ],
    },
    author="Gauciv",
    description="A Python recreation of the classic Space Impact game",
    keywords="game, pygame, space, shooter",
    python_requires=">=3.6",
)
