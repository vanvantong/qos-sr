
import random
import gym
import numpy as np
import time
import datetime
import math

def maxFunc(a,b):
	if a <= b:
		return b
	else:
		return a


def minFunc(a,b):
	if a <= b:
		return a
	else:
		return b

def vs_qoe_model(delay, loss):

	qoe_vs = math.exp(1.038 - (1.081/10000 * delay) - (4.937/1000 * loss))
	return qoe_vs

def ft_qoe_model(bw):

	qoe_ft = 0.059 * math.exp(-0.048) * bw + 0.054
	return qoe_ft

def voip_qoe_model(loss):

	qoe_voip = 3.01 * math.exp(-4.473) * loss + 1.065
	return qoe_voip

def writeFile(s):
	f = open("/home/vantong/onos/apps/segmentrouting/app/src/main/java/org/onosproject/segmentrouting/reRouting.csv", "w")
	f.write(str(s))
	f.close()


while(True):
	nFile = '/home/vantong/onos/providers/lldpcommon/src/main/java/org/onosproject/provider/lldpcommon/link_para.csv'
	f = open('/home/vantong/onos/apps/segmentrouting/app/src/main/java/org/onosproject/segmentrouting/SRPaths.csv','r')
	latency = 0
	loss = -10
	linkUtilization = 10
	for line in f:
		tmp = line.split(';')
		if len(tmp) == 3:
			link = tmp[1].split(',')
			for k in range(len(link)):
				f_para = open(nFile,'r')
				for line_para in f_para:
					tmp_para = line_para.split(';')
					for j in range(len(tmp_para)):
						if tmp_para[j].find(link[k]) != -1:
							para = tmp_para[j].split('*')						
							if(len(para) == 4):
								s = para[1].split(',')
								if(len(s) == 10):
									if s[9].count(".") == 1:
										latency = latency + float(s[9])
								s = para[2].split(',')
								if(len(s) == 10):
									if s[9].count(".") == 1:
										loss = maxFunc(loss,  float(s[9]))
								s = para[3].split(',')
								if(len(s) == 10):
									if s[9].count(".") == 1:
										linkUtilization = minFunc(linkUtilization, float(s[9]))
	#ToS - video streaming: 1, file transfer: 2, voip: 3

	tos = 1
	reRouting = 0
	if(tos == 1):
		qoe = vs_qoe_model(latency, loss)
	elif (tos == 2):
		qoe = ft_qoe_model(linkUtilization)
	elif(tos == 3):
		voip_qoe_model(loss)


	epsilon1 = 0.9
	epsilon2 = 0.1
	if qoe < 3:
		print("QoE: {}").format(qoe)
		# There is the problem in the network
		if np.random.rand() <= epsilon1:
			reRouting = 1
			print("Rerouting: {}").format(reRouting)
			writeFile(reRouting)
		else:
			reRouting = 0
			print("Rerouting: {}").format(reRouting)
			writeFile(reRouting)
	else:
		# The network is normal
		if np.random.rand() >= epsilon2:
			reRouting = 0
			print("Rerouting: {}").format(reRouting)
			writeFile(reRouting)
		else: 
			reRouting = 1
			print("Rerouting: {}").format(reRouting)
			writeFile(reRouting)
	print("\n")
	time.sleep(10)