"""
    CS3103, Sem 1 AY1213
    Programming Assignment 2
    Hu Qiang
    A0077857J

    This program is written in Python 3
"""

import sys
import re

class Counter:

    IP = "0800"
    ARP = "0806"
    ICMP = "01"
    TCP = "06"
    UDP = "11"
    Ping_RQ= "08"
    Ping_RP = "00"
    Ping = "ping"
#    DHCP_S = "0043"
#    DHCP_C = "0044"
    DHCP = "0043"
    DNS = "0035"
    C = 0
    N = 0
    B = 0
    dhcpCounter = 0

#vars = {IP :"08 00",
#        ICMP : "01",
#        TCP : "06",
#        UDP :"11",
#        Ping_RQ : "08",
#        Ping_RP : "00",
#        DHCP_S : "00 43",
#        DHCP_C : "00 44",
#        DNS : "00 35"}

    counts = {ARP   : 0,
              IP    : 0,
              ICMP  : 0,
              TCP   : 0,
              UDP   : 0,
              Ping  :0,
#              Ping_RP:0,
              DHCP : 0,
              DNS   : 0}
    output = ""

    dhcpMsgType = {1: "DISCOVER",
                   2: "OFFER",
                   3: "REQUEST",
                   4: "DECLINE",
                   5: "ACK",
                   6: "NACK",
                   7: "RELEASE",
                   8: "INFORM"}
    
    def __init__(self, f):
            self.file = f

    def add(self,n):
            self.counts[n] += 1

    def getName(self, index, arr):
            count = int(arr[index],16)
#            print(" ".join(arr))
            name = ""
            while count != 0:
                    hexStr = ''.join(arr[index+1:index+1+count])
                    name += bytes.fromhex(hexStr).decode('utf-8')+"."
                    index += count + 1
                    count = int(arr[index],16)
            if name:
                return name
            else:
                    return "Not given"

    def getIp(self, arr):
            return ".".join([str(int(x,16)) for x in arr])


    def processTcp(self, arr):
            pass

    def processDhcp(self, arr):
            """
            For IPv4 only
            """
            index = base = 8
            self.dhcpCounter += 1
            self.output += \
