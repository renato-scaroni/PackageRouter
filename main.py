#!/usr/bin/env python

import sys
import os
from classes import *

def CreateAgent(name, param):
	print "criando agente ", name

def CreateDevice(name, param):
	if "$simulator host" in param:
		return Host(name)
	elif "$simulator router" in param:
		numberOfInterfaces = int(param.split(" ")[3].split("]")[0])
		return Router(name, numberOfInterfaces)

def GetNumFromString(s):
	i = 0
	while not s[:-i].isdigit():
		i += 1
	return int(s[:-i])

def CreateLink(data, entities):
	origDevice = data[2][1:].split(".")[0]
	if len(data[2][1:].split(".")) >1:
		origPort = data[2][1:].split(".")[1]
	else:
		origPort = -1
	destDevice = data[3][1:].split(".")
	if len(data[3][1:].split(".")) >1:
		destPort = data[3][1:].split(".")[1]
	else:
		destPort = -1

	if type(entities[origDevice]) == type(Host("")):
		entities[origDevice].SetLink(GetNumFromString(data[4]), GetNumFromString(data[5]), destDevice[0], int(destPort))
	else:
		entities[origDevice].SetLink(GetNumFromString(data[4]), GetNumFromString(data[5]), destDevice[0], int(destPort), int(origPort))


	if type(entities[destDevice[0]]) == type(Host("")):
		entities[destDevice[0]].SetLink(GetNumFromString(data[4]), GetNumFromString(data[5]), (origDevice), int(origPort))
	else:
		entities[destDevice[0]].SetLink(GetNumFromString(data[4]), GetNumFromString(data[5]), (origDevice), int(origPort), int(destPort))

def readInput(inputFilename, outputFilename):
	entities = {}
	agents = {}
	f = open(inputFilename, "rb")
	for line in f:
		data = line.split(" ")
		if data[0] == "set":   #hora de criar um objeto
			name = data[1]
			param = ""
			for i in range(2, len(data)): param += " " + data[i]
			if "$simulator host" in param or "$simulator router" in param:
				entities[name] = CreateDevice(name, param)
			else:
				agents[name] = CreateAgent(name, param)
		if data[0] == "$simulator":
			if data[1] == "duplex-link":
				CreateLink(data, entities)

	f.close()
	simulator = EP3Simulator(entities)
	simulator.simulate(outputFilename)


def main():
	if len(sys.argv) < 3 or len(sys.argv) > 3:
		print "Uso: ./main.py <entrada> <saida>"
		return
	readInput(sys.argv[1], sys.argv[2])


if  __name__ =='__main__':
    main()