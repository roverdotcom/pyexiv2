'''\
This file is a hack to get the package working post-build but without
requiring an actual installation. Specifically, this enables
"development mode" installation via ``python setup.py develop``.

'''

from ..build.libexiv2python import *
