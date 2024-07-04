# SERVER CEREBRAL EXPERIMENTS

## Requerimientos
- Python 3.11.9

## Bibliotecas
- Flask
- flask_cors
- pyautogui

## Instalación

Para ejecutar este proyecto localmente, necesitarás instalar las siguientes dependencias:

1. Flask
    ```bash
    pip install Flask
    ```

2. flask_cors
    ```bash
    pip install Flask-Cors
    ```

3. pyautogui
    ```bash
    pip install PyAutoGUI
    ```

## Ejecutando el servidor

Para iniciar el servidor, abre una terminal y ejecuta:

```bash
python3 main.py
```

## Tests
Para probar los endpoints de la API, puedes utilizar la extensión Thunder Client en VS Code o cualquier otro sistema de pruebas de APIs.

- Thunder Client: https://marketplace.visualstudio.com/items?itemName=rangav.vscode-thunder-client

Ejemplo de prueba de endpoint

1. Configura una nueva solicitud en Thunder Client con los siguientes detalles:
- URL: http://127.0.0.1:4000/API/Solutions_Experiment_Traditional
- METHOD: GET

2. Ejecuta la solicitud y verifica la respuesta.

```json
  {
  "solutions": [
    {
      "arrival": 0.0006957113683149689,
      "arrival_normalized": 0.00077992,
      "id": 39,
      "nameFile": "obj_space_gen_001.out",
      "risk": 0.5686918266145414,
      "risk_normalized": 0.54588164,
      "time": 0.014258559973020888,
      "time_normalized": 2.49215714
    },
    {
      "arrival": 0.0037391421168870755,
      "arrival_normalized": 0.00411889,
      "id": 35,
      "nameFile": "obj_space_gen_001.out",
      "risk": 1.0,
      "risk_normalized": 0.95238095,
      "time": 0.30823399588427464,
      "time_normalized": 9.839785
    },
    {
      "arrival": 0.0006631256759423352,
      "arrival_normalized": 0.00074417,
      "id": 17,
      "nameFile": "obj_space_gen_001.out",
      "risk": 0.4211974013749852,
      "risk_normalized": 0.4068711,
      "time": 0.2367355704317203,
      "time_normalized": 8.05275194
    },
    {
      "arrival": 0.002970338533988568,
      "arrival_normalized": 0.00327543,
      "id": 55,
      "nameFile": "obj_space_gen_001.out",
      "risk": 0.6336823013191708,
      "risk_normalized": 0.60713386,
      "time": 0.014462657995063813,
      "time_normalized": 2.49725837
    }
  ]
}
```