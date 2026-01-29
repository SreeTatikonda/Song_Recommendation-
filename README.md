# MoodTune - AI-Powered Music Recommendation System

An intelligent music recommendation system that analyzes your mood through natural language and suggests perfect songs to match your emotional state.

## Features

- **Advanced Mood Detection**: Analyzes text input using keyword matching and sentiment scoring
- **9 Mood Categories**: Happy, Sad, Energetic, Calm, Romantic, Angry, Anxious, Nostalgic, Confident
- **Beautiful UI**: Retro-futuristic design with smooth animations and gradients
- **Dual Backend**: Both lightweight keyword-based and optional Spotify API integration
- **RESTful API**: Clean API endpoints for easy integration
- **Real-time Analysis**: Instant mood detection and song recommendations

## System Architecture

```
┌─────────────────┐
│   Frontend      │  React-based single-page app
│   (index.html)  │  - Mood input interface
└────────┬────────┘  - Results display
         │           - Beautiful animations
         ↓
┌─────────────────┐
│   Flask API     │  REST API Server
│ (api_server.py) │  - /analyze endpoint
└────────┬────────┘  - /moods endpoint
         │           - CORS enabled
         ↓
┌─────────────────┐
│  Mood Detector  │  Text Analysis Engine
│  (backend.py)   │  - Keyword matching
└────────┬────────┘  - Sentiment scoring
         │           - Emotion classification
         ↓
┌─────────────────┐
│   Music DB      │  Song Recommendations
│  (backend.py)   │  - Curated playlists
└─────────────────┘  - 45 songs across 9 moods

Optional:
┌─────────────────┐
│  Spotify API    │  Real Music Data
│ (spotify_*.py)  │  - Live recommendations
└─────────────────┘  - Preview URLs
```

## Project Structure

```
mood-music-app/
├── index.html              # Frontend React application
├── backend.py              # Core mood detection & recommendation engine
├── api_server.py           # Flask REST API server
├── spotify_integration.py  # Spotify API client (optional)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Quick Start

### Option 1: Standalone Frontend (No Installation)

Simply open `index.html` in your browser:

```bash
# Open the file in your browser
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows
```

The frontend works independently with built-in mood detection!

### Option 2: Full System with API

#### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt --break-system-packages
```

#### Step 2: Test the Backend

```bash
python backend.py
```

This will run test cases showing mood detection in action.

#### Step 3: Start the API Server

```bash
python api_server.py
```

Server will start on `http://localhost:5000`

#### Step 4: Open Frontend

Open `index.html` in your browser to use the full system.

##  Usage Examples

### Using the Web Interface

1. **Open the app** - Load `index.html` in your browser
2. **Describe your mood** - Type how you're feeling in the text area
3. **Get recommendations** - Click "Find My Music" to see personalized songs

### Example Inputs

- "I'm feeling happy and energetic today!"
- "Feeling a bit down and need some comfort"
- "Need some workout music to pump me up"
- "Want to relax and unwind after a long day"
- "In the mood for some romance"

### Using the API

```bash
# Analyze mood and get recommendations
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I am feeling happy today!", "num_songs": 5}'

# Get all available moods
curl http://localhost:5000/moods

# Get recommendations for specific mood
curl http://localhost:5000/recommend/energetic?num_songs=5
```

### Using Python Directly

```python
from backend import MoodTuneAPI

# Initialize the API
api = MoodTuneAPI()

# Analyze mood and get recommendations
result = api.analyze_and_recommend(
    "I'm feeling energetic and ready to workout!",
    num_songs=5
)

print(f"Detected Mood: {result['detected_mood']}")
print(f"Confidence: {result['confidence']}")

for song in result['recommendations']:
    print(f"  • {song['title']} - {song['artist']}")
```

##  Mood Categories

The system detects 9 distinct moods:

1. **Happy**  - Upbeat, feel-good music
2. **Sad**  - Emotional, comforting songs
3. **Energetic**  - High-energy workout tracks
4. **Calm**  - Peaceful, relaxing melodies
5. **Romantic**  - Love songs and tender ballads
6. **Angry**  - Intense, cathartic music
7. **Anxious**  - Soothing, reassuring tracks
8. **Nostalgic** - Classic throwback songs
9. **Confident**  - Empowering anthems

