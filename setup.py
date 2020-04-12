from pkg_resources import parse_requirements
from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='djmodels_creator',
    version='1.0',
    packages=find_packages(),
    description='Makes models.py file for Django ORM from csv files',
    url='https://github.com/fecitpotentiam/djmodels_creator',
    author='fecitpotentiam',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.7',
    install_reqs=parse_requirements('requirements.txt')
)