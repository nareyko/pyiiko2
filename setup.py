from setuptools import setup, find_packages

setup(
    name='Pyiiko2',
    description='Library for iikoAPI',
    url='https://github.com/nareyko/pyiiko2',
    author='Vadim Nareyko',
    author_email='vadim@nareyko.com',
    version='0.3.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests>=2.20.0',
        'defusedxml>=0.6.0'
    ]
)
