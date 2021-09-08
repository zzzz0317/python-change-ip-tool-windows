# IP切换器

**仅Windows平台可用**

**需要过UAC，建议使用 [pyinstaller](https://www.pyinstaller.org/) 打包为exe运行**

适用于 需要经常切换网络 且要切换的目标网络有一个或多个未启用 DHCP 的情况


## 配置说明
程序配置文件为同目录的 `config.json` ，第一次使用请参照下面的配置样例创建配置文件。

| 配置项                   | 说明                         | 类型                     | 默认值         | 上级配置项 |
| ------------------------ | ---------------------------- | ------------------------ | -------------- | ---------- |
| iface                    | 网卡名称                     | 字符串                   | 必填项无默认值 | 根         |
| iplist                   | IP配置列表                   | 含有IP配置对象的数组     | 必填项无默认值 | 根         |
| *IP配置对象*             | IP配置对象                   | 对象                     | -              | iplist     |
| name                     | 配置对象名称                 | 字符串                   | 必填项无默认值 | IP配置对象 |
| address                  | IP地址                       | 字符串                   | 必填项无默认值 | IP配置对象 |
| netmask                  | 子网掩码                     | 字符串                   | 必填项无默认值 | IP配置对象 |
| gateway                  | 网关IP地址                   | 字符串                   | 空             | IP配置对象 |
| dns                      | DNS                        | 字符串或含有字符串的数组 | 空             | IP配置对象 |
| subprocess_encode        | 执行命令时打印回显使用的编码 | 字符串                   | 必填项无默认值 | 根         |
| exit_when_finish         | 配置完成后是否自动退出       | 布尔值                   | true           | 根         |
| debug_subprocess_disable | 调试模式，跳过执行命令       | 布尔值                   | false          | 根         |
| debug_std_output         | 调试模式，打印更多调试信息   | 布尔值                   | false          | 根         |

* 在 `address` 中填入网络地址可在启用配置时手动输入剩余的主机地址部分。
* 在 `dns` 中填入数组时，数量超过两个的部分将被忽略。
* 不配置 `dns` 将会清除对应适配器的DNS配置。

## 配置样例

```json
{
  "subprocess_encode": "gbk",
  "exit_when_finish": true,
  "iface": "以太网",
  "iplist": [
    {
      "name": "test1",
      "address": "192.168.1.2",
      "netmask": "255.255.255.0",
      "gateway": "192.168.1.1",
      "dns": [
        "1.1.1.1",
        "192.168.1.1"
      ]
    },
    {
      "name": "test2",
      "address": "192.168.0.0",
      "netmask": "255.255.128.0",
      "gateway": "192.168.0.1"
    },
    {
      "name": "test3",
      "address": "1.1.1.2",
      "netmask": "255.255.255.0"
    }
  ],
  "debug_subprocess_disable": false,
  "debug_std_output": false
}
```

## 说明

* 本项目不提供开源软件的付费版本，也不提供与开源项目相关的任何商业服务（例如付费支持、咨询等）。
