# 青年大学习/团课自动打卡

🤺妈妈再也不用担心我团课没看被团支书赶着催了

 **仅供福建共青团团员学习交流使用** 

## 使用方法

#### 🍎pub_key:

```
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKf9iZkA5HEFw4zt7MRBkcmgUiz5+r5eqDOKbaurEbScmXd3ZZTtyzirqkYKRIH5mQ+8hq+Wd/pTZNXHS8L0+88CAwEAAQ==
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

- 修改.github/workflows/run.yml中的cron为你想要触发的时间，默认是每周三14点运行一次，cron如何写请自行百度
- 进入Action中手动触发一次，测试是否成功





