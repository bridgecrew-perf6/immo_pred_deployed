import json
from datetime import datetime
import os
from flask import Flask, request, jsonify, abort
from predict.prediction import predict
from preprocessing.cleaning_data import preprocess

app = Flask(__name__)

@app.route('/', methods=["GET"])
def alive():
    return f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - This server is alive."

@app.route('/predict', methods=["GET", "POST"])
def predicted():
    error = None
    if request.method == 'POST':
        input_json = request.get_json(force=True)
        data_prep = preprocess(input_json["data"])
        if data_prep:
          predicted = int(predict(data_prep))
          if predicted > 10000:
            return {"prediction": predicted}
          else:
            return {"error": "unable to predict a price. Please check your parameters."}
        else:
            error = 'Invalid data, please refer to the documentation.'
            return error
    if request.method == 'GET':
        return doc
    else:
        error = 'This method is now allowed. Please choice between GET or POST.'
        return error


doc ="""
{
  "data": 
  {
    "area": int,
    "property-type": "APARTMENT" | "HOUSE" | "OTHERS",
    "rooms-number": int,
    "zip-code": int,
    "land-area": Optional[int],
    "garden": Optional[bool],
    "garden-area": Optional[int],
    "equipped-kitchen": Optional[bool],
    "full-address": Optional[str],
    "swimming-pool": Optional[bool],
    "furnished": Optional[bool],
    "open-fire": Optional[bool],
    "terrace": Optional[bool],
    "terrace-area": Optional[int],
    "facades-number": Optional[int],
    "building-state": Optional[
      "NEW" | "GOOD" | "TO RENOVATE" | "JUST RENOVATED" | "TO REBUILD"
    ]
  }
} """

if __name__ == '__main__':
  port = os.environ.get("PORT", 5000)
  app.run(host="0.0.0.0",port=port)