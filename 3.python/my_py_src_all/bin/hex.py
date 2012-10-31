#!/usr/bin/python
# -*- coding: cp949 -*-

import sys

if len(sys.argv) is 1:
  print >> sys.stderr, '���� ���ϸ��� �Է��� �ּ���'
  exit(1)

try:
  IN = open(sys.argv[1], 'rb') # ���� ����
except IOError:
  print >> sys.stderr, '�׷� ������ ���ų�, ���� �����Դϴ�.'
  exit(1)

offset = 0 # ���� ���� �ʱ�ȭ


while True: # ���� ����
  buf16 = IN.read(16) # ������ 16����Ʈ�� �о� ���ۿ� ����
  buf16Len = len(buf16) # ������ ���� ũ�� �˾Ƴ���
  if buf16Len == 0: break

  output = "%08X:  " % (offset) # Offset(����)��, ��� ���ۿ� ����

  for i in range(buf16Len): # ��� �κ��� ��� �� 16�� ��� (8���� 2�κ�����)
    if (i == 8): output += " " # 8���� �и�
    output += "%02X " % (ord(buf16[i])) # ��� �� ���

  for i in range( ((16 - buf16Len) * 3) + 1 ): # �� ���� 16 ����Ʈ�� ���� ���� ��, ��� �κа� ���� �κ� ���̿� ����� ����
    output += " "
  if (buf16Len < 9):
    output += " " # ������ 9����Ʈ���� ���� ���� ��ĭ �� ����

  for i in range(buf16Len): # ���� ���� ���
    if (ord(buf16[i]) >= 0x20 and ord(buf16[i]) <= 0x7E): # Ư�� ���� �ƴϸ� �״�� ���
      output += buf16[i]
    else: output += "." # Ư������, �׷��ȹ��� ���� ��ħǥ�� ���


  offset += 16 # ���� ���� 16 ����
  print output # 1�� �з��� ��� ���� ���ڿ��� �� ���۸� ���



if (offset == 0):
  print "%08X:  " % (offset) # 0����Ʈ ������ ��� ó��

IN.close # ���� �ݱ�

