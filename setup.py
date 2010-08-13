import os.path

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


import mcgrep

           
setup(name='mcgrep',
      version=mcgrep.__version__,
      author="Scott Torborg",
      author_email="storborg@mit.edu",
      license="GPL",
      keywords="memcached memcache pylibmc diagnostics caching pentesting",
      url="http://github.com/storborg/mcgrep",
      description='Memcached probing, diagnostics, debugging, and grepping.',
      packages=find_packages(exclude=['ez_setup', 'tests']),
      long_description=read('README.rst'),
      test_suite='nose.collector',
      zip_safe=False,
      entry_points = {
          'console_scripts': [
              'mcgrep = mcgrep:main']},
      classifiers=[
          "Development Status :: 3 - Alpha",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Intended Audience :: Developers",
          "Natural Language :: English",
          "Programming Language :: Python"])
