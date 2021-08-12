from flask import Flask
from distance_measure.geopy import geopy_lib
from distance_measure.yandex import yandex_lib

app = Flask(__name__)

app.register_blueprint(geopy_lib)
app.register_blueprint(yandex_lib)

if __name__ == "__main__":
    app.run()
