from flask import Flask, render_template, request
import json
from datetime import datetime


app = Flask(__name__, static_url_path='/static')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message/<username>', methods=['GET', 'POST'])
@app.route('/message/', methods=['GET', 'POST'])
def contact(username=None):
    if request.method == 'POST':
        data_dict = {}

        username = request.form['username']
        message = request.form['message']

        data_dict['username'] = username
        data_dict['message'] = message

        with open('storage/data.json', 'r') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = {}

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        existing_data[current_time] = {
            "username": username,
            "message": message
        }

        with open('storage/data.json', 'w') as f:
            json.dump(existing_data, f, indent=2)
    return render_template('message.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(debug=True)