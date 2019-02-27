import sys
import rrdtool
import time
from PojoAgent import PojoAgent

#tiempo_actual = int(time.time())
#tiempo_final = tiempo_actual - 86400
#tiempo_inicial = tiempo_final -25920000
start = getStart(ip);

def graphNetInt(ip):
    ret = rrdtool.graph( ip+"TraficoInterfazRed.png",
                    "--start", str(start),
#                   "--end","N",
                    "--vertical-label=Bytes/s",
                    "DEF:in_network_interface="+ip+".rrd:in_network_interface:AVERAGE",
                    "DEF:out_network_interface="+ip+".rrd:out_network_interface:AVERAGE",
                    "AREA:in_network_interface#00FF00:In traffic",
                    "LINE1:out_network_interface#0000FF:Out traffic\r")
    return ret

def graphICMP(ip):
    ret = rrdtool.graph( ip+"ICMP.png",
                    "--start", str(start),
#                   "--end","N",
                    "--vertical-label=Bytes/s",
                    "DEF:in_icmp="+ip+".rrd:in_icmp:AVERAGE",
                    "DEF:out_icmp="+ip+".rrd:out_icmp:AVERAGE",
                    "AREA:in_icmp#00FF00:In traffic",
                    "LINE1:out_icmp#0000FF:Out traffic\r")
    return ret

def graphTCP(ip):
    ret = rrdtool.graph( ip+"TCP.png",
                    "--start", str(start),
#                   "--end","N",
                    "--vertical-label=Bytes/s",
                    "DEF:in_tcp="+ip+".rrd:in_tcp:AVERAGE",
                    "DEF:out_tcp="+ip+".rrd:out_tcp:AVERAGE",
                    "AREA:in_tcp#00FF00:In traffic",
                    "LINE1:out_tcp#0000FF:Out traffic\r")
    return ret

def graphUDP(ip):
    ret = rrdtool.graph( ip+"UDP.png",
                    "--start", str(start),
#                   "--end","N",
                    "--vertical-label=Bytes/s",
                    "DEF:in_udp="+ip+".rrd:in_udp:AVERAGE",
                    "DEF:out_udp="+ip+".rrd:out_udp:AVERAGE",
                    "AREA:in_udp#00FF00:In traffic",
                    "LINE1:out_udp#0000FF:Out traffic\r")
    return ret

def graphPing(ip):
    ret = rrdtool.graph( ip+"Ping.png",
                    "--start", str(start),
#                   "--end","N",
                    "--vertical-label=Bytes/s",
                    "DEF:in_ping="+ip+".rrd:in_ping:AVERAGE",
                    "DEF:out_ping="+ip+".rrd:out_ping:AVERAGE",
                    "AREA:in_ping#00FF00:In traffic",
                    "LINE1:out_ping#0000FF:Out traffic\r")
    return ret