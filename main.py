import args
import julie
import os
import json
from flask import Flask, request

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = ('pdf')

app = Flask(__name__, static_url_path='/static', static_folder='./static')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def root():
    return app.send_static_file('index.html')


@app.route("/upload", methods=['POST'])
def save_file():
    file = request.files['file']
    if file.filename == '':
        #TODO: add logger
        return "no file selected"
    if file and allowed_file(file.filename):
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return pdf_summary()


@app.route("/pdf", methods=['GET'])
def pdf_summary():
    parsed_arg_dict = args.parse_args()
    source_directory = parsed_arg_dict['source_dir']
    response = julie.do_the_thing(source_directory)
    return json.dumps(response)


if __name__ == '__main__':
    app.run()



