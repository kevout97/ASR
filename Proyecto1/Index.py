import os
import subprocess
from PojoAgent import PojoAgent
from SNMP import SNMP
from ThreadSNMP import ThreadSNMP

def dispositivosRegistrados(flag):
    print("Dispositivos\n###############################################################################")
    pa = PojoAgent("localhost","root","","snmp")#Conexion con la base de datos
    paux = PojoAgent("localhost","root","","snmp")#Conexion con la base de datos
    hosts = pa.getAllHosts()
    for i in range(0,len(hosts)):
        if flag and os.system("ping -c 1 " + str(hosts[i][0]) +" >/dev/null 2>&1 < /dev/null &") == 0:
            ip = str(pa.getIP(str(hosts[i][0])))
            index = str(pa.getIndex(str(ip)))
            pa.setStatus(str(hosts[i][0]),"up")
            thread = ThreadSNMP()
            thread.startMonitoring(str(ip),paux,str(index))
        else:
            ip = str(pa.getIP(str(hosts[i][0])))
            status = str(pa.getStatus(str(ip)))
            if status == "down" and os.system("ping -c 1 " + str(hosts[i][0]) +" >/dev/null 2>&1 < /dev/null &") == 0:
                index = str(pa.getIndex(str(ip)))
                thread = ThreadSNMP()
                thread.startMonitoring(str(ip),paux,str(index))
            elif os.system("ping -c 1 " + str(hosts[i][0]) +" >/dev/null 2>&1 < /dev/null &") == 1:
                pa.setStatus(str(hosts[i][0]),"down")
    
    for i in range(0,len(hosts)):
        print("Dispositivo: "+ str(i+1))
        print("Hostname: "+ str(hosts[i][0]))
        print("Numero de Interfaces: "+str(pa.getInterfaces(str(hosts[i][0]),pa.getIP(str(hosts[i][0])))))
        print("###############################################################################") 
def menu(flag):
    os.system("clear")
    dispositivosRegistrados(flag)
    print("Menu Graficas")
    print("\t1 - Agregar Agente")
    print("\t2 - Eliminar Agente")
    print("\t3 - Estado de Dispositivo")
    print("\t4 - Graficas")
    print("\tq - Salir")

def menuGraficas():
    os.system('clear')
    print ("Menu Principal")
    print ("\t1 - Trafico Interfaz de red")
    print ("\t2 - Estadisticas ICMP")
    print ("\t3 - Estadisticas TCP")
    print ("\t4 - Estadisticas UDP")
    print ("\t5 - Estadisticas Ping")
    print ("\tq - Salir")

def agregarAgente():
    os.system('clear')
    hostname = ""
    status = ""
    version_snmp = ""
    port_snmp = ""
    community = ""
    index = ""
    pa = PojoAgent("localhost","root","","snmp")#Conexion con la base de datos
    paux = PojoAgent("localhost","root","","snmp")#Conexion con la base de datos
    snmp = SNMP()
    hostname = raw_input("Introduce el hostname del agente: ")
    agent = "y"
    while agent == "y" or agent == "Y":
        if str(hostname) == "q" or str(hostname) == "Q":
            break
        else:
            result = pa.verifyHost(str(hostname))
            if len(result) > 0:
                print("El hostname ya se encuentra registrado.")
                hostname = raw_input("Introduce el hostname del agente: ")
            else:
                status = "up" if os.system("ping -c 1 " + str(hostname) +" >/dev/null 2>&1 < /dev/null &") == 0 else "down"
                version_snmp = raw_input("Introduce la version de snmp ('v1' o 'v2c'): ")
                if str(version_snmp) == "q" or str(version_snmp) == "Q":
                    break
                else:
                    port_snmp = raw_input("Introduce el puerto snmp: ")
                    if str(port_snmp) == "q" or str(port_snmp) == "Q":
                        break
                    else:
                        community = raw_input("Introduce la comunidad: ")
                        if str(community) == "q" or str(community) == "Q":
                            break
                        else:
                            index = raw_input("Introduce el index de la interfaz de red del agente: ")
                            if str(index) == "q" or str(index) == "Q":
                                break
        version_snmp = "0" if str(version_snmp) == "v1" else "1"

        ip = str(subprocess.check_output("cat /etc/hosts | grep \""+ str(hostname) +"\" | awk '{print $1}'",shell=True)).split("\n")[0]
        if len(str(ip)) == 0:
            ip = str(subprocess.check_output("dig '"+ str(hostname) +"' +short",shell=True)).split("\n")[0]

        oid = "1.3.6.1.2.1.1.1.0" #Oid para obtener la version de SO
        version_so = snmp.get(str(community),int(version_snmp),str(hostname),str(port_snmp),str(oid))

        oid = "1.3.6.1.2.1.2.1.0" #Oid para obtener el numero de interfaces
        interfaces = snmp.get(str(community),int(version_snmp),str(hostname),str(port_snmp),str(oid))

        oid = "1.3.6.1.2.1.1.3.0" #Oid para obtener el ultimo reinicio
        last_reboot = snmp.get(str(community),int(version_snmp),str(hostname),str(port_snmp),str(oid))

        oid = "1.3.6.1.2.1.1.6.0" #Oid para obtener la direccion fisica
        mac = snmp.get(str(community),int(version_snmp),str(hostname),str(port_snmp),str(oid))

        oid = "1.3.6.1.2.1.1.4.0" #Oid para obtener informacion del administrador
        info_admin = snmp.get(str(community),int(version_snmp),str(hostname),str(port_snmp),str(oid))

        pa.insertAgent(str(hostname),str(version_snmp),port_snmp,str(community),str(status),str(ip),str(version_so),int(interfaces),str(last_reboot),str(mac),str(info_admin),str(index))
        thread = ThreadSNMP()
        thread.startMonitoring(str(ip),paux,str(index))
        pa.closeConnection()
        agent = str(raw_input("El agente "+ str(hostname) +" ha sido agregado...Desea agregar otro agente? ('y' o 'n') >>"))

