#!/usr/bin/env python
import socket
from time import ctime
import json
from io import StringIO
import pickle

HOST = '127.0.0.1'
PORT = 5566
ADDR = (HOST, PORT)

def display_bricks(scenario):
	dict_scenario=json.loads(scenario)
	print scenario
	print dict_scenario
	if dict_scenario['status']==0 and dict_scenario['message']=='Game not change':
		print 'not change'
		return
	
	
	ary_scenario=dict_scenario['message'].split(',')
	print ary_scenario[1]
		
	print '---------------------'
	print '|'+ str(repr(int(ary_scenario[0])).rjust(4))+'|'+ str(repr(int(ary_scenario[1])).rjust(4))+'|'+ str(repr(int(ary_scenario[2])).rjust(4))+'|'+ str(repr(int(ary_scenario[3])).rjust(4))+'|'
	print '---------------------'
	print '|'+ str(repr(int(ary_scenario[4])).rjust(4))+'|'+ str(repr(int(ary_scenario[5])).rjust(4))+'|'+ str(repr(int(ary_scenario[6])).rjust(4))+'|'+ str(repr(int(ary_scenario[7])).rjust(4))+'|'
	print '---------------------'
	print '|'+ str(repr(int(ary_scenario[8])).rjust(4))+'|'+ str(repr(int(ary_scenario[9])).rjust(4))+'|'+ str(repr(int(ary_scenario[10])).rjust(4))+'|'+ str(repr(int(ary_scenario[11])).rjust(4))+'|'
	print '---------------------'
	print '|'+ str(repr(int(ary_scenario[12])).rjust(4))+'|'+ str(repr(int(ary_scenario[13])).rjust(4))+'|'+ str(repr(int(ary_scenario[14])).rjust(4))+'|'+ str(repr(int(ary_scenario[15])).rjust(4))+'|'
	print '---------------------'
	return

def fsm_state_local_transition_table(command):
	if command=='connect':
		tcpCliSock.connect(ADDR)
		return 'server has been connected'
	else:
		print "Please connect to server first."
		return 'local'

def fsm_state_server_has_been_connected_transition_table(command):
	if command=='connect':
		print "Have already connected to server"
		return 'server has been connected'
	elif command=='disconnect':
		print "disconnect from game server"
		tcpCliSock.close()
		return 'local'
	elif command=='new':
		tcpCliSock.sendall("{'action':'New'}")
		game_scenario=tcpCliSock.recv(1024)
		display_bricks(game_scenario)
		
		return 'during a game'
		
	else:
		print "Please new a game round first"
		return 'server has been connected'

def fsm_state_during_a_game_transition_table(command):
	if command=='new':
		print "Have already in a game round"
		return 'during a game'
	elif command=='end':
		tcpCliSock.sendall('{"action":"End"}')
		print "The game has closed"
		return 'server has been connected'
	elif command=='w':
		tcpCliSock.sendall('{"action":"moveUp"}')
		game_scenario=tcpCliSock.recv(1024)
		display_bricks(game_scenario)
		return 'during a game'
	elif command=='a':
		tcpCliSock.sendall('{"action":"moveLeft"}')
		game_scenario=tcpCliSock.recv(1024)
		display_bricks(game_scenario)
		return 'during a game'
	elif command=='s':
		tcpCliSock.sendall('{"action":"moveDown"}')
		game_scenario=tcpCliSock.recv(1024)
		display_bricks(game_scenario)
		return 'during a game'
	
	elif command=='d':
		tcpCliSock.sendall('{"action":"moveRight"}')
		game_scenario=tcpCliSock.recv(1024)
		display_bricks(game_scenario)
		return 'during a game'
	
	elif command=='u':
		tcpCliSock.sendall('{"action":"unDo"}')
		game_scenario=tcpCliSock.recv(1024)
		display_bricks(game_scenario)
		return 'during a game'
	else:
		print "wrong command!"
		return 'during a game'
	
		
		

	
fsm_state="local"

tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print "Welcome to Game 2048!"
print "enter 'help' to get more information."

while True:
	if fsm_state=='local':
		user_command = raw_input(">")
		fsm_state=fsm_state_local_transition_table(user_command)
		
	elif fsm_state=='server has been connected':
		user_command = raw_input(">")
		fsm_state=fsm_state_server_has_been_connected_transition_table(user_command)
		
	elif fsm_state=='during a game':
		user_command = raw_input("move>")
		fsm_state=fsm_state_during_a_game_transition_table(user_command)
		
	else:
		error()
