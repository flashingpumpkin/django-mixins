#!/usr/bin/env python
from setuptools import find_packages, setup
import mixins

METADATA = dict(
    name='django-mixins',
    version=mixins.__version__,
    author='Alen Mujezinovic',
    author_email='alen@caffeinehit.com',
    description='Useful mixins for Django class based views',
    long_description=open('README.rst').read(),
    url='http://github.com/flashingpumpkin/django-mixins',
    keywords='django views mixins',
    packages = find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'Topic :: Internet',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
)


setup(**METADATA)
