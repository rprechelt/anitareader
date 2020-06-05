from os import path

from setuptools import find_packages, setup
from cmake import CMakeExtension, CMakeBuild

# the anitareader version
__version__ = "0.0.1"

# get the absolute path of this project
here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# the standard setup info
setup(
    name="anitareader",
    version=__version__,
    description="A fast, pure Python reader for ANITA data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rprechelt/anitareader",
    author="Remy L. Prechelt",
    author_email="prechelt@hawaii.edu",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords=[""],
    packages=["anitareader"],
    python_requires=">=3.6*, <4",
    install_requires=["xarray", "numpy", "uproot", "cachetools"],
    extras_require={
        "test": [
            "pytest",
            "black",
            "mypy",
            "isort",
            "coverage",
            "pytest-cov",
            "flake8",
        ],
    },
    scripts=[],
    project_urls={},
    include_package_data=True,
    # call into CMake to build our module
    ext_modules=[CMakeExtension("_anitareader")],
    cmdclass={"build_ext": CMakeBuild},
    zip_safe=False,
)
