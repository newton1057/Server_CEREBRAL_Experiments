from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
import json
import pyautogui
import time
import random

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Functions general
def emailToUsername( email : str ):
    """
    Function to convert an email to a username.
    
    The username is the part of the email before the '@' symbol.
    
    Parameters:
    - email: Email address to convert to username
    
    Example:
    newton1057@gmail.com - newton1057

    Returns the username
    """
    return email.split('@')[0]

def pathUserName ( username : str):
    """
    Function to get the path of the user file.

    The path is the path of the user file in the database (JSON).

    Parameters:
    - username: Username of the user.

    Example:
    newton1057 - newton1057.json

    Returns the path of the user file.
    """

    file_path = os.path.join(os.path.dirname(__file__), 'db') # Define the path to the database folder
    user_file_path = os.path.join(file_path, f'{username}.json') # Define the path to the user file
    return user_file_path



@app.route('/API/Users', methods=['POST'])
def Create_User():
    """
    Endpoint to create a new user.
    
    The request should contain the following data:
    - profile: User profile data
    - level: User level data
    - permissions: User permissions data

    The user data should be saved in the database (Files JSON).

    Returns a JSON response with the new user data.
    """
    # Get the new user data from the request
    newUser = request.json

    # Define the username based on the user's email
    username = newUser['profile']['email'].split('@')[0]

    # Define the full path to the JSON file
    file_path = os.path.join(os.path.dirname(__file__), 'db')

    # Definir la ruta completa al archivo JSON usando el nombre de usuario
    user_file_path = os.path.join(file_path, f'{username}.json')

    # Escribir los datos del nuevo usuario en el archivo JSON correspondiente
    with open(user_file_path, 'w') as file:
        json.dump(newUser, file, indent=2)

    return jsonify(newUser), 200


@app.route('/API/Login', methods=['POST'])
def Login():
    """
    Endpoint to login a user.
    
    The request should contain the following data:
    - email: User email
    - password: User password
    
    The user data should be retrieved from the database (Files JSON).
    
    Returns a JSON response with the user data.
    """

    user = request.json
    username = user['email'].split('@')[0]

    file_path = os.path.join(os.path.dirname(__file__), 'db')
    user_file_path = os.path.join(file_path, f'{username}.json')

    if os.path.exists(user_file_path):
       with open(user_file_path, 'r') as file:
           data = json.load(file)
           if (data['profile']['email'] == user['email']) and (data['profile']['password'] == user['password']) :
                return jsonify(data), 200
           else:
                return jsonify({'error': 'Contraseña incorrecta'}), 400
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
@app.route('/API/Quiz_Experiment_Traditional', methods=['POST'])
def Save_Quiz_Experiment_Traditional():
    """
    Endpoint for saver questions of Quiz of Experiment Traitional.

    
    """
    data = request.json

    username = data['email'].split('@')[0]
    
    file_path = os.path.join(os.path.dirname(__file__), 'db')
    user_file_path = os.path.join(file_path, f'{username}.json')

    with open(user_file_path, 'r') as file:
        data_user = json.load(file)

    data_user['Quiz_Experiment_Traditional'] = data['data']

    with open(user_file_path, 'w') as file:
        json.dump(data_user, file, indent=2)
    
    return jsonify({'status': 'OK'}), 200
    
@app.route('/API/UpdatePhase', methods=['POST'])
def Update_Phase():
    data = request.json
    
    username = data['email'].split('@')[0]
    phase = data['phase']
    phases_completed = data['phase_completed']

    file_path = os.path.join(os.path.dirname(__file__), 'db')
    user_file_path = os.path.join(file_path, f'{username}.json')

    with open(user_file_path, 'r') as file:
        data_user = json.load(file)

    if 'Phases' in data_user:
        if phase not in data_user['Phases']:
            data_user['Phases'].append(phase)
    else:
        data_user['Phases'] = [phase]

    if 'Phases_completed' in data_user:
        if phases_completed not in data_user['Phases_completed']:
            data_user['Phases_completed'].append(phases_completed)
    else:
        data_user['Phases_completed'] = [phases_completed]

    with open(user_file_path, 'w') as file:
        json.dump(data_user, file, indent=2)

    return jsonify({'status': 'OK'}), 200

