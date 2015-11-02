from setuptools import setup, find_packages
try:
    import md5  # fix for "No module named _md5" error
except ImportError:
    # python 3 moved md5
    from hashlib import md5

with open("README.rst") as f:
    long_description = f.read()


setup(name='expiringdict',
      version='1.1.3',
      description="Dictionary with auto-expiring values for caching purposes",
      long_description=long_description,
      author='Anton Efimenko',
      author_email='anton@mailgunhq.com',
      url='https://github.com/mailgun/expiringdict',
      license='Apache 2',
      packages=find_packages(exclude=['tests']),
      classifiers=[
                   'Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Apache Software License',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Topic :: Software Development :: Libraries',
                   'Topic :: Software Development :: Libraries :: Python Modules'],
      include_package_data=True,
      zip_safe=True,
      extras_require={'test': ['nose', 'mock', 'coverage']})
