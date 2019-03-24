import rrdtool
import os.path

class DataBaseRRDTOOL:
    name = None
    def __init__(self,name):
        self.name = name

    def create(self):
        ret = rrdtool.create(str(self.name),
                     "--start",'N',
                     "--step",'60',
                     "DS:inoctets:COUNTER:600:U:U",
                     "RRA:AVERAGE:0.5:1:2016",
            #RRA:HWPREDICT:rows:alpha:beta:seasonal period[:rra - num]
                     "RRA:HWPREDICT:1000:0.1:0.0035:288:3",
              #RRA:SEASONAL:seasonal period:gamma:rra-num
                     "RRA:SEASONAL:288:0.1:2",
              #RRA:DEVSEASONAL:seasonal period:gamma:rra-num
                     "RRA:DEVSEASONAL:288:0.1:2",
                #RRA:DEVPREDICT:rows:rra-num
                     "RRA:DEVPREDICT:1000:4",
            #RRA:FAILURES:rows:threshold:window length:rra-num
                     "RRA:FAILURES:288:7:9:4")
        if ret:
            print (rrdtool.error())
        else:
            return True
    
    def insert(self,inoctets):
        query = "N:" + str(inoctets)
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
    
    def check_aberration(self):
        """ This will check for begin and end of aberration
            in file. Will return:
            0 if aberration not found.
            1 if aberration begins
            2 if aberration ends
        """
        ab_status = 0

        info = rrdtool.info(str(self.name))
        rrdstep = int(info['step'])
        lastupdate = info['last_update']
        previosupdate = str(lastupdate - rrdstep - 1)

        fmin = int(values[2][0])
        fmax = int(values[2][1])
        flast = int(values[2][2])
        # check if failure value had changed.
        if (fmin != fmax):
            if (flast == 1):
                ab_status = 1
            else:
                ab_status = 2
        return ab_status