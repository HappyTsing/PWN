PWN 快速入门！

环境准备：

1. 安装 32 位库

```
sudo apt-get install lib32ncurses5
sudo apt-get install lib32z1
sudo apt-get install gcc-multilib
```

2. mac ida 7 崩溃解决

下载 [libqcocoa.dylib](https://github.com/fjh658/IDA7.0_SP)，然后替换掉
`/Applications/IDA Pro 7.0/ida.app/Contents/PlugIns/platforms/libqcocoa.dylib` 即可。