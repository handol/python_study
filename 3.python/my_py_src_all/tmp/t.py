

T = [None]*5
for t in T:
	print id(t)

TT = [None]*5
for t in TT:
	print id(t)

A = [10] * 5
for a in A:
	print id(a), "val=", a

A[0] = 5
for a in A:
	print id(a),  "val=", a


B = [[10]] * 5
for b in B:
	print id(b), "val=", b

B[0].append(20)
for b in B:
	print id(b), "val=", b


C = [[None]] * 5
for c in C:
	print id(c)