@app.route('/API/GetPhases', methods=['POST'])
def Get_Phases():
    """
    Endpoint to obtain the phases of the user.

    The request should contain the following data:
    - email: User email.
    
    Returns a JSON with the phases of the user.

    Example response:
    {
    "Phases": [
        "",
        "Introduction",
        "Traditional_Experiment_Training",
        "Traditional_Experiment_Assessment",
        "Traditional_Experiment_Quiz",
        "Simulated_Experiment_Training",
        "Simulated_Experiment_Assesment",
        "Simulated_Experiment_Quiz",
        "Comparison_Between_Experiments",
        "Finish"
    ],
    "Phases_Completed": [
        "Introduction",
        "Traditional_Experiment_Training",
        "Traditional_Experiment_Assessment",
        "Traditional_Experiment_Quiz",
        "Simulated_Experiment_Training",
        "Simulated_Experiment_Assesment",
        "Simulated_Experiment_Quiz",
        "Comparison_Between_Experiments",
        "Finish"
    ]
    }
    """

    data = request.json # Get the data from the request

    email = data['email'] # Get email
    
    username = emailToUsername(email)
    user_file_path = pathUserName(username)

    with open(user_file_path, 'r') as file:
        data_user = json.load(file) # Load the user data

    if 'Phases' in data_user and 'Phases_completed' in data_user:
        return jsonify({"Phases": data_user['Phases'], "Phases_Completed": data_user['Phases_completed']}), 200
    else:
        return jsonify({'error': 'No hay fases'}), 404

@app.route('/API/MoveMouse', methods=['GET'])
def Move_Mouse():
    """
    Endpoint to move the mouse to a specific position.

    The mouse should move to the position (x, y) specified in the request.
    """
    time.sleep(1) # Wait 1 second
    # pyautogui.moveTo(900, 300)
    pyautogui.click(900, 300) # Move the mouse to the x, y and click
    
    time.sleep(1) # Wait 1 second
    # pyautogui.moveTo(1075, 650) # Move the mouse to the x, y and click
    pyautogui.click(1075, 650)

    return jsonify({'status': 'OK'}), 200


@app.route('/API/SaveVideo', methods=['POST'])
def Save_Video():
    if 'video' not in request.files:
        return jsonify({'status': 'No video file in request'}), 400

    video = request.files['video']
    email = request.form.get('email')
    experiment = request.form.get('experiment')

    username = email.split('@')[0]
    print(email)
    print(username)
    print(experiment)

    if video.filename == '':
        return jsonify({'status': 'No selected file'}), 400

    if video and email:

        filename = 'recording.webm'  # Puedes generar un nombre único si es necesario
        video_path = os.path.join(os.path.dirname(__file__), 'db', filename)
        fileName = os.path.join(os.path.dirname(__file__), 'db', f'{username}_{experiment}.webm')
        print(fileName)
        video.save(fileName)
        return jsonify({'status': 'Video saved', 'path': fileName}), 200

    return jsonify({'status': 'Failed to save video'}), 500



@app.route('/API/Solutions_Experiment_Traditional', methods=['GET'])
def Get_Solutions_Experiment_Traditional():
    """
    Endpoint to obtain solutions for an experiment.
    
    Returns a JSON with a list of solutions. Each solution contains:
    - id: Unique identifier of the solution
    - time: Time associated with the solution
    - risk: Risk level associated with the solution
    - arrival: Arrival time associated with the solution
    - time_normalized: Normalized time value
    - risk_normalized: Normalized risk value
    - arrival_normalized: Normalized arrival value
    
    Example response:
    {
        "solutions": [
                {
                    "arrival": 0.8547351436291185,
                    "arrival_normalized": 0.93775279,
                    "id": 27,
                    "risk": 1.0,
                    "risk_normalized": 0.95238095,
                    "time": 0.8189215064308476,
                    "time_normalized": 22.60391874
                },
                {
                    "arrival": 0.00013552002075421486,
                    "arrival_normalized": 0.00016533,
                    "id": 3,
                    "risk": 1.0,
                    "risk_normalized": 0.95238095,
                    "time": 0.34075900735323816,
                    "time_normalized": 10.65271578
                },
                {
                    "arrival": 0.007342445192255449,
                    "arrival_normalized": 0.0080721,
                    "id": 10,
                    "risk": 0.9975361173727239,
                    "risk_normalized": 0.95005879,
                    "time": 0.3152653554473582,
                    "time_normalized": 10.01552694
                },
                {
                    "arrival": 0.005972652063457751,
                    "arrival_normalized": 0.00656929,
                    "id": 28,
                    "risk": 1.0,
                    "risk_normalized": 0.95238095,
                    "time": 0.17697053210862104,
                    "time_normalized": 6.55898339
                }
        ]
    }
    """

    # Simulated data for the solutions.
    # NOTE: This should be replaced with the Algorithm to get the solutions
    # Define path to the file

    nameFile = 'obj_space_gen_001.out'  # Name of the file with the solutions
    filePath = os.path.join(os.path.dirname(__file__), 'solutions_test', nameFile) # Define the path to the file

    # Read the file and extract the data for lines
    with open(filePath, 'r') as file:
        lines = file.readlines() # Read the lines of the file

    # Process the data
    data = []
    for line in lines:
        values = line.split()  # Divided the line into values
        values = [float(value) for value in values]  # Convert the values to float
        data.append(values)  # Add the values to the data list

    time = [] # List to store the time values
    risk = [] # List to store the risk values
    arrive = [] # List to store the arrival values
    
    for values in data:
        time.append(values[0]) # Add the time value to the list
        risk.append(values[1]) # Add the risk value to the list
        arrive.append(values[2]) # Add the arrival value to the list

    min_time = min(time) # Get the minimum time value
    max_time = max(time) # Get the maximum time value

    min_risk = min(risk) # Get the minimum risk value
    max_risk = max(risk) # Get the maximum risk value

    min_arrive = min(arrive) # Get the minimum arrival value
    max_arrive = max(arrive) # Get the maximum arrival value

    # Get the solutions
    solutions = [] # List to store the solutions
    numbers_random = []
    for i in range(4):
        random_index = random.randint(0, len(data) - 1) # Get a random index for the solution
        
        while random_index in numbers_random:
            random_index = random.randint(0, len(data) - 1)

        numbers_random.append(random_index)

        # Create the solution object
        solution = {
            'nameFile': nameFile,
            'id': random_index,
            'time_normalized': data[random_index][0],
            'risk_normalized': data[random_index][1],
            'arrival_normalized': data[random_index][2],
            'time': ((data[random_index][0] - min_time) / (max_time - min_time)),
            'risk': ((data[random_index][1] - min_risk) / (max_risk - min_risk)),
            'arrival': ((data[random_index][2] - min_arrive) / (max_arrive - min_arrive)),
        }

        solutions.append(solution) # Add the solution to the list
    
    data = {
        'solutions': solutions
    }

    return jsonify(data), 200


