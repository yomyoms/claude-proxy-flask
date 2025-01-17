from flask import Flask, request, Response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/proxy/v1/messages', methods=['GET', 'POST'])
def proxy():
    if request.method == 'POST':
        req_data = request.get_json()
        
        # Extract bearer token and convert to x-api-key
        auth_header = request.headers.get('Authorization')
        api_key = auth_header.replace('Bearer ', '') if auth_header else None
        
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': api_key
        }
        
        response = requests.post('https://api.aimlapi.com/v1/messages', json=req_data, headers=headers)
        
        # Return response with status code 200
        return Response(
            response.content,
            status=200,
            mimetype='application/json'
        )
    else:
        return {'error': 'This endpoint supports only POST requests'}, 405

if __name__ == '__main__':
    app.run(port=5000)