"----------------------\n\
DHCP Transaction {}\n\
----------------------\n".format(self.dhcpCounter)
            type = int(arr[index], 16)
            """get message type"""
            if type == 1:
                    self.output += "Message type: request\n"
            elif type == 2:
                    self.output += "Message type: reply\n"
            else:
                    raise Exception("Wrong message type:{}\n"\
                                    .format(type))
            index += 1
            """
            Hardware type
            """
            type = int(arr[index], 16)
            if type == 1:
                    self.output += "Hardware type: Ethernet\n"
            else:
                    self.output += "Hardware type: {}\n"\
                                    .format(type)
            index += 1
            """
            Hadware address length
            """
            hwlen = int(arr[index],16)
            self.output += "Hardware address length: {}\n"\
                            .format(hwlen)
            index += 1

            self.output += "Hops: {}\n".format(int(arr[index],16))
            index += 1

            self.output += "Transaction ID: 0x{}\n"\
                            .format("".join(arr[index:index + 4]))
            index += 4

            self.output += "Seconds elapsed: {}\n"\
                            .format(int(arr[index]+arr[index+1],16))
            index += 2

            flag = int(arr[index]+arr[index+1], 16)
            if flag>>15 == 1:
                    self.output += "Flags: multicast\n"
            else:
                    self.output += "Flags: Unicast\n"
            index += 2

            self.output += "Client IP address: {}.{}.{}.{}\n"\
                            .format(int(arr[index],16),
                                   int(arr[index+1],16),
                                   int(arr[index+2],16),
                                  int(arr[index+3],16))
            index += 4

            self.output += "Your IP address: {}.{}.{}.{}\n"\
                            .format(int(arr[index],16),
                                    int(arr[index+1],16),
                                    int(arr[index+2],16),
                                    int(arr[index+3],16))
            index += 4
            self.output += "Server IP address: {}.{}.{}.{}\n"\
                            .format(int(arr[index],16),
                                    int(arr[index+1],16),
                                    int(arr[index+2],16),
                                    int(arr[index+3],16))
            index += 4

            self.output += "Relay agent IP address: {}.{}.{}.{}\n"\
                            .format(int(arr[index],16),
                                    int(arr[index+1],16),
                                    int(arr[index+2],16),
                                    int(arr[index+3],16))
            index += 4

            self.output += "Client MAC address: "+arr[index]
            for i in range(1,hwlen):
                    self.output += (":"+arr[i])
            self.output += "\n"
            index += 16

            self.output += "Server name: {}\n"\
                            .format(self.getName(index, arr))
            index += 64

            self.output += "Boot file name: {}\n"\
                            .format(self.getName(index, arr))
            index += 128
            
            if arr[index] == "63"\
               and arr[index+1] == "82"\
               and arr[index+2] == "53"\
               and arr[index+3] == "63":
                    self.output += "Magic cookie: DHCP\n"
            else:
                    raise Exception("Sorry, I dont know how to handle it!")
            index += 4

            opcode = int(arr[index], 16)
            while opcode != 255 and opcode != 0:
                    self.output += "Option:\n"
                    if opcode == 53:
                            self.output += "\tLength: 1\n"
                            index += 2
                            type = int(arr[index],16)
                            self.output += "\tDHCP Message Type: {}\n"\
                                           .format(self.dhcpMsgType[type])
                            index += 1
                            opcode = int(arr[index],16)
                    elif opcode == 1:
                            index += 1
                            len = int(arr[index], 16)
                            self.output += "\tLength: {}\n"\
                                            .format(len)
                            self.output += "\tSubnet Mask: {}\n"\
                                            .format(self.getIp(arr[index+1: index+1+len]))
                            index += len + 1
                            opcode = int(arr[index], 16)

                    elif opcode == 3:
                            index += 1
                            len = int(arr[index], 16)
                            self.output += "\tLength: {}\n"\
                                            .format(len)
                            self.output += "\tRouter: {}\n"\
                                            .format(self.getIp(arr[index+1: index+1+len]))
                            index += len + 1
                            opcode = int(arr[index], 16)
                    elif opcode == 6:
                            index += 1
                            len = int(arr[index], 16)
                            self.output += "\tLength: {}\n"\
                                            .format(len)
                            for i in range(int(len/4)):
                                    self.output += "\tDomain Name Server: {}\n"\
                                                    .format(self.getIp(arr[index+1+i*4: index+1+i*4+4]))
                            index += len + 1
                            opcode = int(arr[index], 16)

                    
                    elif opcode == 12:
                            index += 1
                            len = int(arr[index], 16)
                            self.output += "\tLength: {}\n"\
                                            .format(len)
                            self.output += "\tHost Name: {}\n"\
                                            .format(bytes.fromhex("".join(arr[index+1: index+1+len])).decode('utf-8'))
                            index += len + 1
                            opcode = int(arr[index], 16)
                    elif opcode == 15:
                            index += 1
                            len = int(arr[index], 16)
                            self.output += "\tLength: {}\n"\
                                            .format(len)
                            self.output += "\tDomain Name: {}\n"\
                                            .format(bytes.fromhex("".join(arr[index+1: index+1+len])).decode('utf-8'))
                            index += len + 1
                            opcode = int(arr[index], 16)
                    elif opcode == 44:
                            index += 1
                            len = int(arr[index], 16)
                            self.output += "\tLength: {}\n"\
                                            .format(len)
                            for i in range(int(len/4)):
                                    self.output += "\tNetBIOS Over TCP/IP Name Server: {}\n"\
                                                    .format(self.getIp(arr[index+1+i*4: index+1+i*4+4]))
                            index += len + 1
                            opcode = int(arr[index], 16)

                    elif opcode == 50:
                            index += 1
                            len = int(arr[index], 16)
                            self.output += "\tLength: {}\n"\
                                            .format(len)
                            for i in range(int(len/4)):
                                    self.output += "\tRequested IP Address: {}\n"\
                                                    .format(self.getIp(arr[index+1+i*4: index+1+i*4+4]))
                            index += len + 1
                            opcode = int(arr[index], 16)

                    elif opcode == 51:
                            index += 1
                            len = int(arr[index], 16)
                            self.output += "\tLength: {}\n"\
                                            .format(len)
                            self.output += "\tIP Address Lease Time: {}s\n"\
                                            .format(int("".join(arr[index+1: index+1+len]),16))
                            index += len + 1
                            opcode = int(arr[index], 16)
                    elif opcode == 54:
                            index += 1
                            len = int(arr[index], 16)
                            self.output += "\tLength: {}\n"\
                                            .format(len)
                            self.output += "\tDHCP Server IP: {}\n"\
                                            .format(self.getIp(arr[index+1: index+1+len]))
                            index += len + 1
                            opcode = int(arr[index], 16)
                    elif opcode == 55:
                            index += 1
                            len = int(arr[index], 16)
                            self.output += "\tLength: {}\n"\
                                            .format(len)
                            for i in range(len):
                                    key = int(arr[index+1+i],16)
                                    type = ""
                                    if key in self.dhcpMsgType:
                                            type = "DHCP "+self.dhcpMsgType[key]
                                    else:
                                            type = str(key)
                                    self.output += "\tParameter Request List: {}\n"\
                                                    .format(type)
                            index += len + 1
                            opcode = int(arr[index], 16)


                    else:
                            index += 1
                            len = int(arr[index],16)
                            self.output += "\tLength: {}\n"\
                                            .format(len)
                            self.output += """\tMessage Type: {} 
\tThis is currently not implemented\n"""\
                                            .format(opcode)
                            index += len + 1
                            opcode = int(arr[index], 16)
            self.output += "\n"



    def processUdp(self, arr):
            sourcePort = arr[34]+arr[35]
            destinationPort = arr[36]+arr[37]
            if sourcePort == self.DNS or destinationPort == self.DNS:
                    self.add(self.DNS)
            elif sourcePort == self.DHCP or destinationPort == self.DHCP:
                    self.add(self.DHCP)
                    self.processDhcp(arr[34:])


    def processIcmp(self, arr):
            number = arr[34]
            if number == self.Ping_RQ or\
               number == self.Ping_RP:
                    self.add(self.Ping)

    def processIp(self, arr):
            number = arr[23]
            if number == self.ICMP:
                    self.add(number)
                    self.processIcmp(arr)
            elif number == self.TCP:
                    self.add(number)
                    self.processTcp(arr)
            elif number == self.UDP:
                    self.add(number)
                    self.processUdp(arr)



    def processFrame(self,arr):
