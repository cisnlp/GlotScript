from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="LangScriptID",
    version="0.1",
    author="Amir Hossein Kargaran",
    author_email="kargaranamir@email.com",
    description="A package for detecting the script and language of given texts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kargaranamir/LangScriptID",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)