import os, sys
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import subprocess

class GfortranExtension(Extension):
    def __init__(self, name, sourcedir='', input='', output=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)
        self.input = os.path.join(self.sourcedir, input)
        self.output = os.path.join(self.sourcedir, output)

class GfortranBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output('${FC:-gfortran} --version', shell=True)
        except OSError:
            raise RuntimeError("gfortran must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        gfortran_args = ['-fPIC',
                         '-fdefault-real-8',
                         '-shared',
                         '-o',
                         ext.output]

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        env = os.environ.copy()
        subprocess.check_call('${FC:-gfortran} ' + " ".join([ext.input] + gfortran_args),
                              cwd=self.build_temp, env=env, shell=True)

setup(name='glmnet_python',
      version = '1.0.1',
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
      ext_modules=[GfortranExtension('GLMnet', 'glmnet_python',
                                     'GLMnet.f', 'GLMnet.so')],
      cmdclass={'build_ext': GfortranBuild},
)
