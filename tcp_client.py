#!/usr/bin/env python
from socket import *
from time import ctime


HOST = '127.0.0.1'
PORT = 5566
ADDR = (HOST, PORT)


def fsm_state_local_transition_table(command):
	if command=='connect':
		tcpCliSock.connect(ADDR)
		return 'server has been connected'
	else:
		print("Please connect to server first.")
		return 'local'

def fsm_state_server_has_been_connected_transition_table(command):
	return

def fsm_state_during_a_game_transition_table(command):
	return

	
fsm_state="local"

tcpCliSock = socket(AF_INET, SOCK_STREAM)

print("Welcome to Game 2048!")
print("enter 'help' to get more information.")

while True:
	if fsm_state=='local':
		user_command = input(">")
		fsm_state_local_transition_table(user_command)
		
	elif fsm_state=='server has been connected':
		user_command = input(">")
		fsm_state_server_has_been_connected_transition_table(user_command)
		
	elif fsm_state=='during a game':
		user_command = input("move>")
		fsm_state_during_a_game_transition_table(user_command)
		
	else:
		error()



