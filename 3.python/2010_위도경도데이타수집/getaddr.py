from xml.dom import minidom
import urllib.request
import time
def getaddr(x, y):
    #x=37.4
    #y=127.2
    url = 'http://kr.open.gugi.yahoo.com/service/rgc.php?appid=YahooDemo&latitude=37.4997677193116&longitude=127.3094189453125&output=xml'
    url = 'http://kr.open.gugi.yahoo.com/service/rgc.php?appid=YahooDemo&latitude=%f&longitude=%f&output=xml' % (x, y)
    #print (url)
    handle = urllib.request.urlopen(url)
    data = handle.read().decode('utf-8')
    #print (data)
    #xmldoc = minidom.parse('binary.xml')
    xmldoc = minidom.parseString(data)
    reflist = xmldoc.getElementsByTagName('Found')
    if reflist:
        for node in reflist:
            #print (node.toxml(), node.nodeName, node.firstChild.data, node.attributes)
            pass
    else:
        return None

    try:        
        state = xmldoc.getElementsByTagName('state')
        county = xmldoc.getElementsByTagName('county')
        town = xmldoc.getElementsByTagName('town')        
        state = state[0].firstChild.data
        county = county[0].firstChild.data
        town = town[0].firstChild.data
        return state, county, town
    except:
        return None
    



north=38.20
south=33.21
west=126.35
east=128.36
s,c,t = getaddr(37.4, 127.2)
print (s, c,t)

x=west


stepx = (east - west) / 300
stepy = (north - south) / 400

#stepx = 0.5
#stepy = 0.5

outf = open('addr.csv', 'w')
while x <= east:
    y=south
    while y <= north:
        print (y,x)
        res = getaddr(y,x)
        if res:
            s, c,t = res             
            sss = '%f\t%f\t%s\t%s\t%s\n' % (y, x, s, c, t)
            #outf.write(y, '\t', x, '\t', s, '\t',c, '\t',t )
            outf.write(sss)
        else:
            pass        
        y += stepy
        time.sleep(0.01)
    x += stepx

outf.close()

