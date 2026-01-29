"""
Flask API Server for MoodTune
Provides REST endpoints for mood detection and music recommendations
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from backend import MoodTuneAPI
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Initialize MoodTune API
moodtune = MoodTuneAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'service': 'MoodTune API',
        'version': '1.0.0',
        'endpoints': {
            '/analyze': 'POST - Analyze mood and get recommendations',
            '/moods': 'GET - Get all available moods',
            '/health': 'GET - Health check'
        }
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


@app.route('/analyze', methods=['POST'])
def analyze_mood():
    """
    Analyze user mood and return song recommendations
    
    Request body:
    {
        "text": "I'm feeling happy today!",
        "num_songs": 5  # optional, defaults to 5
    }
    
    Response:
    {
        "user_input": "...",
        "detected_mood": "happy",
        "confidence": 0.85,
        "intensity": "high",
        "recommendations": [...],
        "emotion_scores": {...}
    }
    """
    try:
        data = request.get_json()
        
        # Validate request
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing required field: text'
            }), 400
        
        user_text = data['text']
        num_songs = data.get('num_songs', 5)
        
        # Validate num_songs
        if not isinstance(num_songs, int) or num_songs < 1 or num_songs > 20:
            return jsonify({
                'error': 'num_songs must be an integer between 1 and 20'
            }), 400
        
        # Process request
        logger.info(f"Analyzing mood for text: {user_text[:50]}...")
        result = moodtune.analyze_and_recommend(user_text, num_songs)
        
        logger.info(f"Detected mood: {result['detected_mood']} (confidence: {result['confidence']})")
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/moods', methods=['GET'])
def get_moods():
    """
    Get list of all available moods
    
    Response:
    {
        "moods": ["happy", "sad", "energetic", ...]
    }
    """
    try:
        moods = moodtune.recommender.get_all_moods()
        return jsonify({'moods': moods}), 200
        
    except Exception as e:
        logger.error(f"Error getting moods: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/recommend/<mood>', methods=['GET'])
def recommend_by_mood(mood):
    """
    Get recommendations for a specific mood
    
    Query params:
    - num_songs: number of songs to return (default: 5)
    
    Response:
    {
        "mood": "happy",
        "recommendations": [...]
    }
    """
    try:
        num_songs = request.args.get('num_songs', 5, type=int)
        
        # Validate num_songs
        if num_songs < 1 or num_songs > 20:
            return jsonify({
                'error': 'num_songs must be between 1 and 20'
            }), 400
        
        # Check if mood exists
        available_moods = moodtune.recommender.get_all_moods()
        if mood not in available_moods:
            return jsonify({
                'error': f'Invalid mood. Available moods: {", ".join(available_moods)}'
            }), 400
        
        recommendations = moodtune.recommender.get_recommendations(mood, num_songs)
        
        return jsonify({
            'mood': mood,
            'recommendations': recommendations
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint does not exist'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500


if __name__ == '__main__':
    print("=" * 80)
    print("MoodTune API Server Starting...")
    print("=" * 80)
    print("\nAvailable endpoints:")
    print("  GET  /              - API information")
    print("  GET  /health        - Health check")
    print("  POST /analyze       - Analyze mood and get recommendations")
    print("  GET  /moods         - Get all available moods")
    print("  GET  /recommend/<mood> - Get recommendations for specific mood")
    print("\n" + "=" * 80)
    print()
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )
