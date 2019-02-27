import rrdtool

class DataBaseRRDTOOL:
    name = None
    def __init__(self,name):
        self.name = name

    def create(self):
        ret = rrdtool.create(str(self.name),
                     "--start",'N',
                     "--step",'60',
                     "DS:innetworkinterface:COUNTER:60:U:U",
                     "DS:outnetworkinterface:COUNTER:60:U:U",
                     "DS:inicmp:COUNTER:60:U:U",
                     "DS:outicmp:COUNTER:60:U:U",
                     "DS:intcp:COUNTER:60:U:U",
                     "DS:outtcp:COUNTER:60:U:U",
                     "DS:inudp:COUNTER:60:U:U",
                     "DS:outudp:COUNTER:60:U:U",
                     "DS:inping:COUNTER:60:U:U",
                     "DS:outping:COUNTER:60:U:U",
                     "RRA:AVERAGE:0.5:1:50",
                     "RRA:AVERAGE:0.5:1:50",
                     "RRA:AVERAGE:0.5:1:50",
                     "RRA:AVERAGE:0.5:1:50",
                     "RRA:AVERAGE:0.5:1:50",
                     "RRA:AVERAGE:0.5:1:50",
                     "RRA:AVERAGE:0.5:1:50",
                     "RRA:AVERAGE:0.5:1:50",
                     "RRA:AVERAGE:0.5:1:50", 
                     "RRA:AVERAGE:0.5:1:50")
        if ret:
            print (rrdtool.error())
        else:
            return True
    
    def insert(self,in_network_interface,out_network_interface,in_icmp,out_icmp,in_tcp,out_tcp,in_udp,out_udp,in_ping,out_ping):
        query = "N:" + str(in_network_interface) + ":" + str(out_network_interface) + ":" + str(in_icmp) + ":" + str(out_icmp) + ":" + str(in_tcp) + ":" + str(out_tcp) + ":" + str(in_udp) + ":" + str(out_udp) + ":" + str(in_ping) + ":" + str(out_ping)
        ret = rrdtool.update(self.name, query)
        
        if ret:
            print (rrdtool.error())
        else:
            return True