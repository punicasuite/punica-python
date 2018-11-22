#!/usr/build/env python
# -*- coding: utf-8 -*-

from os import getcwd, path

from setuptools import setup, find_packages

with open(path.join(getcwd(), 'README.md'), mode='r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='punica',
    version='0.0.12',
    description="""Ontology DApp Development Framework""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='NashMiao',
    author_email='wdx7266@outlook.com',
    url='https://github.com/ontio-community/punica-python',
    maintainer='NashMiao',
    maintainer_email='wdx7266@outlook.com',
    # include_package_data=True,
    py_modules=['punica'],
    python_requires='>=3.6,<4',
    install_requires=[
        'Click',
        'GitPython',
        'punica-neo-boa',
        'ontology-python-sdk',
    ],
    license="MIT",
    zip_safe=False,
    entry_points={
        'console_scripts': ["punica=punica.cli:main"],
    },
    packages=find_packages(exclude=["test*"]),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
