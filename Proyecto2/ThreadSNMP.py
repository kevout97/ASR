import threading
import os.path
import sys
import time
from DataBaseRRDTOOL import DataBaseRRDTOOL
from SNMP import SNMP
import os
from PojoAgent import PojoAgent
from Telegram import Telegram

class ThreadSNMP:
    thread = None

    def monitoring(self,ip,mainPojo,mainDBRRD,indexInterface,indexCPU):
        snmp = SNMP()
        hostname = mainPojo.getHostname(str(ip))
        community = mainPojo.getCommunity(str(hostname))
        version_snmp = 0 if str(mainPojo.getVersionSNMP(str(hostname))) == "v1" else 1
        port_snmp = int(mainPojo.getPortSNMP(str(hostname)))
        telegram = Telegram("712644612:AAHauTnCsKgno4fOh3z8p9B5fJuOnGC9-tk")
        #telegram.sendMessage(mensaje,"-343597492")
        idChat = "-343597492"
        while True:
            try:
                if mainPojo.ifWindows(ip):
                    if os.system("ping -c 1 " + str(ip) +" >/dev/null 2>&1 < /dev/null &") == 0 and mainPojo.getStatus(str(ip)) == "up" and len(str(mainPojo.getStatus(str(ip)))) > 0:
                        indexRAM = mainPojo.getIndexRAM(str(ip))
                        indexHDD = mainPojo.getIndexHDD(str(ip))
                        cpuload = snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.2.1.25.3.3.1.2."+ str(indexCPU)) #OID para calcular promedio del ultimo minuto del porcentaje que el procesador no estuvo inactivo
                        freeram = int(snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.2.1.25.2.3.1.6."+ str(indexRAM))) #OID para obtener la memoria RAM disponible en kB
                        usehdd = int(snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.2.1.25.2.3.1.6."+ str(indexHDD))) #OID para obtener la cantidad de Disco Duro usado.
                        totalram = int(snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.2.1.25.2.3.1.5."+ str(indexRAM))) #OID para obtener el total de la RAM
                        totalhdd = int(snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.2.1.25.2.3.1.5."+ str(indexHDD))) #OID para obtener el total del HDD
                        hddload = (usehdd * 100)/totalhdd #Cantidad de Disco Duro en Porcentaje
                        ramload = ((totalram - freeram) * 100)/totalram #Cantidad de RAM en porcentaje
                        mainDBRRD.insert(cpuload,ramload,hddload)
                        #######Establecer umbrales#######
                        if int(ramload) > 50:
                            mensaje = "Porcentaje de *RAM* utilizada por el Host "+ str(ip) +": *"+ str(ramload) + " %* ("+ str(time.strftime("%c")) +")"
                            telegram.sendMessage(mensaje,idChat)
                        if int(hddload) > 50:
                            mensaje = "Porcentaje de *HDD* utilizado por el Host "+ str(ip) +": *"+ str(hddload) + " %* ("+ str(time.strftime("%c")) +")"
                            telegram.sendMessage(mensaje,idChat)
                        if int(cpuload) > 50:
                            mensaje = "Porcentaje de *CPU* utilizado por el Hots "+ str(ip) +": *"+ str(cpuload) + " %* ("+ str(time.strftime("%c")) +")"
                            telegram.sendMessage(mensaje,idChat)
                        time.sleep(1)
                    else:
                        mainPojo.setStatus(str(hostname),"down")
                        print("Server is down")
                        break
                else:
                    if os.system("ping -c 1 " + str(ip) +" >/dev/null 2>&1 < /dev/null &") == 0 and mainPojo.getStatus(str(ip)) == "up" and len(str(mainPojo.getStatus(str(ip)))) > 0:
                        cpuload = snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.2.1.25.3.3.1.2."+ str(indexCPU)) #OID para calcular promedio del ultimo minuto del porcentaje que el procesador no estuvo inactivo
                        freeram = int(snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.4.1.2021.4.6.0")) #OID para obtener la memoria RAM disponible en kB
                        usehdd = int(snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.4.1.2021.9.1.8.1")) #OID para obtener la cantidad de Disco Duro usado. En linux agregar disk / 1 en snmpd.conf
                        totalram = int(snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.2.1.25.2.2.0")) #OID para obtener el total de la RAM
                        totalhdd = int(snmp.get(community,version_snmp,ip,port_snmp,"1.3.6.1.4.1.2021.9.1.11.1")) #OID para obtener el total del HDD
                        hddload = (usehdd * 100)/totalhdd #Cantidad de Disco Duro en Porcentaje
                        ramload = ((totalram - freeram) * 100)/totalram #Cantidad de RAM en porcentaje
                        mainDBRRD.insert(cpuload,ramload,hddload)
                        #######Establecer umbrales#######
                        if int(ramload) > 50:
                            mensaje = "Porcentaje de *RAM* utilizada por el Host "+ str(ip) +": *"+ str(ramload) + " %* ("+ str(time.strftime("%c")) +")"
                            telegram.sendMessage(mensaje,idChat)
                        if int(hddload) > 50:
                            mensaje = "Porcentaje de *HDD* utilizado por el Host "+ str(ip) +": *"+ str(hddload) + " %* ("+ str(time.strftime("%c")) +")"
                            telegram.sendMessage(mensaje,idChat)
                        if int(cpuload) > 50:
                            mensaje = "Porcentaje de *CPU* utilizado por el Hots "+ str(ip) +": *"+ str(cpuload) + " %* ("+ str(time.strftime("%c")) +")"
                            telegram.sendMessage(mensaje,idChat)
                        time.sleep(1)
                    else:
                        mainPojo.setStatus(str(hostname),"down")
                        print("Server is down")
                        break
            except:
                pa = PojoAgent("localhost","root","","snmp")
                result = pa.verifyHost(str(ip))
                if len(result) == 0:
                    break
                else:
                    print("Ocurrio un error")
                #print("Unexpected error:"+ str(sys.exc_info()[0]))

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