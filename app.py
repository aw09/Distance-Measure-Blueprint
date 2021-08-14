from flask import Flask
from distance_measure.geopy import geopy_lib
from distance_measure.yandex import yandex_lib
import logging

app = Flask(__name__)

app.register_blueprint(geopy_lib)
app.register_blueprint(yandex_lib)

@app.route("/")
def welcome():
    return '''
    <h4>Welcome to Distance Measure blueprint<h4>
    <table>
    <tr>
        <td>/geopy</td>
        <td>for using geopy library</td>
    </tr>
    <tr>
        <td>/yandex</td>
        <td>for using Yandex API</td>
    </tr>
    </table>
    '''

logging.basicConfig(filename='record.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)