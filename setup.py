from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="GlotScript",
    version="1.0",
    author="Amir Hossein Kargaran",
    author_email="kargaranamir@email.com",
    description="A package for detecting the script (writing system) of given text.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cisnlp/GlotScript",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
