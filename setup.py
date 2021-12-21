from pkg_resources import parse_requirements
from setuptools import setup
with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='GutenProcessor',
    version='0.1',
    packages=['GutenProcessor'],
    url='',
    license='GNU',
    author='Davide Picca',
    author_email='davide.picca@unil.ch',
    description='This is a package for processing Gutenberg.org resources',
    install_requires = install_requires,
    classifiers=[
                # How mature is this project? Common values are
                #   3 - Alpha
                #   4 - Beta
                #   5 - Production/Stable
                'Development Status :: 3 - Alpha',

                # Indicate who your project is intended for
                'Intended Audience :: Developers',
                'Topic :: Software Development :: Build Tools',

                # Specify the Python versions you support here. In particular, ensure
                # that you indicate whether you support Python 2, Python 3 or both.
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.6',
                'Programming Language :: Python :: 3.7',
                'Programming Language :: Python :: 3.8',
                'Programming Language :: Python :: 3.9',
            ]
)
