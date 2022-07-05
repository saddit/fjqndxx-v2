# 本地OCR识别功能

**不需要填写，填写了也没有影响** `config.json` 中的 ak,sk 或者 `github action` 中的 secrets:ocr_api_key, ocr_secret_key

将ocr type更改为”tesseract“即可调用，**仅支持Window和Linux系统**

## Linux 下配置环境

系统内需要安装以下依赖：
 
  - tesseract-ocr 
  - libtesseract-dev 
  - libleptonica-dev 
  - openssl
