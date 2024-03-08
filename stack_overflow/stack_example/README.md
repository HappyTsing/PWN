# 编译

```
gcc -m32 -no-pie -fno-stack-protector stack_example.c -o stack_example
```

gcc 编译指令中：

- -m32 指的是生成 32 位程序； 
- -fno-stack-protector 指的是不开启堆栈溢出保护，即不生成 canary。 
- -no-pie 为了避免加载基址被打乱，关闭 pie

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
