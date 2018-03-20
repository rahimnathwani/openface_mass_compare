import numpy as np
import cv2
import os
import json

from util import (
    getRep,
    getPeople
)

from bottle import (
    get,
    post,
    request,
    response,
    default_app,
    BaseRequest
    )

BaseRequest.MEMFILE_MAX = 1e8

@get('/')
def default_get():
    return static_file("index.html", ".")

@get('/<uid>')
def get_face(uid):
    f = glob.glob("/root/data/images/{}/*".format(uid))
    return static_file(f[0], '/')

@post('/')
def compare_image():
    if request.files.get('pic'):
        binary_data = request.files.get('pic').file.read()
    else:
        binary_data = request.body.read()

    img_array = np.asarray(bytearray(binary_data), dtype=np.uint8)
    image_data = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    response.content_type = 'application/json'
    if image_data is None:
        response.status = 200
        return {'error': 'Unable to decode posted image!'}
    try:
        people = getPeople(image_data)
        person = sorted(people, key=lambda p: p['face_size'])[-1]
        if person['confidence'] > 0.9:
            return json.dumps({
                'name': person['uid'],
                'message': 'welcome ' + person['uid']
                }, indent=4)
        else:
            return json.dumps({
                'name': person['uid'],
                'message': 'welcome ' + person['uid']
                }, indent=4)

    except Exception as e:
        response.status = 200
        return {'error': str(e)}

port = int(os.environ.get('PORT', 8080))

if __name__ == "__main__":
    run(host='0.0.0.0', port=port, debug=True, server='gunicorn', workers=4)

app = default_app()
