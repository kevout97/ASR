import rrdtool

class DataBaseRRDTOOL:
    name = None
    def __init__(self,name):
        self.name = name

    def create(self):
        ret = rrdtool.create(str(self.name),
                     "--start",'N',
                     "--step",'60',
                     "DS:cpuload:GAUGE:600:U:U",
                     "DS:ramload:GAUGE:600:U:U",
                     "DS:hddload:GAUGE:600:U:U",
                     "RRA:AVERAGE:0.5:1:50")
        if ret:
            print (rrdtool.error())
        else:
            return True
    
    def insert(self,cpuload,ramload,hddload):
        query = "N:" + str(cpuload) + ":" + str(ramload) + ":" + str(hddload)
        ret = rrdtool.update(self.name, query)
        
        if ret:
            print (rrdtool.error())
        else:
            return True
    
    def createXML(self):
        ret = rrdtool.dump(str(self.name)+'.rrd',str(self.name)+'.xml')
        if ret:
            print (rrdtool.error())
        else:
            return True