# OCR 模块通用实现规范

如果想提供新的、更好的文字识别方式，请按照以下步骤进行开发

## 创建脚本文件

fork本项目develop分支并克隆到本地, 在*ocr_module*文件夹中新建目录 `{名称}/{名称}_ocr.py` , 如 `baidu_image/baidu_image_ocr.py`

## 编写脚本文件

`{名称}_ocr.py` 必须实现以下接口

```python
# [必须]是否使用密钥
def is_need_keys() -> bool

# [可选]设置密钥，如果不需要可不编写
def set_keys(api_key: str, secret: str)

# [必须]获取识别结果
# 参数为图片的base64格式
# 识别失败需抛出异常 raise Exception("message")
def get_result(img: bytes) -> str
```

## 编写说明文档

再 `README.md` 中的 `可选识别类型`  下填入新的OCR识别模块的名称，按照以下格式：

```markdown
- {名称} [{简述使用条件}]({教程跳转地址,可以是自定义网址})
```

如：

```markdown
- baidu_image [需要到百度AI中申请](https://blog.pressed.top/2021/02/14/signUpBaiduOcr/)
<!-- or -->
- baidu_image [需要到百度AI中申请](./doc/ocr_help/baidu_image.md)
```

教程除了第三方的网站外，也可自行编写`{名称}.md`文件到 `doc/ocr_help` 下，并按照相对地址填入，如 `./doc/ocr_help/baidu_image.md`

### 最后——申请 Pull Request