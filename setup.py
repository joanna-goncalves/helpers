from setuptools import setup, find_packages

requirements = ["toml", "PyYAML", "pandas", "sqlalchemy", "numpy"]

setup(
    name="helpers",
    version="1.1",
    install_requires=requirements,
    packages=find_packages(),
    author="your_name",
)



