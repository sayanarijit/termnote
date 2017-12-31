from setuptools import setup, find_packages
from codecs import open
from os import path
from termnote.termnote import VERSION

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Requirements for installation
with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()

setup(
    name='termnote',
    version=VERSION,
    description='A simple, yet powerful and handy terminal based note taking python app',
    long_description=long_description,
    url='https://github.com/sayanarijit/termnote',
    download_url='https://github.com/sayanarijit/termnote/archive/{}.tar.gz'.format(VERSION),
    author='Arijit Basu',
    author_email='sayanarijit@gmail.com',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Environment :: Console',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        'Operating System :: MacOS',
        'Operating System :: POSIX'
    ],
    keywords='Notes Management Terminal App',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=install_requirements,
    scripts=['bin/termnote', 'bin/tn']
)
