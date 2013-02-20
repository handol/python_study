#!/usr/local/bin/python
import whrandom

debug = 0

lotto_SIZE = 6
lotto_MIN = 1
lotto_MAX = 45

myNum = [37, 36, 7, 14, 12, 20, 42, 7, 14, 12, 04, 36, 37, 42, 50, 02, 58 ]

#ratio = [30, 20, 20, 15, 15]
ratio = [15, 15, 15, 15, 15, 15, 10]
ratio_sum = []
change = [0, +1, -1, +10, -10, +2, -2]
# 30%
# 15% +1
# 15% -1
# 10% +10
# 10% -10

def getRatioSum():
	sum = 0
	for i in range( len(ratio) ):
		sum += ratio[i] 
		ratio_sum.append(sum)
	print 'ratio:', ratio_sum

def selNfromList(list, n):
	res = []
	idx = []
	i = 0
	while i<n:
		r = whrandom.randint(0,len(list)-1)
		if list[r] not in res:
			res.append(list[r])
			idx.append(r)
			i += 1

	print 'idx:', idx
	return res

def getModi_simple(org):
	r = whrandom.randint(1,100)
	for i in range(len(ratio_sum)):
		if r <= ratio_sum[i]:
			res = org + change[i]
			break
	if debug: print org,'-->',res
	return res

def getModi(org):
	if org>lotto_MAX: org %= lotto_MAX

	r = whrandom.randint(1,100)
	for i in range(len(ratio_sum)):
		if r <= ratio_sum[i]:
			res = org + change[i]
			break

	if debug: print "getModi:", org, i, change[i], res 

	if res>80:
		res = getModi(res)
		if debug: print "getModi:", org, i, change[i], res 

	if res < lotto_MIN or res > lotto_MAX:
		res = getModi(res)

	if debug: print org,'-->',res
	return res

def getLotto(luckies):
	mylotto=[]
	i=0
	j=0
	while i<lotto_SIZE:
		#org = whrandom.choice(luckies)
		if j >= len(luckies): j = 0 
		org = luckies[j]
		j += 1
		#lotto = getModi(org)
		lotto = getModi_simple(org)
		if lotto >= lotto_MIN and lotto <= lotto_MAX and\
		lotto not in mylotto: 
			mylotto.append(lotto)
			i += 1
	return mylotto

def prnList(list):
	pass

def evaluateLotto(list):
	odd=0
	highDgt = [0, 0, 0, 0, 0]
	for i in range(len(list)):
		if list[i]%2 == 1: odd += 1
		idx = list[i] / 10
		highDgt[int(idx)] += 1

	str= 'Even/Odd: %d %d , Dgts: %s' % (len(list)-odd, odd, highDgt)
	return str

def add_real_lottonum(fname):
	'add real lotto numbers to our magic number list'
	'lottoNums in recent 2 terms are added'
	f = open(fname, 'r')
	i = 0
	nums = []
	for l in f.readlines():
		w = l.split()
		if len(w) < 8: continue

		for n in w[2:]:
			nums.append(int(n))
		i += 1
		if i>=2: break

	return nums


if __name__=="__main__":
	whrandom.seed()
	getRatioSum()

	myNum = myNum + add_real_lottonum('lotto.data')
	print myNum
	all = []
	for i in range(10):
		print "----", i, "----"
		list = selNfromList(myNum, 6)
		print "Magic Num:", list
		res = getLotto( list )
		print "Lotto Num:", res
		res.sort()
		#print "Lotto Num:", res
		all.append(res)

	for l in range(len(all)):
		print all[l], ' '*(20-len(all[l])), evaluateLotto(all[l])
