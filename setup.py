from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize("rapper.pyx"),
    include_dirs=[numpy.get_include()]
)

def f(j,oo,d = 100, m = 150):
    pass
