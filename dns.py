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
    DNSTran = 0
    output=""

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
    dnsType = {1:"A",
               2:"NS",
               5:"CNAME",
               6:"SOA",
               11:"WKS",
               12:"PTR",
               13:"HINFO",
               15:"MX",
               28:"AAAA",
               252:"AXFR",
               255:"ANY"}
    
    def __init__(self, f):
            self.file = f

    def add(self,n):
            self.counts[n] += 1

    def processTcp(self, arr):
            pass

    def isResponse(self, dns):
            return int(dns[10]+dns[11], 16)>>15

    def isAResponse(self, arr):
            isResponse = self.isResponse(arr)
            index = 20
            count = int(arr[index],16)
            while count != 0:
                    index += count + 1
                    count = int(arr[index],16)
            index += 1
            type = int(arr[index]+arr[index+1], 16)
            return isResponse and type == 1

    def getNameAndIndex(self, index, arr):
            count = int(arr[index],16)
#            print(" ".join(arr))
            name = ""
            while count != 0:
                    if count != int("c0",16):
                            hexStr = ''.join(arr[index+1:index+1+count])
                            name += bytes.fromhex(hexStr).decode('utf-8')+"."
                            index += count + 1
                            count = int(arr[index],16)
                    else:
                            name += self.getNameAndIndex(8+int(arr[index+1],16), arr)["name"]
                            index += 1
                            break

            return {"name":name, "newIndex":index}


    def processDns(self, arr):
            #nonlocal output
            base = 8
            if self.isResponse(arr):
                    self.DNSTran += 1
            if self.isAResponse(arr):
                    self.output += \
"----------------------\n\
DNS Transaction\n\
----------------------\n"
                    len = int(arr[4]+arr[5], 16)
                    numOfQ = int(arr[base+4]+arr[base+5],16)
                    numOfA = int(arr[base+6]+arr[base+7],16)
                    numOfAuRR = int(arr[base+8]+arr[base+9],16)
                    numOfAdRR = int(arr[base+10]+arr[base+11],16)
                    self.output += \
"transaction_id =  {}\n\
Questions =  {}\n\
Answer RRs =  {}\n\
Authority RRs =  {}\n\
Additional RRs =  {}\n".format(arr[base]+arr[base+1],
                               numOfQ, 
                               numOfA, 
                               numOfAuRR, 
                               numOfAdRR)
                    index = base + 12
                    self.output +="Queries:\n"
                    for i in range(numOfQ):
                            R = self.getNameAndIndex(index, arr)
                            name = R["name"]
                            index = R['newIndex']
                            self.output += "\tName = {}\n\tType = {}\n\tClass = {}\n\n".\
                                                 format(name,
                                                        int(arr[index+1]+arr[index+2],16),
                                                        int(arr[index+3]+arr[index+4],16),
                                                       )
                            index += 5 #new index
                    self.output += "Answers:\n"
                    for i in range(numOfA):
                            if arr[index] == "c0":
                                    index2 = base + int(arr[index+1],16)
                                    R = self.getNameAndIndex(index2, arr)
                                    name = R["name"]
                                    type = int(arr[index+2]+arr[index+3],16)
                                    classNum = int(arr[index+4]+arr[index+5],16) 
                                    ttl = int("".join(arr[index+6:index+10]),16)
                                    dataLen = int(arr[index+10]+arr[index+11],16)
                                    self.output += "\tName = {}\n\tType = {}\n\tClass = {}\n\
\tTime to live = {}\n\
\tData length =  {}\n".format(name,
                                                        type,
                                                        classNum,
                                                        ttl,
                                                        dataLen
                                                       )
                                    index += 12
                                    if self.dnsType[type] == "A":
                                            self.output += "\tAddr: {}.{}.{}.{}\n\n"\
                                                            .format(int(arr[index],16),
                                                                    int(arr[index+1],16),
                                                                    int(arr[index+2],16),
                                                                    int(arr[index+3],16))
                                    elif self.dnsType[type] == "CNAME":
                                            R = self.getNameAndIndex(index, arr)
#                                            index = R["newIndex"]
                                            name = R["name"]
                                            self.output += "\tCNAME: "+name+"\n\n"
                                    else:
                                            print(arr)
                                            raise Exception("More type {} is not handled!"\
                                                           .format(self.dnsType[type]))
                            index += dataLen #new index
                    




    def processUdp(self, arr):
            sourcePort = arr[34]+arr[35]
            destinationPort = arr[36]+arr[37]
            if sourcePort == self.DNS or destinationPort == self.DNS:
                    self.add(self.DNS)
                    self.processDns(arr[34:]) #pass the dns including UDP header
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
                             self.output = ("total number of DNS packets = {}\n".\
                                    format(self.counts[self.DNS]))+\
                                    ("total number of DNS transactions = {}\n\n".\
                                    format(self.DNSTran))+\
                                    self.output
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