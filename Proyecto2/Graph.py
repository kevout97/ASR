import sys
import rrdtool
import time
from PojoAgent import PojoAgent

#tiempo_actual = int(time.time())
#tiempo_final = tiempo_actual - 86400
#tiempo_inicial = tiempo_final -25920000

def graphCPU(ip):
    ultima_lectura = int(rrdtool.last(ip +".rrd"))
    tiempo_final = 1539667800 + (3600 * 2)
    tiempo_inicial = ultima_lectura - 3600
    

    ret = rrdtool.graph( ip+"CPU.png",
                        "--start","1539656263",
                        "--end",str(tiempo_final),
                        "--vertical-label=Carga CPU",
                        "--title=Uso de CPU Host: "+str(ip),
                        "--color", "ARROW#009900",
                        '--vertical-label', "Uso de CPU (%)",
                        '--lower-limit', '0',
                        '--upper-limit', '100',
                        '--width', '600', 
                        '--height', '240',
                        "DEF:carga="+ip+".rrd:CPUload:AVERAGE",
                        "CDEF:umbral90=carga,90,LT,0,carga,IF",
                        "AREA:carga#00FF00:Carga CPU\\n",
                        "LINE1:30",
                        "AREA:5#ff000022:stack\\n",
                        "VDEF:CPUlast=carga,LAST",
                        "VDEF:CPUmin=carga,MINIMUM",
                        "VDEF:CPUavg=carga,AVERAGE",
                        "VDEF:CPUmax=carga,MAXIMUM",
                        "AREA:umbral90#EA0000:Trafico de carga mayor que 90\\n",
                        "HRULE:90#FF0000:Umbral - 90%\\n",
                        "GPRINT:CPUlast:%12.0lf%s LAST",
                        "GPRINT:CPUmin:%10.0lf%s MIN",
                        "GPRINT:CPUavg:%13.0lf%s AVG",
                        "GPRINT:CPUmax:%13.0lf%s MAX\\n",
                        "VDEF:m=carga,LSLSLOPE",
                        "VDEF:b=carga,LSLINT",
                        'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                        "CDEF:prediccion=tendencia,90,100,LIMIT",
                        "VDEF:prediccionFIRST=prediccion,FIRST",
                        "VDEF:prediccionLAST=prediccion,LAST",
                        "GPRINT:prediccionFIRST: Umbral 90%  @ %c \\n:strftime",
                        "LINE2:tendencia#FFBB00" )

def graphRAM(ip):
    ultima_lectura = int(rrdtool.last(ip +".rrd"))
    tiempo_final = ultima_lectura + (3600 * 2)
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
                        '--width', '600', 
                        '--height', '240',
                        "DEF:carga="+ip+".rrd:ramload:AVERAGE",
                        "CDEF:umbral90=carga,80,LT,0,carga,IF",
                        "CDEF:prediccion=carga,80,100,LIMIT",
                        "VDEF:prediccionFIRST=prediccion,FIRST",
                        "VDEF:prediccionLAST=prediccion,LAST",
                        "AREA:carga#00FF00:Uso de RAM\\n",
                        "LINE1:30",
                        "AREA:5#ff000022:stack\\n",
                        "VDEF:CPUlast=carga,LAST",
                        "VDEF:CPUmin=carga,MINIMUM",
                        "VDEF:CPUavg=carga,AVERAGE",
                        "VDEF:CPUmax=carga,MAXIMUM",
                        "AREA:umbral90#EA0000:Trafico de carga mayor que 80\\n",
                        "HRULE:30#00FF50:Umbral 1 - 30%\\n",
                        "HRULE:40#CA6048:Umbral 1 - 40%\\n",
                        "HRULE:80#FF0000:Umbral 1 - 80%\\n",
                        "GPRINT:CPUlast:%12.0lf%s LAST",
                        "GPRINT:CPUmin:%10.0lf%s MIN",
                        "GPRINT:CPUavg:%13.0lf%s AVG",
                        "GPRINT:CPUmax:%13.0lf%s MAX\\n",
                        "GPRINT:prediccionFIRST: Umbral 80%  @ %c \\n:strftime",
                        "VDEF:m=carga,LSLSLOPE",
                        "VDEF:b=carga,LSLINT",
                        'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                        "LINE2:tendencia#FFBB00" )

def graphHDD(ip):
    ultima_lectura = int(rrdtool.last(ip +".rrd"))
    tiempo_final = ultima_lectura + (3600 * 2)
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
                        '--width', '600', 
                        '--height', '240',
                        "DEF:carga="+ip+".rrd:hddload:AVERAGE",
                        "CDEF:umbral90=carga,90,LT,0,carga,IF",
                        "AREA:carga#00FF00:Uso de HDD\\n",
                        "LINE1:30",
                        "AREA:5#ff000022:stack\\n",
                        "VDEF:CPUlast=carga,LAST",
                        "VDEF:CPUmin=carga,MINIMUM",
                        "VDEF:CPUavg=carga,AVERAGE",
                        "VDEF:CPUmax=carga,MAXIMUM",
                        "AREA:umbral90#EA0000:Trafico de carga mayor que 90\\n",
                        "CDEF:prediccion=carga,90,100,LIMIT",
                        "VDEF:prediccionFIRST=prediccion,FIRST",
                        "VDEF:prediccionLAST=prediccion,LAST",
                        "HRULE:70#00FF50:Umbral 1 - 70%\\n",
                        "HRULE:80#CA6048:Umbral 1 - 80%\\n",
                        "HRULE:90#FF0000:Umbral 1 - 90%\\n",
                        "GPRINT:CPUlast:%12.0lf%s LAST",
                        "GPRINT:CPUmin:%10.0lf%s MIN",
                        "GPRINT:CPUavg:%13.0lf%s AVG",
                        "GPRINT:CPUmax:%13.0lf%s MAX\\n",
                        "GPRINT:prediccionFIRST: Umbral 90%  @ %c \\n:strftime",
                        "GPRINT:prediccionLAST: Umbral 100%  @ %c :strftime",
                        "VDEF:m=carga,LSLSLOPE",
                        "VDEF:b=carga,LSLINT",
                        'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                        "LINE2:tendencia#FFBB00" )
