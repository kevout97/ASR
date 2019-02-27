CREATE DATABASE snmp;

CREATE TABLE snmp.agents (hostname VARCHAR(500) PRIMARY KEY, version_snmp VARCHAR(10), port_snmp INT, community VARCHAR(500), status VARCHAR(10), initial_time INT);
CREATE TABLE snmp.devices (hostname VARCHAR(500) PRIMARY KEY, ip VARCHAR(50), version_so VARCHAR(500), interfaces INT,last_reboot VARCHAR(100),mac VARCHAR(100),info_admin VARCHAR(500));
CREATE TABLE snmp.interfaces (hostname VARCHAR(500) PRIMARY KEY, interface VARCHAR(100), status VARCHAR(50));
