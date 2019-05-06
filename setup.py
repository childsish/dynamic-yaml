from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dynamic-yaml',
    version='1.1.4',
    description='Enables self referential yaml entries',
    long_description=long_description,
    url='https://github.com/childsish/dynamic-yaml',
    author='Liam Childs',
    author_email='liam.h.childs@gmail.com',
    license='MIT',
    packages=['dynamic_yaml'],
    install_requires=['pyyaml'],
    extras_require={
        'dev': [
            'twine',
            'wheel'
        ]
    },
    keywords='development yaml configuration'
)
