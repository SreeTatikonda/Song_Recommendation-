"""
Spotify API Integration for MoodTune
Fetches real song data from Spotify based on detected mood
"""

import os
from typing import List, Dict, Optional
import requests
import base64


class SpotifyAPI:
    """
    Spotify API client for fetching song recommendations
    """
    
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        """
        Initialize Spotify API client
        
        Args:
            client_id: Spotify API client ID (from environment or parameter)
            client_secret: Spotify API client secret (from environment or parameter)
        """
        self.client_id = client_id or os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('SPOTIFY_CLIENT_SECRET')
        self.access_token = None
        self.token_url = 'https://accounts.spotify.com/api/token'
        self.api_base_url = 'https://api.spotify.com/v1'
        
        # Mood to Spotify audio features mapping
        self.mood_features = {
            'happy': {
                'target_valence': 0.8,
                'target_energy': 0.7,
                'seed_genres': ['pop', 'dance', 'funk']
            },
            'sad': {
                'target_valence': 0.3,
                'target_energy': 0.4,
                'seed_genres': ['acoustic', 'piano', 'sad']
            },
            'energetic': {
                'target_valence': 0.6,
                'target_energy': 0.9,
                'seed_genres': ['rock', 'edm', 'workout']
            },
            'calm': {
                'target_valence': 0.5,
                'target_energy': 0.3,
                'seed_genres': ['ambient', 'chill', 'classical']
            },
            'romantic': {
                'target_valence': 0.7,
                'target_energy': 0.5,
                'seed_genres': ['r-n-b', 'soul', 'romance']
            },
            'angry': {
                'target_valence': 0.3,
                'target_energy': 0.9,
                'seed_genres': ['metal', 'hard-rock', 'punk']
            },
            'anxious': {
                'target_valence': 0.4,
                'target_energy': 0.5,
                'seed_genres': ['alternative', 'indie', 'folk']
            },
            'nostalgic': {
                'target_valence': 0.6,
                'target_energy': 0.6,
                'seed_genres': ['classic-rock', 'oldies', 'retro']
            },
            'confident': {
                'target_valence': 0.7,
                'target_energy': 0.8,
                'seed_genres': ['hip-hop', 'rap', 'power']
            }
        }
    
    def authenticate(self) -> bool:
        """
        Authenticate with Spotify API using client credentials flow
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        if not self.client_id or not self.client_secret:
            print("Warning: Spotify credentials not provided. Using mock data.")
            return False
        
        try:
            # Encode credentials
            auth_string = f"{self.client_id}:{self.client_secret}"
            auth_bytes = auth_string.encode('utf-8')
            auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
            
            # Request token
            headers = {
                'Authorization': f'Basic {auth_base64}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {'grant_type': 'client_credentials'}
            
            response = requests.post(self.token_url, headers=headers, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data['access_token']
            
            print("Successfully authenticated with Spotify API")
            return True
            
        except Exception as e:
            print(f"Spotify authentication failed: {str(e)}")
            return False
    
    def get_recommendations(self, mood: str, limit: int = 10) -> List[Dict]:
        """
        Get song recommendations from Spotify based on mood
        
        Args:
            mood: Detected mood (happy, sad, energetic, etc.)
            limit: Number of recommendations to return
        
        Returns:
            List of song dictionaries
        """
        if not self.access_token:
            if not self.authenticate():
                return self._get_mock_recommendations(mood, limit)
        
        try:
            mood_params = self.mood_features.get(mood, self.mood_features['calm'])
            
            # Build Spotify recommendations API request
            endpoint = f"{self.api_base_url}/recommendations"
            
            params = {
                'seed_genres': ','.join(mood_params['seed_genres'][:2]),
                'target_valence': mood_params['target_valence'],
                'target_energy': mood_params['target_energy'],
                'limit': limit
            }
            
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Format response
            recommendations = []
            for track in data.get('tracks', []):
                song = {
                    'title': track['name'],
                    'artist': ', '.join([artist['name'] for artist in track['artists']]),
                    'album': track['album']['name'],
                    'year': track['album']['release_date'][:4] if track['album'].get('release_date') else 'N/A',
                    'preview_url': track.get('preview_url'),
                    'spotify_url': track['external_urls']['spotify'],
                    'album_art': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'duration_ms': track['duration_ms'],
                    'popularity': track['popularity']
                }
                recommendations.append(song)
            
            return recommendations
            
        except Exception as e:
            print(f"Error fetching Spotify recommendations: {str(e)}")
            return self._get_mock_recommendations(mood, limit)
    
    def _get_mock_recommendations(self, mood: str, limit: int) -> List[Dict]:
        """
        Return mock recommendations when Spotify API is unavailable
        """
        # This would return the curated list from the database
        from backend import MusicRecommender
        recommender = MusicRecommender()
        return recommender.get_recommendations(mood, limit)
    
    def search_track(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Search for tracks on Spotify
        
        Args:
            query: Search query
            limit: Number of results
        
        Returns:
            List of track dictionaries
        """
        if not self.access_token:
            if not self.authenticate():
                return []
        
        try:
            endpoint = f"{self.api_base_url}/search"
            
            params = {
                'q': query,
                'type': 'track',
                'limit': limit
            }
            
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            tracks = []
            for track in data.get('tracks', {}).get('items', []):
                track_info = {
                    'title': track['name'],
                    'artist': ', '.join([artist['name'] for artist in track['artists']]),
                    'album': track['album']['name'],
                    'spotify_url': track['external_urls']['spotify'],
                    'preview_url': track.get('preview_url'),
                    'popularity': track['popularity']
                }
                tracks.append(track_info)
            
            return tracks
            
        except Exception as e:
            print(f"Error searching Spotify: {str(e)}")
            return []


# Setup instructions for Spotify API
SETUP_INSTRUCTIONS = """
To use Spotify API integration:

1. Create a Spotify Developer Account:
   - Go to https://developer.spotify.com/dashboard
   - Log in with your Spotify account (or create one)

2. Create an App:
   - Click "Create an App"
   - Fill in app name and description
   - Accept terms and conditions

3. Get Your Credentials:
   - After creating the app, you'll see your Client ID
   - Click "Show Client Secret" to reveal your Client Secret

4. Set Environment Variables:
   export SPOTIFY_CLIENT_ID='your_client_id_here'
   export SPOTIFY_CLIENT_SECRET='your_client_secret_here'

5. Install required package:
   pip install requests --break-system-packages

Note: The system will work without Spotify API credentials using
curated song database, but Spotify integration provides real-time
music data and preview URLs.
"""


if __name__ == '__main__':
    print("=" * 80)
    print("Spotify API Integration Test")
    print("=" * 80)
    print()
    
    # Test Spotify API
    spotify = SpotifyAPI()
    
    if spotify.authenticate():
        print("\n✓ Successfully connected to Spotify API")
        
        # Test mood-based recommendations
        mood = 'happy'
        print(f"\nFetching {mood} recommendations from Spotify...")
        recommendations = spotify.get_recommendations(mood, limit=5)
        
        print(f"\nTop 5 {mood} songs:")
        print("-" * 60)
        for i, song in enumerate(recommendations, 1):
            print(f"{i}. {song['title']} - {song['artist']}")
            if song.get('spotify_url'):
                print(f"   Listen: {song['spotify_url']}")
        print()
    else:
        print("\n⚠ Spotify API not configured")
        print("\nSetup Instructions:")
        print(SETUP_INSTRUCTIONS)
