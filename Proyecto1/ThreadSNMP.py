import threading
import os.path
import time
from DataBaseRRDTOOL import DataBaseRRDTOOL
from SNMP import SNMP

class ThreadSNMP:
    thread = None

    def monitoring(self,ip,mainPojo,mainDBRRD,index):
        snmp = SNMP()
        hostname = mainPojo.getHostname(str(ip))
        community = mainPojo.getCommunity(str(hostname))
        version_snmp = 0 if str(mainPojo.getVersionSNMP(str(hostname))) == "v1" else 1
        port_snmp = int(mainPojo.getPortSNMP(str(hostname)))
        while True:
            if os.system("ping -c 1 " + str(ip) +" >/dev/null 2>&1 < /dev/null &") == 0 and mainPojo.getStatus(str(ip)) == "up" and len(str(mainPojo.geStatus(str(ip)))) > 0:
                in_network_interface = snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.2.1.2.2.1.10."+ str(index))
                out_network_interface = snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.2.1.2.2.1.16."+ str(index))
                in_icmp = snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.2.1.5.1.0")
                out_icmp = snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.2.1.5.14.0")
                in_tcp = snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.2.1.6.10.0")
                out_tcp = snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.2.1.6.11.0")
                in_udp = snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.2.1.7.1.0")
                out_udp = snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.2.1.7.4.0")
                in_ping = int(snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.2.1.5.8.0")) #The number of ICMP Echo (request) messages received.
                in_ping += int(snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.2.1.5.9.0")) #The number of ICMP Echo Reply messages received.
                out_ping = int(snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.2.1.5.21.0")) #The number of ICMP Echo (request) messages sent.
                out_ping += int(snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.2.1.5.22.0")) #The number of ICMP Echo Reply messages sent.
                mainDBRRD.insert(in_network_interface,out_network_interface,in_icmp,out_icmp,in_tcp,out_tcp,in_udp,out_udp,in_ping,out_ping)
                time.sleep(1)
            else:
                print("")
                break

    def startMonitoring(self,ip,mainPojo,index):
        if os.path.isfile(str(ip) + ".rrd"):
            self.dbrrd = DataBaseRRDTOOL(str(ip) + ".rrd")
            nameThread = ip + "thread"
            self.thread = threading.Thread(target=self.monitoring, name=nameThread,args=(ip,mainPojo,self.dbrrd,index,))
            self.thread.setDaemon(True)
            self.thread.start()
        else:
            self.dbrrd = DataBaseRRDTOOL(str(ip) + ".rrd")
            self.dbrrd.create()
            nameThread = ip + "thread"
            self.thread = threading.Thread(target=self.monitoring, name=nameThread,args=(ip,mainPojo,self.dbrrd,index,))
            self.thread.setDaemon(True)
            self.thread.start()
    
    def stopMonitoring(self,ip):
        nameThread = ip + "thread"
        self.thread = threading.Thread(name=nameThread)
        if self.thread.isAlive():
            self.thread._stop()