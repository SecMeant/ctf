#!/usr/bin/python2

import socket
import string

challange_ip = 'xo.fword.wtf'
challange_port = 5554

# All chars for bruteforcing
chars = string.ascii_letters + string.digits + '_()[]<>?/\\-=!@#$%^&*'

# Whatever character that is not a valid flag char
flag_char_ok = '\x01'

flag_max_len = 64

flag = ''
input = []

current_len = 1

xo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
xo.connect((challange_ip, challange_port))

xo_read = xo.makefile()

while 1:

    input += ' '
    for c in chars:
        input[-1] = c

        xo_read.readline() # discard "input: "
        xo.sendall(''.join(input) + '\n')
        guessed_length = int(xo_read.readline())

        print('Char: {}, Input: {}'.format(c, ''.join(input)))
        print(guessed_length)

        if guessed_length == len(flag):
            flag += c
            input[-1] = flag_char_ok
            break

    print("Flag: {}".format(flag))
