from pysnmp.hlapi import *

class SNMP:
    def __init__(self):
    
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