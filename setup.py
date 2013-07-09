from setuptools import setup, find_packages
import md5  # fix for "No module named _md5" error


setup(name='expiringdict',
      version='1.0',
      description="Dictionary with auto-expiring values for caching purposes",
      long_description=open("README.md").read(),
      author='Anton Efimenko',
      author_email='anton@mailgunhq.com',
      url='http://www.mailgun.com',
      license='MIT',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=True,
      extras_require={'test': ['nose', 'mock']})
