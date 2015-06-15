from setuptools import setup, find_packages

setup(
    name='helsinki',
    version='0.0.1',
    description='Notifications for helsinki citizens',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 2.7'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': ['helsinki = helsinki.main::run_app']
    }
)
