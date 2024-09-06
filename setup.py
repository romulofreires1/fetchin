from setuptools import setup, find_packages

setup(
    name="http-helper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Rômulo Freires",
    description="A Python library for custom logging, metrics, and fetching HTTP requests",
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seuusuario/http-helper",
)

