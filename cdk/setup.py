#!/usr/bin/env python
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

setup(
    name='swarms-service-cdk',
    version='0.0.1-3.1',
    description='Swarms Aagent CDK code for deploying an AWS Lambda handler',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.13',
    ],
    url='https://github.com/ran-isenberg/aws-lambda-handler-cookbook',
    author='James Michael DuPont',
    author_email='jmikedupont2@gmail.com',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    package_data={'': ['*.json']},
    include_package_data=True,
    python_requires='>=3.13',
    install_requires=[],
)
