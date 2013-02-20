import time
import sys

def sleep_n(n):
	for i in range(n):
		time.sleep(1)


if len(sys.argv) < 2: 
	sys.exit(0)

sleep_n(int(sys.argv[1]) )
