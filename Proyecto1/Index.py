import os
from PojoAgent import PojoAgent
from SNMP import SNMP

def dispositivosRegistrados():

 
def menu():
    os.system('clear')
    print ("Selecciona una opcion")
    print ("\t1 - Agregar Agente")
    print ("\t2 - Eliminar Agente")
    print ("\t3 - Estado de Dispositivo")
    print ("\t4 - Graficas")
    print ("\tq - Salir")

def agregarAgente():
    os.system('clear')
    hostname = ""
    status = ""
    version_snmp = ""
    port_snmp = ""
    community = ""
    pa = PojoAgent("localhost","root","","snmp")
    snmp = SNMP()
    hostname = raw_input("Introduce el hostname o ip del agente ('q' para salir): ")
    while True:
        result = pa.getHostname(str(hostname))
        if len(result[0]) > 0:
            print("El hostname ya se encuentra registrado.")
            hostname = raw_input("Introduce el hostname o ip del agente: ")
        else:
            status = "up" if os.system("ping -c 1 " + str(hostname)) == 0 else "down"
            version_snmp = raw_input("Introduce la version de snmp ('v1' o 'v2c'): ")
            port_snmp = int(raw_input("Introduce el puerto snmp: "))
            community = raw_input("Introduce la comunidad: ")
            break
    version_snmp = "0" if str(version_snmp) == "v1" else "1"

    oid = ""
    ip = snmp.get(str(community),int(version_snmp),str(hostname),int(port_snmp),str(oid))

    oid = ""
    version_so = snmp.get(str(community),int(version_snmp),str(hostname),int(port_snmp),str(oid))

    oid = ""
    interfaces = snmp.get(str(community),int(version_snmp),str(hostname),int(port_snmp),str(oid))

    oid = ""
    last_reboot = snmp.get(str(community),int(version_snmp),str(hostname),int(port_snmp),str(oid))

    oid = ""
    mac = snmp.get(str(community),int(version_snmp),str(hostname),int(port_snmp),str(oid))

    oid = ""
    info_admin = snmp.get(str(community),int(version_snmp),str(hostname),int(port_snmp),str(oid))
    
    pa.insertAgent(str(hostname),str(version_snmp),port_snmp,str(community),str(status),str(ip),str(version_so),int(interfaces),str(last_reboot),str(mac),str(info_admin))
def eliminarAgente():

def estadoDispositivo():

def graficas():


while True:
    menu()
    opcionMenu = raw_input("Selecciona una opcion >> ")
    if str(opcionMenu)=="1":
        raw_input("Has pulsado la opcion 1...\npulsa una tecla para continuar")
    elif str(opcionMenu)=="2":
        print ("")
        raw_input("Has pulsado la opcion 2...\npulsa una tecla para continuar")
    elif str(opcionMenu)=="3":
        print ("")
        raw_input("Has pulsado la opcion 3...\npulsa una tecla para continuar")
    elif (str(opcionMenu)=="q" or str(opcionMenu)=="Q"):
        break
    else:
        raw_input("Opcion incorrecta...\npulsa una tecla para continuar")