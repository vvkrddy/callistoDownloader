from setuptools import setup, find_packages
import numpy, sys
import re

def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop),
                       open(project + '/__init__.py').read())
    return result.group(1)

def get_requires():
    reqs = []
    for line in open('requirements.txt', 'r').readlines():
        reqs.append(line)
    return reqs

setup(
    name='callistoDownloader',
    version=get_property('__version__', 'callistoDownloader'),
    description='A python package to download e-Callisto spectrograms',
    url='https://github.com/vvkrddy/callistoDownloader',
    author='Pininti Vivek Reddy',
    author_email='',
    license='MIT',
    packages=find_packages(),
    include_dirs=[numpy.get_include()],
    include_package_data = True,
    zip_safe=False,
    classifiers=[

        'Development Status :: 3 - Alpha',      

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Astronomy',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        ],
    keywords='Solar Physics Astronomy Spectrogram',
    install_requires=get_requires()
    )