# 题目分析

1. 只需要覆盖返回地址，无需自己构造 shellcode
2. 关闭 ASLR/PIE、Canary
3. 此题与 NX 无关，因为 success 函数是题目提供的！

# 编译

```
gcc -m32 -no-pie -fno-stack-protector -o stack_example stack_example.c
```

gcc 编译指令中：

- -m32 指的是生成 32 位程序
- -fno-stack-protector 指的是不开启堆栈溢出保护，即不生成 canary
- -no-pie 为了避免加载基址被打乱，关闭 pie
- -z execstack 关闭 NX

> 不同 gcc 版本对于 PIE 的默认配置不同，我们可以使用命令gcc -v查看 gcc 默认的开关情况。如果含有--enable-default-pie参数则代表 PIE 默认已开启，需要在编译指令中添加参数。

系统配置中，通过修改 `/proc/sys/kernel/randomize_va_space` 来控制 ASLR 启动与否

- 0，关闭 ASLR，没有随机化。栈、堆、.so 的基地址每次都相同。
- 1，普通的 ASLR。栈基地址、mmap 基地址、.so 加载基地址都将被随机化，但是堆基地址没有随机化。
- 2，增强的 ASLR，在 1 的基础上，增加了堆基地址随机化。

关闭 ASLR：

```
echo 0 > /proc/sys/kernel/randomize_va_space
```

# checksec 查看文件保护格式

```
checksec stack_example
```

结果如下：

```
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
```

此外，可以通过 `file` 指令也可以获取一些信息。

# 破解思路

首先需要知道当执行 vulnerable 时的栈帧结构：

```
                    +-----------------+
                    |     retaddr     |
                    +-----------------+
                    |     saved ebp   |
            ebp--->+-----------------+
                    |                 |
                    |                 |
                    |                 |
                    |                 |
                    |                 |
                    |                 |
        s,ebp-0x14-->+-----------------+
```

当 main 函数调用 vulnerable 函数时，其最终会压入 retaddr，该地址为 vulnerable 函数返回后，该回到 main 函数的位置。

当进入 vulnerable 的栈帧后，首先会压入需要保存的寄存器信息，接着压入临时变量，此处就是 `char s`。

因此我们需要做的就是让 `char s` 溢出，覆盖 `retaddr` 的值，将他的值修改为 success 函数的起始地址。

寄存器 ebp 记录了栈帧的起始地址，然后只需要知道 `char s` 在栈中距离 ebp 的地址有多少，再加上 4 个字节（ebp那个地址指向的数据），最后将 success 函数的起始地址写入即可。

通过 ida 获取 success 的起始地址为：0x08048456

由于在计算机内存中，每个值都是按照字节存储的。一般情况下都是采用小端存储，可以通过 pwntools 提供的 p32 方法自动完成转换

因此最终构造的 payload 为：

```python
payload = b'a' * 0x14 + b'bbbb' + p32(success_addr) # p32 将数字转换为字符串（自动变为小端序）此处为：'\x56\x84\x04\x08'
```

```
                +-----------------+
                |    0x08048456   |
                +-----------------+
                |       bbbb      |
        ebp--->+-----------------+
                |                 |
                |                 |
                |     a*0x14      |
                |                 |
                |                 |
                |                 |
    s,ebp-0x14-->+-----------------+
```