from setuptools import setup, find_packages

try:
    ModuleNotFoundError
except NameError:
    ModuleNotFoundError = ImportError

try:
    import md5  # fix for "No module named _md5" error
except ImportError:
    # python 3 moved md5
    from hashlib import md5

tests_require = [
    "dill",
    "coverage",
    "coveralls",
    "mock",
    "nose",
]

setup(name="expiringdict",
      version="1.2.2",
      description="Dictionary with auto-expiring values for caching purposes",
      long_description=open("README.rst").read(),
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Topic :: Software Development :: Libraries",
      ],
      keywords="",
      author="Mailgun Technologies Inc.",
      author_email="admin@mailgun.com",
      url="https://www.mailgun.com/",
      license="Apache 2",
      packages=find_packages(exclude=["tests"]),
      include_package_data=True,
      zip_safe=True,
      tests_require=tests_require,
      install_requires=[
          'typing;python_version<"3.5"',
      ],
      extras_require={
          "tests": tests_require,
      })