##  Advanced Configuration

### Spotify API Integration (Optional)

For real-time Spotify data and preview URLs:

1. **Get Spotify Credentials**:
   - Go to https://developer.spotify.com/dashboard
   - Create an app
   - Get your Client ID and Client Secret

2. **Set Environment Variables**:
   ```bash
   export SPOTIFY_CLIENT_ID='your_client_id'
   export SPOTIFY_CLIENT_SECRET='your_client_secret'
   ```

3. **Use Spotify Integration**:
   ```python
   from spotify_integration import SpotifyAPI
   
   spotify = SpotifyAPI()
   spotify.authenticate()
   songs = spotify.get_recommendations('happy', limit=10)
   ```

## API Endpoints

### `POST /analyze`

Analyze mood from text and get recommendations.

**Request:**
```json
{
  "text": "I'm feeling happy today!",
  "num_songs": 5
}
```

**Response:**
```json
{
  "user_input": "I'm feeling happy today!",
  "detected_mood": "happy",
  "confidence": 0.87,
  "intensity": "high",
  "recommendations": [
    {
      "title": "Happy",
      "artist": "Pharrell Williams",
      "year": 2013,
      "genre": "Pop",
      "energy": 0.8,
      "valence": 0.9,
      "tags": ["Pop", "Dance", "Positive"]
    }
  ],
  "emotion_scores": {
    "happy": 3,
    "sad": 0,
    "energetic": 1
  }
}
```

### `GET /moods`

Get all available mood categories.

**Response:**
```json
{
  "moods": [
    "happy", "sad", "energetic", "calm",
    "romantic", "angry", "anxious", "nostalgic", "confident"
  ]
}
```

### `GET /recommend/<mood>`

Get recommendations for a specific mood.

**Request:** `GET /recommend/energetic?num_songs=5`

**Response:**
```json
{
  "mood": "energetic",
  "recommendations": [...]
}
```

##  How It Works

### Mood Detection Algorithm

1. **Text Preprocessing**: Clean and normalize input text
2. **Keyword Matching**: Multi-level keyword detection
   - Primary keywords (weight: 3)
   - Secondary keywords (weight: 1)
   - Intensity keywords (weight: 5)
3. **Scoring**: Calculate weighted scores for each emotion
4. **Confidence Calculation**: Measure detection certainty
5. **Intensity Classification**: Determine emotion strength (low/medium/high)

### Recommendation Engine

1. **Mood Mapping**: Map detected emotion to song database
2. **Audio Feature Matching**: Songs categorized by:
   - Valence (positivity)
   - Energy level
   - Genre
   - Tags and mood descriptors
3. **Ranking**: Return top-matched songs
4. **Metadata**: Include artist, year, tags, and audio features

## Future Enhancements

- [ ] User authentication and playlist saving
- [ ] Machine learning model for better mood detection
- [ ] Multi-modal input (analyze images, voice)
- [ ] Real-time audio preview player
- [ ] Mood history tracking
- [ ] Social sharing features
- [ ] Integration with Apple Music, YouTube Music
- [ ] Mood-based radio stations
- [ ] Custom playlist generation

##  Tech Stack

**Frontend:**
- React 18
- Vanilla CSS with animations
- Custom gradient designs
- Responsive layout

**Backend:**
- Python 3.8+
- Flask (REST API)
- Custom NLP engine
- Spotify Web API (optional)

**Key Features:**
- Zero-config frontend (works standalone)
- RESTful API architecture
- Modular design
- Comprehensive error handling
- CORS enabled for cross-origin requests

##  Testing

Run the backend tests:

```bash
# Test mood detection engine
python backend.py

# Test Spotify integration
python spotify_integration.py

# Test API server (manual testing with curl/Postman)
python api_server.py
```

## Contributing

Contributions are welcome! Areas for improvement:

1. Add more songs to the database
2. Improve mood detection accuracy
3. Add new mood categories
4. Enhance UI/UX design
5. Add unit tests
6. Create Docker configuration
7. Add database persistence

## License

This project is open source and available for educational purposes.

## Acknowledgments

- Spotify Web API for music data
- HuggingFace for NLP inspiration
- React for frontend framework
- Flask for API framework

---

**Built by Yashu**

*Making music discovery emotional and intelligent.*
