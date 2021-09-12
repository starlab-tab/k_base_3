# -*- coding: utf-8 -*-
import base64
from io import BytesIO
import random
import pathlib
import re
from flask import current_app

import requests
from PIL import Image
from PIL import ImageFile
import time

from app.exceptions import Code404, Code400

ImageFile.LOAD_TRUNCATED_IMAGES = True


def get_effective_proxy():
    proxies = {
        'http': 'socks5://127.0.0.1:1080',
        'https': 'socks5://127.0.0.1:1080'
    }
    return proxies


def get_dest_path(suffix, media_type='other'):
    from app.config.config import config_ini
    time_stamp = time.time()
    time_stamp_str = str(time_stamp).replace('.', '')
    ts = int(time_stamp)
    date = time.strftime("%Y%m%d", time.localtime(time_stamp))

    upload_path = config_ini['uploads'][f'{media_type}_image_folder']
    upload_path = f'{upload_path}/{date}'
    pathlib.Path(upload_path).mkdir(parents=True, exist_ok=True)

    image_access = config_ini['media'][f'{media_type}_image_access_url']
    image_name = f'{hex(ts)[2:]}{time_stamp_str}{random.randint(200, 65535)}.{suffix}'
    image_path = f'{upload_path}/{image_name}'
    image_url = f'{image_access}/{date}/{image_name}'
    return image_path, image_url


def for_url(media_type, image_url):
    # res = requests.get(img_url, stream=True, proxies=get_effective_proxy())
    status = False
    try:
        res = requests.get(image_url, stream=True)
        count = 1
        while res.status_code != 200 and count <= 5:
            res = requests.get(image_url, stream=True)
            count += 1
        if res.status_code == 200:
            image = Image.open(BytesIO(res.content))
            suffix = image.format.lower()
            image_path, image_url = get_dest_path(suffix=suffix, media_type=media_type)
            image.save(image_path)
            status = True
    except Exception as e:
        current_app.logger.exception(f'fail to save image_url: {image_url}')
    # image_url = f'http://127.0.0.1:5000{image_url}'
    image_url = image_url
    return image_url, status


def for_upload(media_type, raw_image):
    try:
        image = Image.open(BytesIO(raw_image['image'].read()))
        suffix = image.format.lower()
        image_path, image_url = get_dest_path(suffix=suffix, media_type=media_type)
        image.save(image_path)
        return image_url
    except Exception as e:
        raise Code404("upload fail")


def for_base64(media_type, base64_str):
    status = False
    image_url = "http://127.0.0.1"
    try:
        base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
        byte_data = base64.b64decode(base64_data)
        image = Image.open(BytesIO(byte_data))
        suffix = image.format.lower()
        image_path, image_url = get_dest_path(suffix, media_type)
        image.save(image_path)
        # image_url = f'http://127.0.0.1:5000{image_url}'
        image_url = image_url
        status = True
    except Exception as e:
        current_app.logger.exception(f'fail to save image_base64 \n{e}')
    return image_url, status
