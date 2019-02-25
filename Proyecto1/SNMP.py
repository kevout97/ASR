from pysnmp.hlapi import *

class SNMP:
    def __init__(self):
    
    def get(self,community,version_snmp,ip,port,oid):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                CommunityData(community,mpModel=version_snmp),
                UdpTransportTarget((ip, port)),
                ContextData(),
                ObjectType(ObjectIdentity(oid)))
        )
        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    return (' = '.join([x.prettyPrint() for x in varBinds])).split()[2]