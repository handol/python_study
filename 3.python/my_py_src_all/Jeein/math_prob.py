import sys
import random

def problem1(v_sum):
	v_min = v_sum / 10
	v_r = random.randint(v_min, v_sum - 1)
	v_comp = v_sum - v_r
	underbar = '_' * (1 + len(str(v_sum)) )
	print "%4d + %s = %4d"  % (v_r, underbar, v_sum)


if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "usage: num_problems  sum"
		sys.exit(1)

	for i in  range(int(sys.argv[1])):
		problem1(int(sys.argv[2]))

