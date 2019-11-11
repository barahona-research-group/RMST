#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from distutils.core import setup, Extension

setup(
        name = 'RMST',
        version = '0.1',
        packages=['.'],
        install_requires=['numpy', 
                        'scipy', 
                        'matplotlib', 
                        'tqdm',
                        'networkx']
      )
