from flask import Flask
from flask import request #<-- import 'request'
from flask_cors import CORS, cross_origin


app = Flask(__name__)

@app.route('/', methods = ['POST'])
def index(name='Treehouse'):  #<-- provide default value for 'name'
    name = request.args.get('name', name) #<-- get argument 'name' or use default name set above
    return 'Hello {name}'.format(name=name) #<-- update return string to accept variable 'name'

if __name__ == "__main__":
    app.run(debug=True)



