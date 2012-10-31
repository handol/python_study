import hashlib

a = hashlib.sha1()
a.update('8')
print a.hexdigest()

import base64

for i in range(20):  
    print "%d ==> %s" % (i, base64.b64encode(str(i)))
