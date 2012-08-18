try:
    from .currentenv import *
except ImportError:
    # Let's not harm people for using explicit settings
    pass
