# 题目分析

1. 需要构造 shellcode
2. 关闭 ASLR/PIE、Canary、NX

# 编译

```shell
gcc -m32 -no-pie -fno-stack-protector -z execstack  -o no_protection no_protection.c
```

# shellcode

当我们在获得程序的漏洞后，就可以在程序的漏洞处执行特定的代码，而这些代码也就是俗称的shellcode。

通常，我们的 shellcode 是获取终端，也就是执行 `/bin/sh`。

获取 shellcode 的方法：

- pwntools

```python
from pwn import *
context(log_level='debug',arch='i386',os='linux')
shellcode = asm(shellcraft.sh())
```

- 利用别人写好的: exploit-db 搜

- 自己写，参考：[长亭pwn公开课-栈溢出 28分](https://www.bilibili.com/video/BV1FW421P7Ng/)


# shellcode 的位置

可以把 shellcode 放在缓冲区的开头，然后通过覆盖返回地址跳转至 shellcode；也可以把 shellcode 凡在返回地址之后，然后同样过覆盖返回地址跳转至 shellcode。
> 参考：[长亭pwn公开课-栈溢出 10分](https://www.bilibili.com/video/BV1FW421P7Ng/)

# 解题

检查保护措施

```
checksec no_protection
```

寻找填充长度：pwntools-cyclic