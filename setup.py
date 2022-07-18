import setuptools
import os

with open("README.md", "r") as f:
    long_description = f.read()

version = {}
with open(os.path.join("optic_object_wavefronts/version.py")) as f:
    exec(f.read(), version)

setuptools.setup(
    name="optic_object_wavefronts",
    version=version["__version__"],
    description="Representing optical components using object wavefronts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sebastian Achim Mueller",
    author_email="",
    url="https://github.com/cherenkov-plenoscope/optic_object_wavefronts",
    license="GPL v3",
    packages=["optic_object_wavefronts"],
    package_data={
        "optic_object_wavefronts": [
            "materials/media/*",
            "materials/surfaces/*",
        ]
    },
    python_requires=">=3",
    install_requires=["shapely",],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
)
