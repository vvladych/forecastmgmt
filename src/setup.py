__author__="vvladych"
__date__ ="$09.10.2014 23:12:01$"

from setuptools import setup,find_packages

setup (
  name = 'forecaster',
  version = '0.1',
  packages = find_packages(),

  # Declare your packages' dependencies here, for eg:
  install_requires=['foo>=3'],

  # Fill in these to make your Egg ready for upload to
  # PyPI
  author = 'vvladych',
  author_email = '',

  summary = 'Python package for the forecast/predictions management',
  url = '',
  license = '',
  long_description= 'Long description of the package',

  # could also include long_description, download_url, classifiers, etc.

  
)
