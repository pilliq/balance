# AMDG

from setuptools import setup
from balance import __version__

setup(name='balance',
      version=__version__,
      description='A balance book',
      keywords=['balance', 'ledger'],
      url='http://github.com/pilliq/balance',
      author='Phillip Quiza',
      author_email='pquiza@gmail.com',
      license='MIT',
      packages=['balance'],
      test_suite='tests.all_tests',
      entry_points = {
          'console_scripts': [
              'balance = balance.cli:main',
          ],
      },
      zip_safe=False)
