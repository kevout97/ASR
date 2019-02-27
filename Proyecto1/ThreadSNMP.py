import threading
import os.path
import time
from DataBaseRRDTOOL import DataBaseRRDTOOL
from SNMP import SNMP

class ThreadSNMP:
    thread

    def monitoring(self,ip,mainPojo,mainDBRRD):
        snmp = SNMP()
        hostname = self.mainPojo.getHostname(str(ip))
        community = self.mainPojo.getCommunity(str(hostname))
        version_snmp = 0 if str(self.pojo.getVersionSNMP(str(hostname))) == "v1" else 1
        port_snmp = int(self.pojo.getPortSNMP(str(hostname)))
        while True:
            in_network_interface = snmp.get(community,version_snmp,ip,port_snmp,"")
            out_network_interface = snmp.get(community,version_snmp,ip,port_snmp,"")
            in_icmp = snmp.get(community,version_snmp,ip,port_snmp,"")
            out_icmp = snmp.get(community,version_snmp,ip,port_snmp,"")
            in_tcp = snmp.get(community,version_snmp,ip,port_snmp,"")
            out_tcp = snmp.get(community,version_snmp,ip,port_snmp,"")
            in_udp = snmp.get(community,version_snmp,ip,port_snmp,"")
            out_udp = snmp.get(community,version_snmp,ip,port_snmp,"")
            in_ping = snmp.get(community,version_snmp,ip,port_snmp,"")
            out_ping = snmp.get(community,version_snmp,ip,port_snmp,"")
            mainDBRRD.insert(in_network_interface,out_network_interface,in_icmp,out_icmp,in_tcp,out_tcp,in_udp,out_udp,in_ping,out_ping)
            time.sleep(1)

    def startMonitoring(self,ip,mainPojo):
        if os.path.isfile(ip + ".rrd"):
            self.dbrrd = DataBaseRRDTOOL(ip + ".rrd")
            nameThread = ip + "thread"
            self.thread = threading.Thread(target=self.monitoring, name=nameThread,args=(ip,mainPojo,self.dbrrd,))
            self.thread.setDaemon(True)
            self.thread.start()
        else:
            self.dbrrd = DataBaseRRDTOOL(ip + ".rrd")
            self.dbrrd.create()
            nameThread = ip + "thread"
            self.thread = threading.Thread(target=self.monitoring, name=nameThread,args=(ip,mainPojo,self.dbrrd,))
            self.thread.setDaemon(True)
            self.thread.start()
        return self.thread
    
    def stopMonitoring(self,ip):
        nameThread = ip + "thread"
        self.thread = threading.Thread(name=nameThread)
        if self.thread.isAlive():
            self.thread._stop()