import os, sys
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import subprocess

class Compile(build_py):
    """Custom build setup to help run needed shell commands

    Inspired by https://stackoverflow.com/a/27953695/1237531"""
    def run(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        source_path = os.path.join(dir_path, 'glmnet_python/GLMnet.f')
        output_path = os.path.join(dir_path, 'glmnet_python/GLMnet.so')
        compile = subprocess.check_output(['gfortran',
            source_path,
            '-fPIC',
            '-fdefault-real-8',
            '-shared',
            '-o',
            output_path
        ])
        build_py.run(self)

setup(name='glmnet_python',
      version = '0.2.2',
      description = 'Python version of glmnet, from Stanford University',
      long_description=open('README.md').read(),
      url="https://github.com/johnlees/glmnet_python",
      author = 'Han Fang (modified by John Lees)',
      author_email = 'hanfang.cshl@gmail.com,john@johnlees.me',
      license = 'GPL-2',
      packages=['glmnet_python'],
      install_requires=['joblib>=0.10.3'],
      package_data={'glmnet_python': ['*.so', 'glmnet_python/*.so']},
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Operating System :: Unix',
        ],
      keywords='glm glmnet ridge lasso elasticnet',
      cmdclass={'build_py': Compile},
)
