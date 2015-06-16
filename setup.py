import os
from setuptools import setup, find_packages

requirements = [line.rstrip('\n') for line in open('requirements.txt')]

setup(
    name='helsinki',
    version='0.0.1',
    description='Notifications for helsinki citizens',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 2.7'
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': ['helsinki=helsinki.main:run_app']
    }
)
