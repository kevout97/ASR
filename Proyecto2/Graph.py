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
    start = pa.getStart(ip)
    ret = rrdtool.graph( ip+"Ping.png",
                    "--start", str(start),
#                   "--end","N",
                    "--vertical-label=Bytes/s",
                    "DEF:inping="+ip+".rrd:inping:AVERAGE",
                    "DEF:outping="+ip+".rrd:outping:AVERAGE",
                    "AREA:inping#00FF00:In traffic",
                    "LINE1:outping#0000FF:Out traffic\r")
    return ret

def graphCPU(ip):
    ultima_lectura = int(rrdtool.last(ip +".rrd"))
    tiempo_final = ultima_lectura + 3600
    tiempo_inicial = ultima_lectura - 3600

    ret = rrdtool.graph( ip+"CPU.png",
                        "--start",str(tiempo_inicial),
                        "--end",str(tiempo_final),
                        "--vertical-label=Carga CPU",
                        "--title=Uso de CPU Host: "+str(ip),
                        "--color", "ARROW#009900",
                        '--vertical-label', "Uso de CPU (%)",
                        '--lower-limit', '0',
                        '--upper-limit', '100',
                        "DEF:carga="+ip+".rrd:cpuload:AVERAGE",
                        "AREA:carga#00FF00:Carga CPU",
                        "LINE1:30",
                        "AREA:5#ff000022:stack",
                        "VDEF:CPUlast=carga,LAST",
                        "VDEF:CPUmin=carga,MINIMUM",
                        "VDEF:CPUavg=carga,AVERAGE",
                        "VDEF:CPUmax=carga,MAXIMUM",

                        "COMMENT:Now          Min             Avg             Max\n",
                        "GPRINT:CPUlast:%12.0lf%s",
                        "GPRINT:CPUmin:%10.0lf%s",
                        "GPRINT:CPUavg:%13.0lf%s",
                        "GPRINT:CPUmax:%13.0lf%s",
                        "VDEF:m=carga,LSLSLOPE",
                        "VDEF:b=carga,LSLINT",
                        'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                        "LINE2:tendencia#FFBB00" )

def graphRAM(ip):
    ultima_lectura = int(rrdtool.last(ip +".rrd"))
    tiempo_final = ultima_lectura + 3600
    tiempo_inicial = ultima_lectura - 3600

    ret = rrdtool.graph( ip+"RAM.png",
                        "--start",str(tiempo_inicial),
                        "--end",str(tiempo_final),
                        "--vertical-label=Uso de RAM",
                        "--title=Uso de RAM Host: "+str(ip),
                        "--color", "ARROW#009900",
                        '--vertical-label', "Uso de RAM (%)",
                        '--lower-limit', '0',
                        '--upper-limit', '100',
                        "DEF:carga="+ip+".rrd:ramload:AVERAGE",
                        "AREA:carga#00FF00:Uso de RAM",
                        "LINE1:30",
                        "AREA:5#ff000022:stack",
                        "VDEF:CPUlast=carga,LAST",
                        "VDEF:CPUmin=carga,MINIMUM",
                        "VDEF:CPUavg=carga,AVERAGE",
                        "VDEF:CPUmax=carga,MAXIMUM",

                        "COMMENT:Now          Min             Avg             Max\n",
                        "GPRINT:CPUlast:%12.0lf%s",
                        "GPRINT:CPUmin:%10.0lf%s",
                        "GPRINT:CPUavg:%13.0lf%s",
                        "GPRINT:CPUmax:%13.0lf%s",
                        "VDEF:m=carga,LSLSLOPE",
                        "VDEF:b=carga,LSLINT",
                        'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                        "LINE2:tendencia#FFBB00" )

def graphHDD(ip):
    ultima_lectura = int(rrdtool.last(ip +".rrd"))
    tiempo_final = ultima_lectura + 3600
    tiempo_inicial = ultima_lectura - 3600

    ret = rrdtool.graph( ip+"HDD.png",
                        "--start",str(tiempo_inicial),
                        "--end",str(tiempo_final),
                        "--vertical-label=Uso de HDD",
                        "--title=Uso de HDD Host: "+str(ip),
                        "--color", "ARROW#009900",
                        '--vertical-label', "Uso de HDD (%)",
                        '--lower-limit', '0',
                        '--upper-limit', '100',
                        "DEF:carga="+ip+".rrd:hddload:AVERAGE",
                        "AREA:carga#00FF00:Uso de HDD",
                        "LINE1:30",
                        "AREA:5#ff000022:stack",
                        "VDEF:CPUlast=carga,LAST",
                        "VDEF:CPUmin=carga,MINIMUM",
                        "VDEF:CPUavg=carga,AVERAGE",
                        "VDEF:CPUmax=carga,MAXIMUM",

                        "COMMENT:Now          Min             Avg             Max\n",
                        "GPRINT:CPUlast:%12.0lf%s",
                        "GPRINT:CPUmin:%10.0lf%s",
                        "GPRINT:CPUavg:%13.0lf%s",
                        "GPRINT:CPUmax:%13.0lf%s",
                        "VDEF:m=carga,LSLSLOPE",
                        "VDEF:b=carga,LSLINT",
                        'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                        "LINE2:tendencia#FFBB00" )
