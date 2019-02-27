import sys
import rrdtool
import time
from PojoAgent import PojoAgent

#tiempo_actual = int(time.time())
#tiempo_final = tiempo_actual - 86400
#tiempo_inicial = tiempo_final -25920000

def graphNetInt(ip):
    pa = PojoAgent("localhost","root","","snmp")#Conexion con la base de datos
    start = pa.getStart(ip);
    ret = rrdtool.graph( ip+"TraficoInterfazRed.png",
                    "--start", str(start),
#                   "--end","N",
                    "--vertical-label=Bytes/s",
                    "DEF:innetworkinterface="+ip+".rrd:innetworkinterface:AVERAGE",
                    "DEF:outnetworkinterface="+ip+".rrd:outnetworkinterface:AVERAGE",
                    "AREA:innetworkinterface#00FF00:In traffic",
                    "LINE1:outnetworkinterface#0000FF:Out traffic\r")
    return ret

def graphICMP(ip):
    pa = PojoAgent("localhost","root","","snmp")#Conexion con la base de datos
    start = pa.getStart(ip);
    ret = rrdtool.graph( ip+"ICMP.png",
                    "--start", str(start),
#                   "--end","N",
                    "--vertical-label=Bytes/s",
                    "DEF:inicmp="+ip+".rrd:inicmp:AVERAGE",
                    "DEF:outicmp="+ip+".rrd:outicmp:AVERAGE",
                    "AREA:inicmp#00FF00:In traffic",
                    "LINE1:outicmp#0000FF:Out traffic\r")
    return ret

def graphTCP(ip):
    pa = PojoAgent("localhost","root","","snmp")#Conexion con la base de datos
    start = pa.getStart(ip);
    ret = rrdtool.graph( ip+"TCP.png",
                    "--start", str(start),
#                   "--end","N",
                    "--vertical-label=Bytes/s",
                    "DEF:intcp="+ip+".rrd:intcp:AVERAGE",
                    "DEF:outtcp="+ip+".rrd:outtcp:AVERAGE",
                    "AREA:intcp#00FF00:In traffic",
                    "LINE1:outtcp#0000FF:Out traffic\r")
    return ret

def graphUDP(ip):
    pa = PojoAgent("localhost","root","","snmp")#Conexion con la base de datos
    start = pa.getStart(ip);
    ret = rrdtool.graph( ip+"UDP.png",
                    "--start", str(start),
#                   "--end","N",
                    "--vertical-label=Bytes/s",
                    "DEF:inudp="+ip+".rrd:inudp:AVERAGE",
                    "DEF:outudp="+ip+".rrd:outudp:AVERAGE",
                    "AREA:inudp#00FF00:In traffic",
                    "LINE1:outudp#0000FF:Out traffic\r")
    return ret

def graphPing(ip):
    pa = PojoAgent("localhost","root","","snmp")#Conexion con la base de datos
    start = pa.getStart(ip);
    ret = rrdtool.graph( ip+"Ping.png",
                    "--start", str(start),
#                   "--end","N",
                    "--vertical-label=Bytes/s",
                    "DEF:inping="+ip+".rrd:inping:AVERAGE",
                    "DEF:outping="+ip+".rrd:outping:AVERAGE",
                    "AREA:inping#00FF00:In traffic",
                    "LINE1:outping#0000FF:Out traffic\r")
    return ret