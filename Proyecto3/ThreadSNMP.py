import threading
import os.path
import sys
import time
from DataBaseRRDTOOL import DataBaseRRDTOOL
from SNMP import SNMP
import os
from PojoAgent import PojoAgent
from Telegram import Telegram
from Graph import *

class ThreadSNMP:
    thread = None

    def monitoring(self,ip,mainPojo,mainDBRRD,indexInterface,indexCPU):
        snmp = SNMP()
        hostname = mainPojo.getHostname(str(ip))
        community = mainPojo.getCommunity(str(hostname))
        version_snmp = 0 if str(mainPojo.getVersionSNMP(str(hostname))) == "v1" else 1
        port_snmp = int(mainPojo.getPortSNMP(str(hostname)))
        telegram = Telegram("712644612:AAHauTnCsKgno4fOh3z8p9B5fJuOnGC9-tk")
        idChat = "-343597492"
        flag = True
        while True:
            try:
                if os.system("ping -c 1 " + str(ip) +" >/dev/null 2>&1 < /dev/null &") == 0 and mainPojo.getStatus(str(ip)) == "up" and len(str(mainPojo.getStatus(str(ip)))) > 0:
                    inoctets = int(snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.2.1.2.2.1.10.1")) #OID para obtener el total de inoctets
                    mainDBRRD.insert(inoctets)
                    fallas = mainDBRRD.check_aberration()

                    #######Notificacion de Fallas#######
                    try:
                        if int(fallas) == 1 and flag:
                            flag = False
                            graphHW(ip)
                            mensaje = "Falla detectada en el Host :"+ str(ip) +"("+ str(time.strftime("%c")) +")"
                            telegram.sendMessage(mensaje,idChat)
                            telegram.sendImage(str(ip)+"HW.png",idChat)

                        if int(fallas) == 2 and not flag:
                            flag = True
                            graphHW(ip)
                            mensaje = "La falla en el Host :"+ str(ip) +" ha sido mitigada ("+ str(time.strftime("%c")) +")"
                            telegram.sendMessage(mensaje,idChat)
                            telegram.sendImage(str(ip)+"HW.png",idChat)
                    except Exception as a:
                        print(a)
                    time.sleep(60)
                else:
                    mainPojo.setStatus(str(hostname),"down")
                    print("Server is down")
                    break
            except Exception as e:
                pa = PojoAgent("localhost","root","","snmp")
                result = pa.verifyHost(str(ip))
                if len(result) == 0:
                    break
                else:
                    print(e)

    def startMonitoring(self,ip,mainPojo,index,indexCPU):
        if os.path.isfile(str(ip) + ".rrd"):
            self.dbrrd = DataBaseRRDTOOL(str(ip) + ".rrd")
            nameThread = ip + "thread"
            self.thread = threading.Thread(target=self.monitoring, name=nameThread,args=(ip,mainPojo,self.dbrrd,index,indexCPU,))
            self.thread.setDaemon(True)
            self.thread.start()
        else:
            self.dbrrd = DataBaseRRDTOOL(str(ip) + ".rrd")
            self.dbrrd.create()
            nameThread = ip + "thread"
            self.thread = threading.Thread(target=self.monitoring, name=nameThread,args=(ip,mainPojo,self.dbrrd,index,indexCPU,))
            self.thread.setDaemon(True)
            self.thread.start()