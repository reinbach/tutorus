try:
    from .currentenv import *
except ImportError:
    # going to assume that we are in prod and make use of prod settings
    from test import *
