name: "报告Bug"
description: 如果想报告运行出错请用此模板
body:
  - type: input
    attributes:
      label: 使用的Python版本
      placeholder: 3.7
    validations:
      required: true
  - type: input
    attributes:
      label: 使用的发行版本
      placeholder: 1.3.0
    validations:
      required: true
  - type: textarea
    attributes:
      label: 问题描述
    validations:
      required: true
  - type: textarea
    attributes:
      label: 运行日志
      description: 请复制或截图完整的错误日志
    validations:
      required: true
  - type: textarea
    attributes:
      label: 其他补充
