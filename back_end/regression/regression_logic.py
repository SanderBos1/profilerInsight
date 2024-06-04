from flask import Blueprint, request, session, jsonify
from jsonschema import validate, ValidationError
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from io import BytesIO
import base64
import numpy as np

regression_bp = Blueprint(
    "regression_bp",
    __name__,
)


regression_input_schema = {
    "type": "object",
    "properties": {
        "coeficient": {"type": "number"},
        "intercept": {"type": "number"},
        "metric": {"type": "string"},
        "data_points": {
            "type": "array",
            "items": {
                "type": "array",
                "items": {"type": "number"},
            }
        }
    },
    "required": ["coeficient", "intercept", "metric", "data_points"]
}

data_points_input_schema= {
    "type": "object",
    "properties": {
        "datapoint": {
            "type": "array",
            "items": {
               "type": "number"
            },
            "minItems": 2,
            "maxItems": 2
        }
    },
    "required": ["datapoint"]
}

@regression_bp.route('/regression', methods=['GET'])
def basic_regression():
   """
   input: regression_input_schema

   Makes a picture displaying the regression line and the points given by the user.
   The metric is calculated and displayed in the title of the picture.
   Returns:
      {
         "image": A picture with the regression line defined by the input and the points added by the user.
   """

   try:
      input = request.get_json()
      validate(instance=input, schema=regression_input_schema)
   except ValidationError as e:
      return jsonify({"error": e.message}), 400
   except Exception as e:
        return jsonify({"error": "Invalid input"}), 400

   x = np.linspace(-10, 10, 100)
   y = input["coeficient"] * x + input["intercept"]

   user_xvalues = [float(x[0]) for x in input["data_points"]]
   user_yvalues = [float(x[1]) for x in input["data_points"]]  

   predicted_Y = input["coeficient"] * np.array(user_xvalues) + input["intercept"]

   # Selects the correc metric.
   if input["metric"] == "mean squared error":
      mse = np.mean((user_yvalues - predicted_Y) ** 2)
   else:
      "Invalid metric"

   fig = Figure()
   ax = fig.subplots()
   ax.scatter(user_xvalues, user_yvalues)
   ax.plot(x, y)
   ax.grid()
   ax.spines['left'].set_position('zero')
   ax.spines['bottom'].set_position('zero')
   ax.set_title(f"regression_example MSE:{mse}")
   buf = BytesIO()
   fig.savefig(buf, format="jpg")
   imageData = base64.b64encode(buf.getbuffer()).decode("ascii")

   return {
      "image": imageData,
      "metric": input["metric"]
   }


@regression_bp.route('/regression/data_points', methods=['GET', 'DELETE', 'PUT'])
def data_points():
   """
   Input: 
      GET: No input
      DELETE: A data point pair of the form [1, 2]
      PUT: A data point pair of the form [1, 2]

      {
      
         "datapoint": [1, 2]
      }

   """

   if request.method == "GET":
      if 'data_points' not in session:
         answer = "No data_points"
      answer = session["data_points"]
      return {
         "data_points": answer
      }
   
   try:
      input = request.get_json()
      validate(instance=input, schema=data_points_input_schema)
   except ValidationError as e:
      return jsonify({"error": e.message}), 400
   except Exception as e:
        return jsonify({"error": "Invalid input"}), 400
   
   if request.method == "DELETE":
      if len(session["data_points"]) == 0 or 'data_points' not in session:
         answer = "No data_points"
      elif input['datapoint'] in session['data_points']:
        session['data_points'].remove(input['datapoint'])
        answer = "Data point removed"
      else:
         answer = "Data point not in data_points"
      return{
         "data_points": answer

      }
   
   if request.method == "PUT":
      if 'data_points' not in session:
         session['data_points'] = []
      session['data_points'].append(input['datapoint'])
      answer = "Data point added"
      return{
         "data_points": answer

      }