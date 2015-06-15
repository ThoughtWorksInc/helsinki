import os
from setuptools import setup, find_packages

fileList = []
for root, subFolders, files in os.walk('helsinki/templates'):
    for file in files:
        fileList.append(os.path.join(root,file))

setup(
    name='helsinki',
    version='0.0.1',
    description='Notifications for helsinki citizens',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 2.7'
    ],
    packages=find_packages(),
    package_data={'helsinki': fileList},
    entry_points={
        'console_scripts': ['helsinki=helsinki.main:run_app']
    }
)
