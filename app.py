from flask import Flask, send_file, send_from_directory, request, jsonify, abort
from PIL import Image, ImageSequence
from utilities import transform_image
import requests

app = Flask(__name__)


@app.route('/')
def gifResize():
    ''' This Endpoint accepts path or url, width and height as parameters'''
    path = request.args.get('path')
    url = request.args.get('url')
    img = None
    if path:
        try:
            img = Image.open(path)
        except FileNotFoundError:
            abort(404)
    elif url:
        # Check if the provided response for the provided url return gif content type.
        my_file = requests.get(url)
        print("got response: ", my_file.headers)
        if my_file.headers['Content-Type'] == 'image/gif':
            try:
                open('gifFile.gif', 'wb').write(my_file.content)
                img = Image.open('gifFile.gif')
            except:
                abort(404)
    if img:
        width = request.args.get('width')
        height = request.args.get('height')
        if height and width:
            height = int(height)
            width = int(width)
            out_img = transform_image(img, width, height)
            out_img[0].save('resized.gif', save_all=True,
                            append_images=out_img[1:], loop=0)
            return send_from_directory("/home/raktim/Downloads/pyproject/GIFresize", path="resized.gif", as_attachment=True)
        else:
            return jsonify({'Error': 'No dimensions received'})
    else:
        return jsonify({"Error": "No valid url given. Must be a url of a gif file."})


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
