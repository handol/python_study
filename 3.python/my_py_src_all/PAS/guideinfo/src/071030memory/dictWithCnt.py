
from operator import itemgetter

###
# �ߺ��Ǵ� key���� ������ �����ϴ� dict.
# DictWithList ���ٴ� ������ ����. ������ value�� ������� ����.
###
class DictWithCnt(dict):
        # key, value�� dict �� �߰��ϴ� ��.
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
	
