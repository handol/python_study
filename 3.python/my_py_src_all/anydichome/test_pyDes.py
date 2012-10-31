import pyDes
import base64

k = pyDes.des("HANDOL00", pyDes.CBC, "\0\0\0\0\0\0\0\0")
d = k.encrypt("Please  ")
d = base64.b64encode(d)
print "Encypted string: " + d
d = base64.b64decode(d)
print "Decypted string: " + k.decrypt(d)

k = pyDes.triple_des("MySecretTripleDesKeyData")
d = k.encrypt("Please  ", "*")
d = base64.b64encode(d)
print "Encypted string: " + d
d = base64.b64decode(d)
print "Decypted string: " + k.decrypt(d, "*")