@app.route('/API/Solutions_Experiment_Simulated', methods=['GET'])
def Get_Solutions_Experiment_Simulated():
    """
    Endpoint to obtain solutions for an experiment.

    Returns a JSON with a list of solutions. Each solution contains:
    - id: Unique identifier of the solution
    - time: Time associated with the solution
    - risk: Risk level associated with the solution
    - arrival: Arrival time associated with the solution

    Example response:
    {
        "solutions": [
            {
                "id": 1,
                "time": 12.34,
                "risk": 0.56,
                "arrival": 23.45
            },
            {
                "id": 2,
                "time": 67.89,
                "risk": 0.12,
                "arrival": 34.56
            },
            {
                "id": 3,
                "time": 78.90,
                "risk": 0.34,
                "arrival": 45.67
            },
            {
                "id": 4,
                "time": 56.78,
                "risk": 0.78,
                "arrival": 12.34
            }
        ]
    }
    """

    # Simulated data for the solutions NOTE: This should be replaced with the Algorithm to get the solutions
    # Define path to the file
    filePath = os.path.join(os.path.dirname(__file__), 'solutions_test', 'obj_space_gen_001.out')

    # Read the file and extract the data for lines
    with open(filePath, 'r') as file:
        lines = file.readlines()

    # Process the data
    data = []
    for line in lines:
        values = line.split()  # Divided the line into values
        values = [float(value) for value in values]  # Convert the values to float
        data.append(values)  # Add the values to the data list

    # Get the solutions
    solutions = [] # List to store the solutions
    numbers_random = []
    for i in range(4):
        random_index = random.randint(0, len(data) - 1) # Get a random index for the solution

        while random_index in numbers_random:
            random_index = random.randint(0, len(data) - 1)

        numbers_random.append(random_index)
        
        # Create the solution object
        solution = {
            'id': random_index,
            'time': data[random_index][0],
            'risk': data[random_index][1],
            'arrival': data[random_index][2]
        }

        solutions.append(solution) # Add the solution to the list
    
    data = {
        'solutions': solutions
    }

    return jsonify(data), 200

@app.route('/API/SaveSolution_Experiment_Traditional', methods=['POST'])
def SaveSolution_Experiment_Traditional():
    data = request.json
    
    email = data['email']
    username = email.split('@')[0]
    solution = data['solution']

    file_path = os.path.join(os.path.dirname(__file__), 'db')

    user_file_path = os.path.join(file_path, f'{username}.json')

    with open(user_file_path, 'r') as file:
        data_user = json.load(file)

    data_user['Solution_Experiment_Traditional'] = solution

    with open(user_file_path, 'w') as file:
        json.dump(data_user, file, indent=2)

    return jsonify({'status': 'OK'}), 200