def eliminarAgente():
    hostname = raw_input("Introduce el hostname del agente: ")
    pa = PojoAgent("localhost","root","","snmp")#Conexion con la base de datos
    while True:
        if str(hostname) == "q" or str(hostname) == "Q":
            break
        else:
            result = pa.verifyHost(str(hostname))
            if len(result[0]) == 0:
                print("El hostname no existe.")
                hostname = raw_input("Introduce el hostname del agente: ")
            else:
                ip = pa.getIP(str(hostname))
                pa.deleteAgent(str(hostname), str(ip))
                pa.closeConnection()
                raw_input("El agente ha sido eliminado....presiona una tecla para regresar al Menu >>")
                break


def estadoDispositivo():
    hostname = raw_input("Introduce el hostname del agente: ")
    pa = PojoAgent("localhost","root","","snmp")#Conexion con la base de datos
    while True:
        if str(hostname) == "q" or str(hostname) == "Q":
            break
        else:
            result = pa.verifyHost(str(hostname))
            if len(result) == 0:
                print("El hostname no existe.")
                hostname = raw_input("Introduce el hostname del agente: ")
            else:
                ip = pa.getIP(str(hostname))
                print("Hostname:           "+ str(hostname) +"\nIP:                 " + str(pa.getIP(str(hostname))) +"\nVersion SO:        "+ str(pa.getVersionSO(str(hostname),str(ip))) +"\nNumero Interfaces:  "+ str(pa.getInterfaces(str(hostname),str(ip))) +"\nUltimo Reinicio:   "+ str(pa.getLastReboot(str(hostname),str(ip))) +"\nUbicacion Fisica:  "+ str(pa.getMac(str(hostname),str(ip))) +"\nInfo. Admin:       "+ str(pa.getInfoAdmin(str(hostname),str(ip))))
                pa.closeConnection()
                raw_input("Presiona una tecla para regresar al menu >>")
                break


def graficas():
    while True:
        menuGraficas()
        opcionMenu = raw_input("Selecciona una opcion >> ")
        if str(opcionMenu)=="1":
            print("Grafica Trafico de Interfaz de red")
        elif str(opcionMenu)=="2":
            print("Grafica ICMP")
        elif str(opcionMenu)=="3":
            print("Grafica TCP")
        elif str(opcionMenu)=="4":
            print("Graficas UDP")
        elif str(opcionMenu)=="4":
            print("Graficas Ping")
        elif (str(opcionMenu)=="q" or str(opcionMenu)=="Q"):
            print("")
            break
        else:
            raw_input("Opcion incorrecta...pulsa una tecla para continuar >>")

flag = True
while True:
    menu(flag)
    flag = False
    opcionMenu = raw_input("Selecciona una opcion >> ")
    if str(opcionMenu)=="1":
        agregarAgente()
    elif str(opcionMenu)=="2":
        eliminarAgente()
    elif str(opcionMenu)=="3":
        estadoDispositivo()
    elif str(opcionMenu)=="4":
        print("Graficas")
    elif (str(opcionMenu)=="q" or str(opcionMenu)=="Q"):
        print("")
        break
    else:
        raw_input("Opcion incorrecta...pulsa una tecla para continuar >>")
