import sys
from setuptools import setup, find_packages
import md5  # fix for "No module named _md5" error


requirements = []
if sys.version_info < (2, 7):
    requirements.append('ordereddict')


setup(name='expiringdict',
      version='1.0',
      description="Dictionary with auto-expiring values for caching purposes",
      long_description=open("README.md").read(),
      author='Anton Efimenko',
      author_email='anton@mailgunhq.com',
      url='https://github.com/mailgun/expiringdict',
      license='APACHE2',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=requirements,
      extras_require={'test': ['nose', 'mock', 'coverage']})
