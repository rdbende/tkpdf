from setuptools import setup
import subprocess

version = subprocess.check_output(["git", "describe", "--abbrev=0", "--tags"]).strip().decode()

assert version[0] == "v"  # Something went wrong

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="tkpdf",
    version=version,
    description="PDF viewer for Tkinter.",
    author="rdbende",
    author_email="rdbende@gmail.com",
    url="https://github.com/rdbende/tkpdf",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["pymupdf"],
    python_requires=">=3.6",
    license="MIT license",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["tkpdf"]
)
