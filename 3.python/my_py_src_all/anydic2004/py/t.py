import os
import time
from stat import *

def prn_finfo(path):
	s = os.stat(path)
	print path, s[ST_SIZE], s[ST_MTIME], time.strftime('%Y/%M/%D %h:%m%s', s[ST_MTIME])

prn_finfo('.')