#            print(self.C)
            self.C += 1
#            print(arr)
            number = arr[12]+arr[13]
            if number == self.IP:
#                    print(self.C)
                    self.add(number)
                    self.processIp(arr)
            elif number == self.ARP:
                    self.add(number)
            else:
                    self.N += 1

    def skipPackage(self):
            line = file.readline()
            while line == "\n":#skip mpty lines
                    line = file.readline()
            while True: #skip the block
                    if line == "\n" or line == "":
                            return
                    else:
                            line = file.readline()
            return 
    
    def validLine(self, line):
            if not bool(re.compile(r'[^a-f0-9]').search(line[0:4])):
                    return True
            elif line[0:5] == "Frame":
                    return False
            else:
                    self.skipPackage()
                    return False
 
    def run(self):
            str = ""
            shouldCheck = True
            while True:
                     line = file.readline();
                     if line == "":
                             self.processFrame(str.strip().split())
                             print ("total number of packages = {}"\
                                    .format(self.C))
                             self.output = "total number of DHCP packets = {}\n\n".\
                                    format(self.counts[self.DHCP]) + self.output
                             print(self.output)
                             return
                     elif line != "\n":
                             if shouldCheck: #Only check the begining of a frame
                                     if self.validLine(line):
                                             str += line[6:-19]
                                             shouldCheck = False
                                     else:
                                             shouldCheck = True
                                             str = ""
                             else:
                                     str += line[6:-19]
                     elif line == "\n" and str != "":
                             self.processFrame(str.strip().split())
                             shouldCheck = True
                             str = ""

           



if __name__ == "__main__":
        file = open(sys.argv[1], "r")
        c =Counter(file)
        c.run()
        if len(sys.argv) == 3:
                out_file = open(sys.argv[2], "w+")
                out_file.write(c.output)
                out_file.close()