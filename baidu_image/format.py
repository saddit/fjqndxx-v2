from PIL import Image
import io


def img_format(img: bytes, format_str: str) -> bytes:
    """
    图片格式转化
    img: 图片二进制数据，非base64格式
    format：如'PNG'、'JPG'等
    """
    pimg = Image.open(io.BytesIO(img))
    stream = io.BytesIO()
    pimg.save(stream, format=format_str)
    return stream.getvalue()


def Image_format(img: Image, format_str: str) -> bytes:
    stream = io.BytesIO()
    img.save(stream, format=format_str)
    return stream.getvalue()


def img_PIL(img: bytes) -> Image:
    return Image.open(io.BytesIO(img))
