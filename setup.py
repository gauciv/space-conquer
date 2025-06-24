from setuptools import setup, find_packages

setup(
    name="space_conquer",
    version="1.0.0",  # Initial release version
    packages=find_packages(),
    install_requires=[
        "pygame",
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "space-conquer=space_impact.game_manager:main",
        ],
    },
    author="Gauciv",
    description="A Python recreation of the classic Space Impact game",
    keywords="game, pygame, space, shooter",
    python_requires=">=3.6",
)
