from DataBaseMysql import DBClass
import os
class PojoAgent:
    db = None

    def __init__(self,host,user,passwd,database):
        self.db = DBClass(host,user,passwd,database)
    
    def insertAgent(self,hostname,version_snmp,port_snmp,community,status,ip,version_so,interfaces,last_reboot,mac,info_admin,index):
        query = "INSERT INTO agents (hostname,version_snmp,port_snmp,community,status,initial_time,indice) VALUES ('" + hostname + "','" + version_snmp + "'," + str(port_snmp) +",'" + community +"','"+ status +"',UNIX_TIMESTAMP(NOW()),"+ index +")"
        self.db.insertUpdateDelete(query)
        query = "INSERT INTO devices (hostname,ip,version_so,interfaces,last_reboot,mac,info_admin) VALUES ('"+ hostname +"','"+ ip +"','"+ version_so +"',"+ str(interfaces) +",'"+ last_reboot +"','"+ mac +"','"+ info_admin +"')"
        self.db.insertUpdateDelete(query)
        print("Insert hecho")
    
    def getAllAgentsDevices(self):
        query = "SELECT agents.hostname,version_snmp,port_snmp,community,ip,version_so,interfaces,last_reboot,mac,info_admin FROM agents, devices WHERE agents.hostname=devices.hostname"
        return self.db.executeSelect(query)
    
    def getStart(self,ip):
        query = "SELECT agents.initial_time FROM agents, devices WHERE agents.hostname=devices.hostname AND devices.ip='"+ ip +"'"
        result = self.db.executeSelect(query)
        return result[0][0]
    
    def getAllHosts(self):
        query = "SELECT hostname FROM agents"
        return self.db.executeSelect(query)
    
    def getIndex(self,ip):
        query = "SELECT agents.indice FROM agents, devices WHERE agents.hostname=devices.hostname AND devices.ip='"+ ip +"'"
        result = self.db.executeSelect(query)
        return result[0][0]
    
    def verifyHost(self,hostname):
        query = "SELECT hostname FROM agents WHERE hostname='" + hostname + "'"
        return self.db.executeSelect(query)
    
    def getIP(self,hostname):
        query = "SELECT ip FROM agents, devices WHERE agents.hostname=devices.hostname"
        result = self.db.executeSelect(query)
        return result[0][0]

    def getHostname(self,ip):
        query = "SELECT agents.hostname FROM agents, devices WHERE agents.hostname=devices.hostname AND devices.ip='"+ ip +"'"
        result = self.db.executeSelect(query)
        return result[0][0]

    def getVersionSNMP(self,hostname):
        query = "SELECT version_snmp FROM agents WHERE hostname='" + hostname + "'"
        result = self.db.executeSelect(query)
        return result[0][0]

    def getPortSNMP(self,hostname):
        query = "SELECT port_snmp FROM agents WHERE hostname='" + hostname + "'"
        result = self.db.executeSelect(query)
        return result[0][0]

    def getCommunity(self,hostname):
        query = "SELECT community FROM agents WHERE hostname='" + hostname + "'"
        result = self.db.executeSelect(query)
        return result[0][0]
    
    def getIP(self,hostname):
        query = "SELECT ip FROM devices WHERE hostname='" + hostname + "'"
        result = self.db.executeSelect(query)
        return result[0][0]

    def getVersionSO(self,hostname,ip):
        query = "SELECT version_so FROM devices WHERE hostname='" + hostname + "' AND ip='" + ip + "'"
        result = self.db.executeSelect(query)
        return result[0][0]

    def getInterfaces(self,hostname,ip):
        query = "SELECT interfaces FROM devices WHERE hostname='" + hostname + "' AND ip='" + ip + "'"
        result = self.db.executeSelect(query)
        return result[0][0]

    def getLastReboot(self,hostname,ip):
        query = "SELECT last_reboot FROM devices WHERE hostname='" + hostname + "' AND ip='" + ip + "'"
        result = self.db.executeSelect(query)
        return result[0][0]

    def getMac(self,hostname,ip):
        query = "SELECT mac FROM devices WHERE hostname='" + hostname + "' AND ip='" + ip + "'"
        result = self.db.executeSelect(query)
        return result[0][0]

    def getInfoAdmin(self,hostname,ip):
        query = "SELECT info_admin FROM devices WHERE hostname='" + hostname + "' AND ip='" + ip + "'"
        result = self.db.executeSelect(query)
        return result[0][0]
    
    def closeConnection(self):
        self.db.closeConnection()
    
    def deleteAgent(self,hostname,ip):
        query = "DELETE FROM agents WHERE hostname='"+ hostname +"'"
        self.db.insertUpdateDelete(query)
        query = "DELETE FROM devices WHERE hostname='"+ hostname +"'"
        self.db.insertUpdateDelete(query)
        os.system("rm -f "+ ip +".rrd")
    
    def setStatus(self,hostname,status):
        query = "UPDATE agents SET status='"+ status +"' WHERE hostname='"+ hostname +"'"
        self.db.insertUpdateDelete(query)
    
    def getStatus(self,ip):
        query = "SELECT status FROM agents, devices WHERE agents.hostname=devices.hostname AND devices.ip='" + ip + "'"
        result = self.db.executeSelect(query)
        return result[0][0]