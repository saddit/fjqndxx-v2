# Send模块通用实现规范

如果想提供新的、更好的消息方式，请按照以下步骤进行开发

## 创建脚本文件

fork本项目develop分支并克隆到本地, 在*send_module*文件夹中新建目录 `{名称}/sender.py` , 如 `server_chan/sender.py`

## 编写脚本文件

`sender.py` 必须实现以下接口

```python
# [必须选]设置密钥
def set_keys(key: str)

# [必须]发送消息
# 需返回对应格式的dict
def send(title: str, content: str) -> dict
```

`def send` 返回值必须按照以下格式

```python
{
    'success': True,	#True or False
    'message': "something"	#error mesage
}
```

## 编写说明文档

在 `README.md` 中的 `可选消息推送`  下的配置项表格第一行 send_type 的可选值处，按照以下格式填入：*（可选值之间用一个空格分隔）*

```markdown
[{名称}]({教程或官网跳转地址,可以是自定义网址})
```

如：

```markdown
[server_chan](./doc/send_help/server_chan.md)
```

教程除了第三方的网站外，也可自行编写`{名称}.md`文件到 `doc/send_help` 下，并按照相对地址填入，如 `./doc/send_help/server_chan.md`

### 最后——申请 Pull Request

需要附上执行成功截图

