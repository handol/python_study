import md5

PHR = "handol hooray"
m = md5.new(PHR)
enc = m.hexdigest()
print enc
m = md5.new(enc)
print m.hexdigest()
