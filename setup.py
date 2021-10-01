import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="python-liang",
    version="0.0.1",
    description="Incorporate non-functional requirements in function definitions",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/yizhang7210/liang",
    author="Yi Zhang",
    author_email="yi.zhang7210@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["liang"],
    include_package_data=True,
    install_requires=[],
)
