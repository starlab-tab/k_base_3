from app.api.m2.sec import api
from flask import jsonify, request
from app.utils import safe_image
from app.forms import UploadImageForm, AlsImageForm


@api.route('/image', methods=['POST'])
def upload_paper_image():
    UploadImageForm().validate_for_api(request.files)
    imgae_url = safe_image.for_upload(media_type='sec', raw_image=request.files)
    return jsonify(data=imgae_url), 200


@api.route('/image', methods=['PATCH'])
def als_paper_image():
    valid_form = AlsImageForm().validate_for_api()
    image_url, status = safe_image.for_url(media_type='sec', image_url=valid_form['url'])
    return jsonify(data=image_url), 200
