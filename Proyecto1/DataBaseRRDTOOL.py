import rrdtool

class DataBaseRRDTOOL:
    name = None
    def __init__(self,name):
        self.name = name

    def create(self):
        ret = rrdtool.create(str(self.name),
                     "--start",'N', #Tiempo de inicio
                     "--step",'60', #Tiempo en el que se actualizara la base de datos
                     "DS:in_network_interface:COUNTER:60:U:U", #Trafico de Interfaz de red (entrada)
                     "DS:out_network_interface:COUNTER:60:U:U", #Trafico de Interfaz de red (salida)
                     "DS:in_icmp:COUNTER:60:U:U", #Estadisticas ICMP (entrada)
                     "DS:out_icmp:COUNTER:60:U:U", #Estadisticas ICMP (salida)
                     "DS:in_tcp:COUNTER:60:U:U", #Estadisticas TCP (entrada)
                     "DS:out_tcp:COUNTER:60:U:U", #Estadisticas TCP (Salida)
                     "DS:in_udp:COUNTER:60:U:U", #Estadisticas UDP (entrada)
                     "DS:out_udp:COUNTER:60:U:U", #Estadisticas UDP (salida)
                     "DS:in_ping:COUNTER:60:U:U", #Estadisticas Ping (entrada)
                     "DS:out_ping:COUNTER:60:U:U", #Estadisticas Ping (salida)
                     "RRA:AVERAGE:0.5:1:50",
                     "RRA:AVERAGE:0.5:1:50",
                     "RRA:AVERAGE:0.5:1:50",
                     "RRA:AVERAGE:0.5:1:50",
                     "RRA:AVERAGE:0.5:1:50",
                     "RRA:AVERAGE:0.5:1:50",
                     "RRA:AVERAGE:0.5:1:50",
                     "RRA:AVERAGE:0.5:1:50",
                     "RRA:AVERAGE:0.5:1:50", 
                     "RRA:AVERAGE:0.5:1:50")
        if ret:
            print (rrdtool.error())
        else:
            return True
    
    def insert(self,in_network_interface,out_network_interface,in_icmp,out_icmp,in_tcp,out_tcp,in_udp,out_udp,in_ping,out_ping):
        query = "N:" + str(in_network_interface) + ":" + str(out_network_interface) + ":" + str(in_icmp) + ":" + str(out_icmp) + ":" + str(in_tcp) + ":" + str(out_tcp) + ":" + str(in_udp) + ":" + str(out_udp) + ":" + str(in_ping) + ":" + str(out_ping)
        ret = rrdtool.update(self.name, query)
        
        if ret:
            print (rrdtool.error())
        else:
            return True