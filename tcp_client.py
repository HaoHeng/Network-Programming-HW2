#!/usr/bin/env python
import socket
from time import ctime
import json
from io import StringIO
import pickle

HOST = '127.0.0.1'
PORT = 5566
ADDR = (HOST, PORT)

tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def display_bricks(scenario):
	dict_scenario=json.loads(scenario)
	if dict_scenario['status']==0 and dict_scenario['message']=='Game not change':
		print 'not change'
		return
	elif dict_scenario['status']==1 and dict_scenario['message']=='The game has closed':
		print 'The game has closed'
		return
	
	
	ary_scenario=dict_scenario['message'].split(',')
		
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

def display_help_message():
	print "'connect' - connect to game server"
	print "'disconnect' - disconnect from game server"
	print "'new' - new a game round"
	print "'end' - close the game"
	print "'w' - move bricks up"
	print "'s' - move bricks down"
	print "'a' - move bricks left"
	print "'d' - move bricks right"
	print "'u' - undo the last move"
	return

def fsm_state_local_transition_table(command):
	if command=='connect':
		tcpCliSock.connect(ADDR)
		print 'connect to game server'
		return 'server has been connected'
	elif command=='help':
		display_help_message()
		return 'local'
	else:
		print "Please connect to server first."
		return 'local'

def fsm_state_server_has_been_connected_transition_table(command):
	if command=='connect':
		print "Have already connected to server"
		return 'server has been connected'
	elif command=='disconnect':
		print "disconnect from game server"
		global tcpCliSock
		tcpCliSock.close()
		tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		return 'local'
	elif command=='new':
		tcpCliSock.sendall("{'action':'New'}")
		game_scenario=tcpCliSock.recv(1024)
		display_bricks(game_scenario)
		
		return 'during a game'
	
	elif command=='help':
		display_help_message()
		return 'server has been connected'
		
	else:
		print "Please new a game round first"
		return 'server has been connected'

def fsm_state_during_a_game_transition_table(command):
	if command=='new':
		print "Have already in a game round"
		return 'during a game'
	
	elif command=='help':
		display_help_message()
		return 'during a game'
	
	elif command=='disconnect':
		print "disconnect from game server"
		global tcpCliSock
		tcpCliSock.close()
		tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		return 'local'
	
	elif command=='end':
		tcpCliSock.sendall('{"action":"End"}')
		game_scenario=tcpCliSock.recv(1024)
		display_bricks(game_scenario)
		return 'server has been connected'
		
	elif command=='whosyourdaddy':
		json_to_be_sent='{"action":"whosyourdaddy"}'
		
	elif command=='w':
		json_to_be_sent='{"action":"moveUp"}'
		
	elif command=='a':
		json_to_be_sent='{"action":"moveLeft"}'
		
	elif command=='s':
		json_to_be_sent='{"action":"moveDown"}'
		
	elif command=='d':
		json_to_be_sent='{"action":"moveRight"}'
		
	elif command=='u':
		json_to_be_sent='{"action":"unDo"}'
		
	else:
		print "wrong command!"
		return 'during a game'
	
	tcpCliSock.sendall(json_to_be_sent)
	game_scenario=tcpCliSock.recv(1024)
	display_bricks(game_scenario)
	
	
	dict_scenario=json.loads(game_scenario)
	ary_scenario=dict_scenario['message'].split(',')
	
	for i in ary_scenario:
		if i=='2048':
			print 'Congrats! You win the game!'
			tcpCliSock.sendall('{"action":"End"}')
			game_scenario=tcpCliSock.recv(1024)
			display_bricks(game_scenario)
			return 'server has been connected'
			
	return 'during a game'


	
fsm_state="local"


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
