import rrdtool
from pysnmp.hlapi import *

def get(self,community,version_snmp,ip,port,oid):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                CommunityData(str(community),mpModel=version_snmp),
                UdpTransportTarget((str(ip), port)),
                ContextData(),
                ObjectType(ObjectIdentity(str(oid))))
        )
        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                result = str(varBind).split("=")
                return result[1]

intcp = get("comunidadEquipo1_grupo4cm1",1,"localhost",161,"1.3.6.1.2.1.6.10.0")
outtcp = get("comunidadEquipo1_grupo4cm1",1,"localhost",161,"1.3.6.1.2.1.6.11.0")
query = "N:"+ str(intcp) +":"+ str(outtcp) + ""
ret = rrdtool.create("parctica2.rrd",
                     "--start", 'N',
                     "DS:intcp:COUNTER:600:U:U",
                     "DS:outtcp:COUNTER:600:U:U",
                     "RRA:AVERAGE:0.5:1:24",
                     "RRA:AVERAGE:0.5:6:10")

gra= rrdtool.graph("practica2.png",
                   "--start", "N",
                   "--end", "920808000",
                   "DEF:practica2.rrd:intcp:AVERAGE",
                   "DEF:practica2.rrd:outtcp:AVERAGE",
                   "LINE1:myspeed#FF0000")