@app.route('/API/SaveSolutions_Experiment_Simulated', methods=['POST'])
def SaveSolutions_Experiment_Traditional():
    data = request.json
    email = data['email']
    username = email.split('@')[0]

    solutions = data['solutions']
    type_ = data['type']

    print(solutions)
    print(type_)

    if type_ == 'Test':
        return jsonify({'status': 'OK'}), 200
    
    file_path = os.path.join(os.path.dirname(__file__), 'db')

    user_file_path = os.path.join(file_path, f'{username}.json')

    with open(user_file_path, 'r') as file:
        data_user = json.load(file)

    if 'Solutions_Experiment_Simulated' in data_user:
        data_user['Solutions_Experiment_Simulated'].append(solutions)
    else:
        data_user['Solutions_Experiment_Simulated'] = [solutions]

    with open(user_file_path, 'w') as file:
        json.dump(data_user, file, indent=2)

    return jsonify({'status': 'OK'}), 200

    
    
    

@app.route ('/API/InitSimulation', methods=['POST'])
def InitSimulation():
    """
    Endpoint to initialize the simulation with the parameters for a specific solution.
    
    The request should contain the following data:
    - id: Unique identifier of the solution to simulate
    
    The simulation should be run with the parameters of the solution and the results should be saved.
    
    Returns a JSON response with the status of the simulation.
    """
    data = request.json
    print(data)

    filePath = os.path.join(os.path.dirname(__file__), 'solutions_test', 'var_space_gen_001.out')

    with open(filePath, 'r') as file:
        lines = file.readlines()

    dataFile = []

    for line in lines:
        values = line.split()
        values = [float(value) for value in values]
        dataFile.append(values)

    params = dataFile[int(data['id']) ] # Get the parameters for the simulation in list format
    print(params) # Neural network weights

    """
    Code to run the simulation with the parameters

    *
    *
    *

    """

    return jsonify({'status': 'OK'}), 200

@app.route('/API/SaveSolutionEnd_Experiment_Simulated', methods=['POST'])
def SaveSolutionEnd_Experiment_Simulated():
    """
    Endpoint to save the results of the simulation for a specific solution.
    
    The request should contain the following data:
    - id: Unique identifier of the solution
    - results: Results of the simulation
    
    The results should be saved in the database.
    
    Returns a JSON response with the status of the operation.
    """
    data = request.json
    print(data)

    email = data['email']
    username = email.split('@')[0]

    file_path = os.path.join(os.path.dirname(__file__), 'db')

    user_file_path = os.path.join(file_path, f'{username}.json')

    with open(user_file_path, 'r') as file:
        data_user = json.load(file)

    data_user['Solution_Experiment_Simulated'] = data['solution']

    with open(user_file_path, 'w') as file:
        json.dump(data_user, file, indent=2)    
    

    return jsonify({'status': 'OK'}), 200

@app.route('/API/Quiz_Experiment_Simulated', methods=['POST'])
def Save_Quiz_Experiment_Simulated():
    data = request.json

    email = data['email']
    username = email.split('@')[0]

    print(username)

    file_path = os.path.join(os.path.dirname(__file__), 'db')

    user_file_path = os.path.join(file_path, f'{username}.json')

    print(user_file_path)

    with open(user_file_path, 'r') as file:
        data_user = json.load(file)

    data_user['Quiz_Experiment_Simulated'] = data['data']

    with open(user_file_path, 'w') as file:
        json.dump(data_user, file, indent=2)
    
    return jsonify({'status': 'OK'}), 200

@app.route('/API/GetVideo', methods=['POST'])
def GetVideo():
    data = request.json
    email = data['email']
    username = email.split('@')[0]

    print(username)

    file_path = os.path.join(os.path.dirname(__file__), 'db')

    videoTraditonalExperiment = os.path.join(file_path, f'{username}_Traditional_Experiment_Assessment.webm')

    print(videoTraditonalExperiment)

    if os.path.exists(videoTraditonalExperiment):
        return send_file(videoTraditonalExperiment, as_attachment=True, mimetype='video/webm')
    else:
        return jsonify({'status': 'ERROR', 'message': 'File not found'}), 404
    
@app.route('/API/SaveQuiz_Beetween_Experiments', methods=['POST'])
def SaveQuiz_Beetween_Experiments():
    data = request.json

    email = data['email']
    username = email.split('@')[0]

    print(data['data']) 

    method_select = data['data']['radio']
    if method_select == '1':
        method_select = 'GraphicLines'
    elif method_select == '2':
        method_select = 'Simulation'

    print(method_select)

    del data['data']['radio']
    

    data['data']['methodSelect'] = method_select

    print(data['data'])

    file_path = os.path.join(os.path.dirname(__file__), 'db')

    user_file_path = os.path.join(file_path, f'{username}.json')

    print(user_file_path)

    with open(user_file_path, 'r') as file:
        data_user = json.load(file)

    data_user['Quiz_Beetween_Experiments'] = data['data']

    with open(user_file_path, 'w') as file:
        json.dump(data_user, file, indent=2)
    
    return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':

    HOST = '127.0.0.1'
    PORT = 4000
    app.run(host=HOST, port=PORT,debug=True)

