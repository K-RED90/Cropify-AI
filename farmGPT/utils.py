import json
from PIL import Image
import io
import base64


def encode_image(image_path):
    """Getting the base64 string"""
    # Open the image file
    with Image.open(image_path) as img:
        with io.BytesIO() as output_bytes:
            img.save(output_bytes, format="JPEG")
            jpeg_data = output_bytes.getvalue()
        return base64.b64encode(jpeg_data).decode("utf-8")


def json_to_markdown(json_data):
    markdown_string = ""
    for key, value in json_data.items():
        formatted_key = " ".join(word.capitalize() for word in key.split("_"))
        if formatted_key in ["Pest", "Disease"]:
            markdown_string += f"### {formatted_key}: {value}\n\n"
        elif isinstance(value, str):
            markdown_string += f"**`{formatted_key}`**: {value}\n\n"
        else:
            markdown_string += f"**`{formatted_key}`**:\n\n{value}\n\n"

    return markdown_string.strip()
