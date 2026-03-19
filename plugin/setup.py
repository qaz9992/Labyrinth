"""
python setup.py build_ext --inplace
"""

from setuptools import setup, Extension
from Cython.Build import cythonize

ext = Extension(
    name="example",        # 模块名（import 用这个）
    sources=["example.py"],
    language="c"
)

setup(ext_modules=cythonize(ext))