#!/usr/bin/env python

#Creating Interface VLAN

info = {}

###Get details###
info["vlan"] = raw_input("Vlan nos: ")
info["ip_add"] = raw_input("Network Subnet: ")
info["account_no"] = raw_input("Account Number: ")
info["company_name"] = raw_input("Company Name: ")
info["company_name"] = info["company_name"].replace(" ", "_")
info["bandwidth"] = raw_input("Bandwidth in Mbps: ")

hsrp_priority = ("150", "120")

###Bandwidth 1.2###
bandwidth_qos = int(round(float(info["bandwidth"]) * 1.2, 0))
str(bandwidth_qos)

###Interface, Gateway, IP address Manipulation###
def ipadd_gateway(ipadd):
	ipadd_splitdot = ipadd.split(".") ###Split the Octets###
	ipadd_octet = ipadd_splitdot[3].split("/") ###Split the mask###
	ipadd_oks = ipadd_octet[0] ###Octet to be manipulated without the mask###
	gateway = int(ipadd_oks)
	gateway = gateway + 1
	gateway_usethis = str(gateway)
	gateway = ipadd_splitdot[0]+"."+ipadd_splitdot[1]+"."+ipadd_splitdot[2]+"."+gateway_usethis
	return gateway


def ipadd_pri_int(ipadd):
        ipadd_splitdot = ipadd.split(".")
        ipadd_octet = ipadd_splitdot[3].split("/")
        ipadd_oks = ipadd_octet[0]
        gateway = int(ipadd_oks)
        gateway = gateway + 2 
        gateway_usethis = str(gateway)
        gateway = ipadd_splitdot[0]+"."+ipadd_splitdot[1]+"."+ipadd_splitdot[2]+"."+gateway_usethis+"/"+ipadd_octet[1]
        return gateway

def ipadd_sec_int(ipadd):
        ipadd_splitdot = ipadd.split(".")
        ipadd_octet = ipadd_splitdot[3].split("/")
        ipadd_oks = ipadd_octet[0]
        gateway = int(ipadd_oks)
        gateway = gateway + 3
        gateway_usethis = str(gateway)
        gateway = ipadd_splitdot[0]+"."+ipadd_splitdot[1]+"."+ipadd_splitdot[2]+"."+gateway_usethis+"/"+ipadd_octet[1]
        return gateway


###Generating Configuration###
###MODIFY THE OSPF INSTANCE NUMBER AND AREA###
def alpha(vlan, ip_add, account_no, company_name, bandwidth, qospolice, alpha):

	gateway = ipadd_gateway(ip_add)

	if alpha == "1st":
		int_ip = ipadd_pri_int(ip_add)
		hsrp_pri_sec = 150
		print ""
		print "==========ROUTER 1=========="
	if alpha == "2nd":
		int_ip = ipadd_sec_int(ip_add)
		hsrp_pri_sec = 120
		print ""
		print "==========ROUTER 2=========="
	print "=========Copy paste Below============"
	print ""
	print "interface Vlan%s" % (vlan)
	print " description %s %s" % (account_no, company_name)
	print " ip address %s" % (int_ip)
	print " ip router ospf 100 area 0.0.0.1”
	print " hsrp version 2"
	print "  hsrp %s" % (vlan)
	print "  preempt"
	print "  priority %s" % (hsrp_pri_sec)
	print "  ip %s" % (gateway)

	print ""
	print "ip access-list ACL_%s#%s_%sM" % (company_name, account_no, bandwidth)
	print " 10 permit ip any %s" % (ip_add)
	print " 20 permit ip %s any" % (ip_add)

	print ""
	print "class-map type qos match-all %s#%s_%sM" % (company_name, account_no, bandwidth)
	print " match access-group name ACL_%s#%s_%sM" % (company_name, account_no, bandwidth)

	print ""
	print "policy-map type qos %s_%s_%sM" % (company_name, account_no, bandwidth)
	print " class %s#%s_%sM" % (company_name, account_no, bandwidth)
	print "  police cir %s mbps bc 200 ms conform transmit violate drop" % (qospolice)

	print ""
	print "vlan configuration %s" % (vlan)
	print " service-policy type qos output %s_%s_%sM" % (company_name, account_no, bandwidth)
	print " service-policy type qos input %s_%s_%sM" % (company_name, account_no, bandwidth)

	print ""
	print "spanning-tree vlan %s priority 4096" % (vlan)

	print ""
	print "============Until Here================"


alpha(info["vlan"], info["ip_add"], info["account_no"], info["company_name"], info["bandwidth"], bandwidth_qos, "1st")
alpha(info["vlan"], info["ip_add"], info["account_no"], info["company_name"], info["bandwidth"], bandwidth_qos, "2nd")
#https://github.com/ledzep84
