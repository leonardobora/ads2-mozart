"""
Setup file for Music Content Classification Project
"""

from setuptools import setup, find_packages

setup(
    name="music-content-classification",
    version="0.1.0",
    description="Neural network models for sensitive content classification in music lyrics",
    author="Research Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "torch>=1.12.0",
        "transformers>=4.20.0", 
        "scikit-learn>=1.1.0",
        "numpy>=1.21.0",
        "pandas>=1.4.0",
        "nltk>=3.7",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "jupyter>=1.0.0",
        ],
        "viz": [
            "matplotlib>=3.5.0",
            "seaborn>=0.11.0",
            "plotly>=5.8.0",
        ],
    },
)