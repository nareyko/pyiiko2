from setuptools import setup, find_packages
from os.path import join, dirname


setup(
    name='Pyiiko2',
    description='Library for iikoAPI',
    url='https://github.com/nareyko/pyiiko2',
    author='Vadim Nareyko',
    author_email='vadim@nareyko.com',
    version='0.3.1',
    packages=find_packages(),
    include_package_data=True,
    test_suite='tests',
    install_requires=[
        'requests>=2.20.0',
        'lxml>=4.1.1'

    ]
)
