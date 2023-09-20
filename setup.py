import setuptools
import os


with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()


with open(os.path.join("optic_object_wavefronts", "version.py")) as f:
    txt = f.read()
    last_line = txt.splitlines()[-1]
    version_string = last_line.split()[-1]
    version = version_string.strip("\"'")


setuptools.setup(
    name="optic_object_wavefronts",
    version=version,
    description="Representing optical components using object wavefronts",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Sebastian Achim Mueller",
    author_email="",
    url="https://github.com/cherenkov-plenoscope/optic_object_wavefronts",
    packages=["optic_object_wavefronts"],
    package_data={
        "optic_object_wavefronts": [
            "materials/media/*",
            "materials/surfaces/*",
        ]
    },
    python_requires=">=3",
    install_requires=[
        "shapely",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
)
