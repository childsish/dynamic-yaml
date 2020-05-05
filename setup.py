from setuptools import setup
from codecs import open
from os import path


def get_root_path():
    return path.dirname(path.realpath(__file__))


def read_file(filename):
    return open(path.join(get_root_path(), filename)).read()


setup(
    name='dynamic-yaml',
    version='1.2.2',
    description='Enables self referential yaml entries',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/childsish/dynamic-yaml',
    author='Liam Childs',
    author_email='liam.h.childs@gmail.com',
    license='MIT',
    packages=['dynamic_yaml'],
    python_requires='>=3.0',
    install_requires=['pyyaml==5.3'],
    extras_require={
        'dev': [
            'twine',
            'wheel'
        ]
    },
    keywords='development yaml configuration'
)
