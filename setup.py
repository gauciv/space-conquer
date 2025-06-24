from setuptools import setup, find_packages

setup(
    name="space_impact",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pygame",
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "space-impact=space_impact.game_manager:main",
        ],
    },
    author="Space Impact Developer",
    description="A Python recreation of the classic Space Impact game",
    keywords="game, pygame, space, shooter",
    python_requires=">=3.6",
)
