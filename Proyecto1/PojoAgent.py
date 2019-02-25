from DataBaseMysql import DBClass
class PojoAgent:
    private db

    def __init__(self,host,user,passwd,database):
        self.db = DBClass(host,user,passwd,database)
    
    def insertAgent(self,hostname,version_snmp,port_snmp,community,status,ip,version_so,interfaces,last_reboot,mac,info_admin)
        query = "INSERT INTO agents (hostname,version_snmp,port_snmp,community,status) VALUES ('" + hostname + "','" + version_snmp + "'," + port_snmp +",'" + community +"','"+ status +"')"
        self.db.insertUpdateDelete(query)
        query = "INSERT INTO devices (hostname,ip,version_so,interfaces,last_reboot,mac,info_admin) VALUES ('"+ hostname +"','"+ ip +"','"+ version_so +"',"+ interfaces +",'"+ last_reboot +"','"+ mac +"','"+ info_admin +"')"
        self.db.insertUpdateDelete(query)
    
    def getAllAgentsDevices(self):
        query = "SELECT agents.hostname,version_snmp,port_snmp,community,ip,version_so,interfaces,last_reboot,mac,info_admin FROM agents, devices WHERE agents.hostname=devices.hostname"
        return self.db.executeSelect(query)
    
    def getAllHosts(self):
        query = "SELECT hostname FROM agents"
        return self.db.executeSelect(query)
    
    def getHostname(self,hostname):
        query = "SELECT count(*) FROM agents WHERE hostname='"+ hostname +"'"
        return self.db.executeSelect(query)

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
        query = "DELETE FROM devices WHERE hostname='"+ hostname +"' AND ip='" + ip + "'"
        self.db.insertUpdateDelete(query)
    
    def setStatus(self,hostname,status):
        query = "UPDATE agents SET status='"+ status +"' WHERE hostname='"+ hostname +"'"
        self.db.insertUpdateDelete(query)