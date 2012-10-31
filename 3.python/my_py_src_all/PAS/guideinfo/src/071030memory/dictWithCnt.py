
from operator import itemgetter

###
# 중복되는 key들의 개수를 저장하는 dict.
# DictWithList 보다는 간단한 형태. 원래의 value는 저장되지 않음.
###
class DictWithCnt(dict):
        # key, value를 dict 에 추가하는 것.
	def add(self, key, cnt=0):
		self[key] = 1 + self.get(key, cnt)

	def rank(self):
		# rank high those which has high counter value
		return sorted(self.iteritems(), key=itemgetter(1), reverse=True)

	def prn(self, mincnt=0):
		# rank high those which has high counter value
		ranked = sorted(self.iteritems(), key=itemgetter(1), reverse=True)
		for (key, cnt) in ranked:
			if cnt > mincnt:
				print "%4d\t%s" % (cnt, key)
	def html(self, mincnt=0):
		self.prn(mincnt)
	
