# 青年大学习/团课自动打卡

![](https://github.com/838239178/tk-auto-study/workflows/auto-study/badge.svg) ![](https://img.shields.io/github/stars/838239178/tk-auto-study) ![](https://img.shields.io/github/forks/838239178/tk-auto-study) ![](https://img.shields.io/badge/Python-3.7+-green.svg)

[此处展示重要更新日志，完整日志搓这里](./doc/Log.md)

> **2021.09.28**：:warning: **[重要更新]** 修复登录异常问题 更换了 **密钥(pubKey)** 和加密方法 请务必fork此最新版本并更换配置文件的public或github_secret的pub_key！
> 
> 2021.10.02: 新增消息推送功能——微信Server酱
>
> 2021.12.07: 新增多人打卡功能

🤺妈妈再也不用担心我团课没看被团支书赶着催了

### 点个:star:再走吧,❤感谢大家的Star和Fork,有问题可以发issue

**仅供福建共青团团员学习交流使用** 

**浙江团员可以点击这里[青春浙江](https://gist.github.com/838239178/ddad90e8c5e52f5fa8f0febea6109f24)**

### 参与贡献！

:pen:如果你有新的或更好OCR识别方式 请参考 [OCR贡献文档](./doc/OCR_Module_Rule.md) 做出你的贡献！

:pen: 如果你有新的或更好消息推送方式 请参考 [消息推送贡献文档](./doc/send_module_rule.md) 做出你的贡献！

## 使用方法

#### 🍎pub_key:

```
A7E74D2B6282AEB1C5EA3C28D25660A7
```

#### 0. 申请Ocr识别接口的权限

[详细教程请点击这里](https://blog.pressed.top/2021/02/14/signUpBaiduOcr/)

*请选择使用一种可以识别文字的api，建议使用BaiduAI的Ocr接口，否则需要自行修改代码*

- 首先要有一个百度账号，进入[这个网址](https://ai.baidu.com/)，点击控制台并登录
- 完成个人实名认证，申请文字识别的使用权
- 点击管理应用，点击创建应用，按要求填一些信息，创建完成后记住**API KEY**和**SECRET KEY**

#### 1. 部署在平台上定时执行

可以是服务器，本地，和GitHubActions，这里只介绍如何在GitHubActions中运行，其他运行方式请参考main.py中的注释

- fork该项目到你的库中

- 添加五个secrets，分别为：username,  pwd,  pub_key,  ocr_api_key,  ocr_secret_key

- **将.github/workflows/run.yml中的注释部分(`#`号)取消**并cron为你想要触发的时间，默认是每周三14点运行一次，cron如何写请自行百度
- 进入Action中手动触发一次，测试是否成功

## 可选识别类型

GithubAction（可选）添加新的secrets OCR_TYPE 来指定识别类型

其他方式在config.json中修改指定配置项即可

- baidu_image [默认方法,需要到百度AI中申请](https://blog.pressed.top/2021/02/14/signUpBaiduOcr/)

## 可选消息推送

> 仅 `1.2.2` 版本及以上可用

使用消息推送 如微信推送、QQ推送

### 配置

GithubAction用户可通过添加secrets：send_type, send_key, send_mode 来使用消息推送

普通用户可查看最新的 `config.json.bak` 浏览新配置项

**配置项解读**

| 配置项    | 说明                                                         | 可选值                                        |
| --------- | ------------------------------------------------------------ | --------------------------------------------- |
| send_type | 消息推送类型 **不填写则不推送**                              | [server_chan](./doc/send_help/server_chan.md) |
| send_key  | 消息推送服务的密钥 在推送服务的官网注册获得                  |                                               |
| send_mode | 推送模式 打卡失败时推送(fail) 打卡成功时推送(success) 无论成功与否都推送(both) **默认失败时推送** | fail success both                             |

## 多人打卡

> 仅支持 `1.2.3` 以上版本

配置多个账号一起打卡 PS:目前在试验阶段 有问题请及时回馈

1. 在 `Github Action` 上配置

    添加新secrets `EXT_USERS`, 按以下格式填写账号：
    
    ```text
   手机号1 密码1
   手机号2 密码2
    ```
   
   原先配置的secrets不需要改动，建议自己保存好多人的账号密码，以便以后增加或删除账号

2. 在本地 `config.json` 上配置

   参考 [config.json.bak](./config.json.bak) 的内容添加新的配置，原配置不需要改动

~~请让你的小伙伴也来点个Star吧~~

## 赏我一杯Coffee

![qq_pic_merged_1633171137809](https://cdn.jsdelivr.net/gh/838239178/PicgoBed/img/68747470733a2f2f63646e2e6a7364656c6976722e6e65742f67682f3833383233393137382f506963676f4265642f696d672f313633333137313136342e6a7067.jpg)![qq_pic_merged_1633171137809](https://cdn.jsdelivr.net/gh/838239178/PicgoBed/img/qq_pic_merged_1633171137809.jpg)

