import pickle
from flask import Flask,request,jsonify, render_template,make_response
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#useful variables
global iris_loaded_model # declare a global variable to avoid unnecessary reloads
iris_prediction_mapper={0:'Iris-Setosa',1:'Iris-Versicolour',2:'Iris-Virginica'}


def model_load():
    #load the classifier model 
    try:
        iris_loaded_model = pickle.load(open('./iris_model.sav', 'rb'))
        return iris_loaded_model
    except Exception as e:
        print ( f"Model Load Error {str(e)}" )

def prediction(loaded_model,array_of_features):    
    if loaded_model:# only if the model is there
        prediction_result=loaded_model.predict(array_of_features)
        try:
            species_type=iris_prediction_mapper.get(prediction_result[0])
            return species_type
        except KeyError:
            species_type="Could Not Be Determined"
            return species_type


@app.route('/predictiris', methods=['GET','POST'])
def predictiris():
    prediction_input=request.form.to_dict()
    #attempt model load
    loaded_model=model_load()
    print(prediction_input)
    output=prediction(loaded_model,[[float(item) for item in list(prediction_input.values())]]) # as the form data conatins the values in string 
    return jsonify(f"Species is {output}")

@app.route('/predictirispartial', methods=['GET','POST'])
def predictirispartial():
    prediction_input=request.form.to_dict() # for demo reasons we will only pass 2 parameters here and add two parameters hardcoded
    print(prediction_input)
    #add two values 
    prediction_input['value3']='5.4'
    prediction_input['value4']='0.9'
    #attempt model load
    loaded_model=model_load()
    print(prediction_input)
    output=prediction(loaded_model,[[float(item) for item in list(prediction_input.values())]]) # as the form data conatins the values in string 
    return jsonify(f"Species on Partial is {output}")


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify("Performed HealthCheck.Container is loading fine ")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000, debug=True)
