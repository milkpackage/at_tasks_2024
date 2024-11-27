from setuptools import setup, find_packages

setup(
    name="mantis_framework",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'selenium>=4.18.1',
        'pytest>=8.0.0',
        'webdriver-manager>=4.0.1',
    ],
)