# PWN 快速入门！

# 环境准备

- 系统选择: ubuntu 18.04

- 编译器版本: gcc 7.5.0

注: ubuntu 20.04 + gcc 9.0 编译出的二进制文件，在 mac 的 ida7.0 上会报错 `could not patch the PLT stub; unexpected PLT format or the file has been modified after linking!`

- 安装 32 位库

```
sudo apt-get install lib32ncurses5
sudo apt-get install lib32z1
sudo apt-get install gcc-multilib
```

- mac ida 7 崩溃解决

下载 [libqcocoa.dylib](https://github.com/fjh658/IDA7.0_SP)，然后替换掉
`/Applications/IDA Pro 7.0/ida.app/Contents/PlugIns/platforms/libqcocoa.dylib` 即可。

# ida 使用

反编译: F5
切换指令与汇编视图: 空格键

# 参考

https://www.yuque.com/hxfqg9/bin/ug9gx5