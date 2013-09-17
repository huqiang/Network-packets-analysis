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
    output = ""

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
    
    def __init__(self, f):
            self.file = f

    def add(self,n):
            self.counts[n] += 1

    def processTcp(self, arr):
            pass

    def processUdp(self, arr):
            sourcePort = arr[34]+arr[35]
            destinationPort = arr[36]+arr[37]
            if sourcePort == self.DNS or destinationPort == self.DNS:
                    self.add(self.DNS)
            elif sourcePort == self.DHCP or destinationPort == self.DHCP:
                    self.add(self.DHCP)


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
                             self.output +="total number of packages = {}\n"\
                                    .format(self.C)
                             self.output += "total number of Ethernet (IP + ARP) packets = {}\n"\
                                    .format((self.counts[self.IP]+self.counts[self.ARP]))

                             self.output += "total number of IP packets = {}\n".\
                                    format(self.counts[self.IP])
                             self.output += "total number of ARP packets = {}\n".\
                                    format(self.counts[self.ARP])
                             self.output += "total number of ICMP packets = {}\n".\
                                    format(self.counts[self.ICMP])
                             self.output += "total number of TCP packets = {}\n".\
                                    format(self.counts[self.TCP])
                             self.output += "total number of UDP packets = {}\n".\
                                    format(self.counts[self.UDP])
                             self.output += "total number of Ping packets = {}\n".\
                                    format(self.counts[self.Ping])
                             self.output += "total number of DHCP packets = {}\n".\
                                    format(self.counts[self.DHCP])
                             self.output += "total number of DNS packets = {}\n".\
                                    format(self.counts[self.DNS])
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