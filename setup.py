#!/usr/build/env python
# -*- coding: utf-8 -*-

from os import getcwd, path

from setuptools import setup, find_packages

with open(path.join(getcwd(), 'README.md'), mode='r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='punica',
    version='0.0.23',
    description="""Ontology DApp Development Framework""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='NashMiao',
    author_email='wdx7266@outlook.com',
    url='https://github.com/punicasuite/punica-python',
    maintainer='NashMiao',
    maintainer_email='wdx7266@outlook.com',
    # include_package_data=True,
    py_modules=['punica'],
    python_requires='>=3.6,<4',
    install_requires=[
        'halo==0.0.26',
        'crayons=0.2.0',
        'Click==7.0',
        'requests==2.22.0',
        'GitPython==2.1.11',
        'punica-neo-boa==0.4.9',
        'ontology-python-sdk==2.0.4',
    ],
    license="MIT",
    zip_safe=False,
    entry_points={
        'console_scripts': ["punica=punica.cli:main"],
    },
    packages=find_packages(exclude=["test*"]),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
