from setuptools import setup, find_packages
import md5  # fix for "No module named _md5" error


setup(name='expiringdict',
      version='1.1.3',
      description="Dictionary with auto-expiring values for caching purposes",
      long_description=open("README.rst").read(),
      author='Anton Efimenko',
      author_email='anton@mailgunhq.com',
      url='https://github.com/mailgun/expiringdict',
      license='Apache 2',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=True,
      extras_require={'test': ['nose', 'mock', 'coverage']})
