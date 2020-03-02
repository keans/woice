from setuptools import setup, find_packages
import codecs
import os

# get current directory
here = os.path.abspath(os.path.dirname(__file__))


def get_long_description():
    """
    get long description from README.rst file
    """
    with codecs.open(os.path.join(here, "README.rst"), "r", "utf-8") as f:
        return f.read()


setup(
    name='woice',
    version='0.0.2',
    description='A small script to connect to the WiFiOnICE network.',
    long_description=get_long_description(),
    url='https://keans.de',
    author='Ansgar Kellner',
    author_email='keans@gmx.de',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='python packaging',
    packages=find_packages(
        exclude=['contrib', 'docs', 'tests']
    ),
    entry_points={
        'console_scripts': [
            'woice = woice.woice:main',
        ],
    },
    install_requires=[
        "lxml", "requests"
    ],
)
