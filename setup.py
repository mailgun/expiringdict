from setuptools import setup, find_packages

with open("README.rst") as f:
    long_description = f.read()


setup(name='expiringdict',
      version='1.1.4',
      description="Dictionary with auto-expiring values for caching purposes",
      long_description=long_description,
      author='Anton Efimenko',
      author_email='anton@mailgunhq.com',
      url='https://github.com/mailgun/expiringdict',
      license='Apache 2',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=True,
      extras_require={'test': ['nose', 'mock', 'coverage']})
