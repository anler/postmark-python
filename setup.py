import os
import sys

from setuptools import setup, find_packages

py_version = sys.version_info[:2]

here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, "README.txt")).read()
except IOError:
    README = ""

dependencies = []

test_dependencies = [
    "pyDoubles"
]

scripts = {
    "console_scripts": []
}


setup(name="postmark-python",
      version="0.1",
      description="Simple postmark api client",
      long_description=README,
      author="Anler Hernandez Peral",
      author_email="anler86@gmail.com",
      url="http://github.com/ikame/postmark-python/",
      license="MIT",
      packages=find_packages(exclude=["tests"]),
      entry_points=scripts,
      test_suite="tests",
      tests_require=test_dependencies,
      install_requires=dependencies,
      keywords="email api postmark",
      classifiers=[
          "Environment :: Web Environment",
          "Intended Audience :: Developers"])
