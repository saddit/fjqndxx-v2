# 微软Azure计算机视觉OCR

## 前提

你需要有一个教育邮箱，申请Azure学生账户，期间需要验证教育邮箱。有了Azure学生账号还能免费使用其他服务，比如服务器。

## 依赖需求

由于Azure支持的图片大小不在范围内，因此需要Pillow缩放图片大小，需要在你的`requirements.txt`中加入`Pillow` 

## 步骤

 1. 需要注册微软账号
 2. 登陆 https://azure.microsoft.com/free/student
 3. 在免费服务中开通**计算机视觉**服务
 4. 填写表单，注意选择的区域，建议选择EastAsia
 5. 创建完成后进入该服务>资源管理>密钥和终结点，复制其中一个密钥和终结点，终结点去掉`https://`前缀
 6. 填写config.json, ocr.ak 为终结点, ocr.sk 为其中一个密钥, 例:
    ```json
    "ocr": {
        "ak": "hksight.cognitiveservices.azure.com",
        "sk": "182391820319283019",
        "type": "azure"
    },
    ```
