# 青年大学习/团课自动打卡 [新系统]

<!-- ![](https://github.com/838239178/tk-auto-study/workflows/auto-study/badge.svg) -->

![](https://img.shields.io/github/stars/838239178/tk-auto-study) ![](https://img.shields.io/github/forks/838239178/tk-auto-study) ![](https://img.shields.io/badge/Python-3.7-green.svg)

[此处展示最近更新日志，完整日志搓这里](./doc/Log.md)

> 2022.10.01: 2.0版本 应用于新系统

🤺妈妈再也不用担心我团课没看被团支书赶着催了，欢迎 **Star** :star2:

### 声明

**仅供福建共青团团员学习交流使用**，项目遵循GPL协议，请勿拿来盈利、诈骗和违法之事！

项目产生的所有结果皆由使用者负责，本项目仅提供Python学习参考价值，本人不进行任何运行和调试。

- [x] 运行和调试本项目则表示为默认同意以上声明

### 参与贡献！

🖊️ 如果你有新的或更好消息推送方式 请参考 [消息推送贡献文档](https://github.com/838239178/tk-auto-study/blob/1.2.5/doc/send_module_rule.md) 做出你的贡献！

## 运行和调试方法

### 抓取Token

1. 进入 '我的' > 微信登录
2. 如果已经登陆需要清除缓存 '我的' > 清除缓存

抓取请求 `/platform/checkuser`，记录以下信息到配置文件中

```json
{
    "refreshExpire": 0,
    "expire": 0,
    "refreshToken": "",
    "token": ""
}
```

> IOS 推荐使用APP **Stream**
>
> Android 推荐使用APP **Canary** 未ROOT用户需要使用虚拟机
>
> *需要信任APP的HTTPS证书*

### 如何在服务器上部署

> requirements.txt 包含默认情况下需要的依赖

#### crontab

克隆项目并更改配置文件名称

```shell
git clone https://github.com/838239178/tk-auto-study.git && \
cd tk-auto-study && \
mv config.json.bak config.json
```

按照要求填写配置文件

```shell
vi config.json
```

修改 crontab

```shell
crontab -e
# 将下面这行复制到里面，cd的路径按照需要更改
00 08 * * 3 cd /root/tk-auto-study && python3 main.py >> crontab.log 2>&1
# 或者
00 08 * * 3 python3 /root/tk-auto-study/main.py >> crontab.log 2>&1
```

使用 `crontab -l` 查看是否修改成功

## 可选消息推送

使用消息推送 如微信推送、QQ推送

### 配置

普通用户可查看最新的 `config.json.bak` 浏览新配置项 (sender)

**配置项解读**

| 配置项    | 说明                                                         | 可选值                                                       |
| --------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| send_type | 消息推送类型 **不填写则不推送**                              | [server_chan](./doc/send_help/server_chan.md) [bark(Beta)](./doc/send_help/bark.md) [push_plus](./doc/send_help/push_plus.md) |
| send_key  | 消息推送服务的密钥                                           | 在推送服务的官网注册获得                                     |
| send_mode | 推送模式 打卡失败时推送(fail) 打卡成功时推送(success) 无论成功与否都推送(both) **默认失败时推送** | fail success both                                            |

## Stargazers over time

[![Stargazers over time](https://starchart.cc/838239178/tk-auto-study.svg)](https://starchart.cc/838239178/tk-auto-study)

## 鸣谢

> [Pycharm](https://zh.wikipedia.org/wiki/PyCharm) 是一个在各个方面都最大程度地提高开发人员的生产力的 IDE，适用于 Python 语言。

特别感谢 [JetBrains](https://www.jetbrains.com/?from=mirai) 为开源项目提供免费的 [PyCharm](https://www.jetbrains.com/pycharm/?from=mirai) 等 IDE 的授权

[<img src="https://github.com/mamoe/mirai/raw/dev/.github/jetbrains-variant-3.png" width="200"/>](https://www.jetbrains.com/?from=mirai)


## 赏我一杯Coffee

![qq_pic_merged_1633171137809](https://cdn.jsdelivr.net/gh/838239178/PicgoBed/img/qq_pic_merged_1633171137809.jpg)

