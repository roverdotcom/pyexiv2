'''\
This file is a hack to get the package working post-build but without
requiring an actual installation. Specifically, this enables
"development mode" installation via ``python setup.py develop``.

'''

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..', 'build')))
reload(sys.modules['libexiv2python'])
from libexiv2python import *
