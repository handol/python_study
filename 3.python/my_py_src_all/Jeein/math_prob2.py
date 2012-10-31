import sys
import random


def add_two_dgts(nums):
	A = random.sample( range(10,70), nums)
	B = random.sample( range(10,70), nums)
	
	for i in range(nums):
		if A[i]%10 < 5: A[i] += 5
		if B[i]%10 < 5: B[i] += 5

	answers = []
	for i in range(nums):
		a = A[i]
		b = B[i]
		if a+b > 100:
			b = 100 - a - random.randint(1,10)
		answer = a + b
		answers.append(answer)
		print "(%2d)  %3d + %3d = ______"  % (i+1, a, b)

	print
	xx = ''
	for i in range(nums):
		xx += "%2d: %d, " % (i+1, answers[i])
	print xx
		
	

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "usage: num_problems"
		sys.exit(1)
	
	random.seed()

	add_two_dgts(int(sys.argv[1]))

