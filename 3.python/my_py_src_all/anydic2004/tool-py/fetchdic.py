#!/usr/bin/env python
# -*- coding: EUC-KR -*-
# ������ ���� ��� ���� ����Ÿ�� ������ ���� �⺻ Ŭ���� ����


def isalphaonly(str):
	for ch in str:
		if not ch.isalpha(): return 0
	return 1

NOPHRASE = 0x01
NOCASE = 0x02

class fetchdic:
	
	def __init__(self, dataFile):
		self.finishword = finishword

		try:
			self.dataFd = open(dataFile, 'w')
		except:
			print "failed in writing file : ", indexFile
			return


	
	def __del__(self):
		self.fd.close()

	def main(self):


	def enqueueDoc(self):
		pass

	def processDoc(self):
		pass

	def storeData(self, idxword, sndword, expl):
	# idxword - ǥ����, ���ξ�
	# sndword - second word. ���ξ� �� �����
	# expl - ����, ������ ��
		pass


if __name__ == "__main__":


