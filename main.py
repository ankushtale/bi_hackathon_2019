import args
import julie

from flask import Flask

app = Flask(__name__, static_url_path='/static', static_folder='./static')


@app.route("/")
def root():
    return app.send_static_file('index.html')


if __name__ == '__main__':

    parsed_arg_dict = args.parse_args()
    source_directory = parsed_arg_dict['source_dir']

    julie.do_the_thing(source_directory)

    app.run()




