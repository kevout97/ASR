import os
from PojoAgent import PojoAgent
from SNMP import SNMP

def dispositivosRegistrados():

 
def menu():
    os.system('clear')
    dispositivosRegistrados()
    print ("Selecciona una opcion")
    print ("\t1 - Agregar Agente")
    print ("\t2 - Eliminar Agente")
    print ("\t3 - Estado de Dispositivo")
    print ("\t4 - Graficas")
    print ("\tq - Salir")

def agregarAgente(): #Falta lanzar el hilo que monitorea al agente
    os.system('clear')
    hostname = ""
    status = ""
    version_snmp = ""
    port_snmp = ""
    community = ""
    pa = PojoAgent("localhost","root","","snmp")#Conexion con la base de datos
    snmp = SNMP()
    hostname = raw_input("Introduce el hostname del agente: ")
    while True:
        result = pa.getHostname(str(hostname))
        if len(result[0]) > 0:
            print("El hostname ya se encuentra registrado.")
            hostname = raw_input("Introduce el hostname del agente: ")
        else:
            status = "up" if os.system("ping -c 1 " + str(hostname)) == 0 else "down"
            version_snmp = raw_input("Introduce la version de snmp ('v1' o 'v2c'): ")
            port_snmp = int(raw_input("Introduce el puerto snmp: "))
            community = raw_input("Introduce la comunidad: ")
            break
    version_snmp = "0" if str(version_snmp) == "v1" else "1"

    oid = "" #Oid para obtener la IP del agente
    ip = snmp.get(str(community),int(version_snmp),str(hostname),int(port_snmp),str(oid))

    oid = "" #Oid para obtener la version de SO
    version_so = snmp.get(str(community),int(version_snmp),str(hostname),int(port_snmp),str(oid))

    oid = "" #Oid para obtener el numero de interfaces
    interfaces = snmp.get(str(community),int(version_snmp),str(hostname),int(port_snmp),str(oid))

    oid = "" #Oid para obtener el ultimo reinicio
    last_reboot = snmp.get(str(community),int(version_snmp),str(hostname),int(port_snmp),str(oid))

    oid = "" #Oid para obtener la direccion fisica
    mac = snmp.get(str(community),int(version_snmp),str(hostname),int(port_snmp),str(oid))

    oid = "" #Oid para obtener informacion del administrador
    info_admin = snmp.get(str(community),int(version_snmp),str(hostname),int(port_snmp),str(oid))
    
    pa.insertAgent(str(hostname),str(version_snmp),port_snmp,str(community),str(status),str(ip),str(version_so),int(interfaces),str(last_reboot),str(mac),str(info_admin))
    pa.closeConnection()
    raw_input("El agente "+ str(hostname) +" ha sido agregado....presiona una tecla para regresar al menu >>")

def eliminarAgente():
    hostname = raw_input("Introduce el hostname del agente: ")
    while True:
        result = pa.getHostname(str(hostname))
        if len(result[0]) == 0:
            print("El hostname no existe.")
            hostname = raw_input("Introduce el hostname del agente: ")
        else:
            pa = PojoAgent("localhost","root","","snmp")#Conexion con la base de datos
            pa.deleteAgent(str(hostname))
            pa.closeConnection()
            raw_input("El agente ha sido eliminado....presiona una tecla para regresar al menu >>")
            break


def estadoDispositivo():
    hostname = raw_input("Introduce el hostname del agente: ")
    while True:
        result = pa.getHostname(str(hostname))
        if len(result[0]) == 0:
            print("El hostname no existe.")
            hostname = raw_input("Introduce el hostname del agente: ")
        else:
            pa = PojoAgent("localhost","root","","snmp")#Conexion con la base de datos
            ip = pa.getIP(str(hostname))
            print("Hostname:\t"+ str(hostname) +"\nIP:\t" + str(pa.getIP(str(hostname))) +"\nVersion SO:\t"+ str(pa.getVersionSO(str(hostname))) +"\nNumero Interfaces:\t"+ str(pa.getInterfaces(str(hostname),str(ip))) +"\nUltimo Reinicio:\t"+ str(pa.getLastReboot(str(hostname),str(ip))) +"\nMAC:\t"+ str(pa.getMac(str(hostname),str(ip))) +"\nInfo. Admin:\t"+ str(pa.getInfoAdmin(str(hostname),str(ip))))
            pa.closeConnection()
            raw_input("Presiona una tecla para regresar al menu >>")
            break


def graficas():


while True:
    menu()
    opcionMenu = raw_input("Selecciona una opcion >> ")
    if str(opcionMenu)=="1":
        agregarAgente()
    elif str(opcionMenu)=="2":
        eliminarAgente()
    elif str(opcionMenu)=="3":
        estadoDispositivo()
    elif (str(opcionMenu)=="q" or str(opcionMenu)=="Q"):
        break
    else:
        raw_input("Opcion incorrecta...\npulsa una tecla para continuar")