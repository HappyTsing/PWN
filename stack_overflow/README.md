# 栈溢出

# 保护措施
①ASLR
通常ASLR有0/1/2三种级别，其中0表示ASLR未开启，1表示随机化stack、libraries，2还会随机化heap。

配置 ASLR 级别：

```
/proc/sys/kernel/randomize_va_space
```

修改该文件的值（0/1/2）即可对 ASLR 级别进行配置，默认为 2.

②PIE
使用命令gcc -v查看 gcc 默认的开关情况。如果含有    `--enable-default-pie` 参数则代表 PIE 默认已开启，此时编译出来的 ELF 用 `file` 命令查看会显示其为 so，其随机化了ELF装载内存的基址（代码段、plt、got、data等共同的基址）。

若想关闭 PIE 则需要在编译指令中添加参数 `-no-pie`。

③Canary

通过命令行选项 `-fno-stack-protector` 可以阻止 GCC 产生 cannary 保护代码，否则将默认生成

④NX

GCC 默认启用 NX 选项，通过添加 `-z execstack` 关闭 NX。

# 核心原理

栈是从高地址向低地址增长的，但是，当编译器为一个变量在栈中分配好空间后，该变量却是从低地址向高地址增长。

<img src="https://happytsing-figure-bed.oss-cn-hangzhou.aliyuncs.com/pwn/common-stack-frame.png" alt="common-stack-frame" style="zoom:33%;" />
