from setuptools import setup, find_packages

setup(
    name="ATB",
    version="1.0",
    packages=find_packages(exclude=["tests.*", "test"])
)