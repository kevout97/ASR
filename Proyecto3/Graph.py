import sys
import rrdtool
import time
from PojoAgent import PojoAgent


def graphHW(ip):
    ultima_lectura = int(rrdtool.last(ip +".rrd"))
    tiempo_final = ultima_lectura + 3600
    tiempo_inicial = ultima_lectura - 3600

    # El 86400 es el tiempo en segundos correspondientes a un dia
    tiempo_inicial_pasado = tiempo_inicial - 86400
    tiempo_final_pasado = tiempo_final - 86400
    
    ret = rrdtool.graph( ip+"HW.png",
                        "--start",str(tiempo_inicial),
                        "--end",str(tiempo_final),
                        "--vertical-label=Bytes/s",
                        "--title=Deteccion de comportamiento anomalo, valor de Alpha 0.1 Host: "+str(ip),
                        "--color", "ARROW#009900",
                        '--width', '600', 
                        '--height', '240',
                        '--slope-mode', 
                        "DEF:observado=" + str(ip) + ".rrd:inoctets:AVERAGE",
                        "DEF:hwpredict=" + str(ip) + ".rrd:inoctets:HWPREDICT",
                        "DEF:devpredict=" + str(ip) + ".rrd:inoctets:DEVPREDICT",
                        "DEF:failures=" + str(ip) + ".rrd:inoctets:FAILURES",
                        "DEF:yvalue="+str(ip) + ".rrd:inoctets:AVERAGE:start="+str(tiempo_inicial_pasado)+":end="+str(tiempo_final_pasado),
                        'SHIFT:yvalue:86400',
                        "CDEF:scaledobs=observado,8,*",
                        "CDEF:scaledyvalue=yvalue,8,*",
                        "CDEF:upper=hwpredict,devpredict,2,*,+",
                        "CDEF:lower=hwpredict,devpredict,2,*,-",
                        "CDEF:scaledupper=upper,8,*",
                        "CDEF:scaledlower=lower,8,*",
                        "CDEF:scaledpred=hwpredict,8,*",
                        'AREA:scaledyvalue#C0C0C0:"Pasado\:"',
                        "TICK:failures#FDD017:1.0:Fallas",
                        "LINE3:scaledobs#00FF00:In traffic",
                        "LINE1:scaledpred#FF00FF:Prediccion\\n",
                        "LINE1:scaledupper#ff0000:Upper Bound Average bits in\\n",
                        "LINE1:scaledlower#0000FF:Lower Bound Average bits in")
