try:
    # Python 3.4 and greater
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch
from nose.tools import *
