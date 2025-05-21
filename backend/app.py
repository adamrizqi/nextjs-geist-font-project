from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from collections import deque
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Define mall graph structure based on the map
MALL_GRAPH = {
    # West Mall nodes
    'DS1': ['MA9', 'W11'],
    'MA9': ['DS1', 'W22'],
    'W11': ['DS1', 'W10'],
    'W10': ['W11', 'W9'],
    'W9': ['W10', 'W8'],
    'W8': ['W9', 'W7'],
    'W7': ['W8', 'W6'],
    'W6': ['W7', 'W5'],
    'W5': ['W6', 'W4'],
    'W4': ['W5', 'W3A'],
    'W3A': ['W4', 'W3'],
    
    # Sky Bridge nodes
    'SB1': ['W3', 'E1'],
    'W3': ['W3A', 'SB1'],
    'E1': ['SB1', 'E2'],
    
    # East Mall nodes
    'MA1': ['E47', 'E43'],
    'E47': ['MA1', 'E46'],
    'E46': ['E47', 'E45'],
    'E45': ['E46', 'E44'],
    'E43': ['MA1', 'E42'],
    'E42': ['E43', 'E41B'],
    'E41B': ['E42', 'E40'],
    'E40': ['E41B', 'E39'],
    'E39': ['E40', 'E38'],
    'E38': ['E39', 'E37'],
    'E37': ['E38', 'E36'],
    'E36': ['E37', 'E35'],
    'E35': ['E36', 'E34'],
    'E34': ['E35', 'E33A'],
    'E33A': ['E34', 'E33'],
}

# Node coordinates mapping
NODE_COORDS = {
    # West Mall coordinates
    'DS1': {'x': 200, 'y': 150},
    'MA9': {'x': 250, 'y': 200},
    'W11': {'x': 100, 'y': 50},
    # Add more coordinates for each node...
}

def find_closest_node(point):
    """Find the closest node to a clicked point"""
    min_distance = float('inf')
    closest_node = None
    
    for node, coords in NODE_COORDS.items():
        dx = point['x'] - coords['x']
        dy = point['y'] - coords['y']
        distance = (dx * dx + dy * dy) ** 0.5
        
        if distance < min_distance:
            min_distance = distance
            closest_node = node
    
    return closest_node

def bfs(start_node, end_node):
    """Find shortest path using BFS"""
    queue = deque([[start_node]])
    visited = {start_node}

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == end_node:
            return path

        for neighbor in MALL_GRAPH.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return []

@app.route('/find-path', methods=['POST', 'OPTIONS'])
def find_path():
    if request.method == 'OPTIONS':
        return make_response('', 200)

    try:
        data = request.json
        if not data or 'start' not in data or 'end' not in data:
            return jsonify({'error': 'Invalid request data'}), 400

        start_point = data['start']
        end_point = data['end']

        # Convert clicked points to graph nodes
        start_node = find_closest_node(start_point)
        end_node = find_closest_node(end_point)

        if not start_node or not end_node:
            return jsonify({'error': 'Invalid points selected'}), 400

        # Find path using BFS
        path = bfs(start_node, end_node)

        if not path:
            return jsonify({'error': 'No path found between selected points'}), 404

        # Convert path nodes back to coordinates
        path_coords = [NODE_COORDS[node] for node in path]

        return jsonify({'path': path_coords})
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
