#!/usr/bin/python

HOST='localhost'
ROCOMM='public'
PORT=161
OID=(1, 3, 6, 1, 2, 1, 1, 1, 0)

from pysnmp.entity.rfc3413.oneliner import cmdgen

cg = cmdgen.CommandGenerator()
comm_data = cmdgen.CommunityData(HOST, ROCOMM)
transport = cmdgen.UdpTransportTarget((HOST, PORT))
errIndication, errStatus, errIndex, result = cg.getCmd(comm_data,
                                                       transport,
                                                       OID)
print 'errIndication:', errIndication
print 'errStatus:', errStatus
print 'errInde:', errIndex
print 'result: ', result
