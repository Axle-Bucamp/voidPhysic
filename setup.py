"""
Setup script for void physics module.

This is a legacy setup script for compatibility.
The recommended way to install is using uv: uv sync
"""

from setuptools import setup, find_packages

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="void-physic",
    version="0.1.0",
    author="Void Physics Research",
    author_email="research@void-physic.org",
    description="Mathematical modeling and visualization of void physics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/void-physic/void-physic",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.11",
    install_requires=[
        "manimgl>=1.7.0",
        "sympy>=1.12",
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "matplotlib>=3.6.0",
        "numba>=0.57.0",
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "void-physic=void_physic.cli:main",
        ],
    },
)
