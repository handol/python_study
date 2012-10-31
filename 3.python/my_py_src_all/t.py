import sys

def printList(alist, blist=[]):
    if not len(alist): print ''.join(blist)
    for i in range(len(alist)):
        blist.append(alist.pop(i))
        printList(alist, blist)
        alist.insert(i, blist.pop())

if __name__ == '__main__':
    k='love'
    if len(sys.argv)>1: k = sys.argv[1]
    printList(list(k))
