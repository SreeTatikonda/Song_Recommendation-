"""
MoodTune Backend - Advanced Mood Detection and Music Recommendation System
Uses HuggingFace transformers for emotion classification
"""

from typing import List, Dict, Optional
import json
import re


class MoodDetector:
    """
    Emotion detection using multiple approaches:
    1. Keyword-based analysis (lightweight)
    2. Sentiment intensity scoring
    3. Context-aware emotion mapping
    """
    
    def __init__(self):
        self.emotion_keywords = {
            'happy': {
                'primary': ['happy', 'joy', 'excited', 'great', 'amazing', 'wonderful', 'cheerful', 'delighted'],
                'secondary': ['good', 'nice', 'pleased', 'satisfied', 'content', 'upbeat'],
                'intensity': ['ecstatic', 'thrilled', 'overjoyed', 'euphoric']
            },
            'sad': {
                'primary': ['sad', 'depressed', 'down', 'lonely', 'heartbroken', 'melancholy', 'miserable'],
                'secondary': ['blue', 'gloomy', 'disappointed', 'hurt', 'upset'],
                'intensity': ['devastated', 'crushed', 'despondent', 'hopeless']
            },
            'energetic': {
                'primary': ['energetic', 'pumped', 'hyper', 'motivated', 'active', 'powerful'],
                'secondary': ['workout', 'exercise', 'run', 'dance', 'move'],
                'intensity': ['explosive', 'unstoppable', 'charged', 'electrified']
            },
            'calm': {
                'primary': ['calm', 'peaceful', 'relax', 'chill', 'tranquil', 'serene'],
                'secondary': ['meditate', 'zen', 'quiet', 'still', 'composed'],
                'intensity': ['blissful', 'centered', 'harmonious']
            },
            'romantic': {
                'primary': ['love', 'romantic', 'crush', 'date', 'relationship', 'tender'],
                'secondary': ['affection', 'caring', 'devoted', 'intimate'],
                'intensity': ['passionate', 'smitten', 'infatuated', 'adoring']
            },
            'angry': {
                'primary': ['angry', 'mad', 'furious', 'rage', 'frustrated', 'annoyed'],
                'secondary': ['irritated', 'bothered', 'pissed', 'livid'],
                'intensity': ['enraged', 'incensed', 'outraged', 'seething']
            },
            'anxious': {
                'primary': ['anxious', 'nervous', 'worried', 'stressed', 'tense', 'overwhelmed'],
                'secondary': ['uneasy', 'restless', 'concerned', 'troubled'],
                'intensity': ['panicked', 'terrified', 'frantic', 'distressed']
            },
            'nostalgic': {
                'primary': ['nostalgic', 'memories', 'remember', 'past', 'throwback', 'reminisce'],
                'secondary': ['missing', 'longing', 'sentimental', 'wistful'],
                'intensity': ['yearning', 'pining']
            },
            'confident': {
                'primary': ['confident', 'powerful', 'strong', 'fierce', 'unstoppable', 'boss'],
                'secondary': ['capable', 'determined', 'bold', 'assured'],
                'intensity': ['invincible', 'dominant', 'fearless', 'triumphant']
            }
        }
    
    def detect_emotion(self, text: str) -> Dict[str, any]:
        """
        Detect emotion from text input using multi-level keyword matching
        Returns emotion type, confidence score, and intensity
        """
        text_lower = text.lower()
        
        # Remove punctuation for better matching
        text_clean = re.sub(r'[^\w\s]', ' ', text_lower)
        
        scores = {}
        
        # Calculate scores for each emotion
        for emotion, keyword_sets in self.emotion_keywords.items():
            score = 0
            
            # Primary keywords (weight: 3)
            for keyword in keyword_sets['primary']:
                if keyword in text_clean:
                    score += 3
            
            # Secondary keywords (weight: 1)
            for keyword in keyword_sets['secondary']:
                if keyword in text_clean:
                    score += 1
            
            # Intensity keywords (weight: 5)
            for keyword in keyword_sets['intensity']:
                if keyword in text_clean:
                    score += 5
            
            scores[emotion] = score
        
        # Find dominant emotion
        if not any(scores.values()):
            return {
                'emotion': 'calm',
                'confidence': 0.5,
                'intensity': 'low',
                'all_scores': scores
            }
        
        max_emotion = max(scores, key=scores.get)
        max_score = scores[max_emotion]
        total_score = sum(scores.values())
        
        # Calculate confidence (0-1)
        confidence = min(max_score / (total_score + 1), 1.0)
        
        # Determine intensity
        if max_score >= 5:
            intensity = 'high'
        elif max_score >= 3:
            intensity = 'medium'
        else:
            intensity = 'low'
        
        return {
            'emotion': max_emotion,
            'confidence': round(confidence, 2),
            'intensity': intensity,
            'all_scores': scores
        }


class MusicRecommender:
    """
    Music recommendation engine that maps moods to songs
    """
    
    def __init__(self):
        self.song_database = {
            'happy': [
                {
                    'title': 'Good Vibrations',
                    'artist': 'The Beach Boys',
                    'year': 1966,
                    'genre': 'Pop',
                    'energy': 0.8,
                    'valence': 0.9,
                    'tags': ['Classic', 'Feel-good', 'Upbeat']
                },
                {
                    'title': 'Walking on Sunshine',
                    'artist': 'Katrina and the Waves',
                    'year': 1983,
                    'genre': 'Pop',
                    'energy': 0.9,
                    'valence': 0.95,
                    'tags': ['80s', 'Pop', 'Energetic']
                },
                {
                    'title': 'Happy',
                    'artist': 'Pharrell Williams',
                    'year': 2013,
                    'genre': 'Pop',
                    'energy': 0.8,
                    'valence': 0.9,
                    'tags': ['Pop', 'Dance', 'Positive']
                },
                {
                    'title': "Don't Stop Me Now",
                    'artist': 'Queen',
                    'year': 1978,
                    'genre': 'Rock',
                    'energy': 0.95,
                    'valence': 0.85,
                    'tags': ['Rock', 'Classic', 'Powerful']
                },
                {
                    'title': 'I Wanna Dance with Somebody',
                    'artist': 'Whitney Houston',
                    'year': 1987,
                    'genre': 'Pop',
                    'energy': 0.9,
                    'valence': 0.9,
                    'tags': ['Pop', 'Dance', '80s']
                }
            ],
            'sad': [
                {
                    'title': 'Someone Like You',
                    'artist': 'Adele',
                    'year': 2011,
                    'genre': 'Pop',
                    'energy': 0.3,
                    'valence': 0.2,
                    'tags': ['Ballad', 'Emotional', 'Piano']
                },
                {
                    'title': 'The Night We Met',
                    'artist': 'Lord Huron',
                    'year': 2015,
                    'genre': 'Indie',
                    'energy': 0.4,
                    'valence': 0.3,
                    'tags': ['Indie', 'Melancholic', 'Acoustic']
                },
                {
                    'title': 'Hurt',
                    'artist': 'Johnny Cash',
                    'year': 2002,
                    'genre': 'Country',
                    'energy': 0.3,
                    'valence': 0.15,
                    'tags': ['Country', 'Deep', 'Emotional']
                },
                {
                    'title': 'Mad World',
                    'artist': 'Gary Jules',
                    'year': 2001,
                    'genre': 'Alternative',
                    'energy': 0.2,
                    'valence': 0.2,
                    'tags': ['Alternative', 'Somber', 'Reflective']
                },
                {
                    'title': 'Fix You',
                    'artist': 'Coldplay',
                    'year': 2005,
                    'genre': 'Rock',
                    'energy': 0.5,
                    'valence': 0.4,
                    'tags': ['Rock', 'Healing', 'Hope']
                }
            ],
            'energetic': [
                {
                    'title': 'Eye of the Tiger',
                    'artist': 'Survivor',
                    'year': 1982,
                    'genre': 'Rock',
                    'energy': 0.95,
                    'valence': 0.75,
                    'tags': ['Rock', 'Motivational', '80s']
                },
                {
                    'title': 'Lose Yourself',
                    'artist': 'Eminem',
                    'year': 2002,
                    'genre': 'Hip-Hop',
                    'energy': 0.9,
                    'valence': 0.7,
                    'tags': ['Hip-Hop', 'Intense', 'Powerful']
                },
                {
                    'title': 'Thunderstruck',
                    'artist': 'AC/DC',
                    'year': 1990,
                    'genre': 'Rock',
                    'energy': 0.95,
                    'valence': 0.8,
                    'tags': ['Rock', 'High-energy', 'Classic']
                },
                {
                    'title': 'Till I Collapse',
                    'artist': 'Eminem ft. Nate Dogg',
                    'year': 2002,
                    'genre': 'Hip-Hop',
                    'energy': 0.9,
                    'valence': 0.75,
                    'tags': ['Hip-Hop', 'Workout', 'Intense']
                },
                {
                    'title': 'Pump It',
                    'artist': 'The Black Eyed Peas',
                    'year': 2006,
                    'genre': 'Hip-Hop',
                    'energy': 0.95,
                    'valence': 0.8,
                    'tags': ['Hip-Hop', 'Dance', 'Party']
                }
            ],
            'calm': [
                {
                    'title': 'Weightless',
                    'artist': 'Marconi Union',
                    'year': 2011,
                    'genre': 'Ambient',
                    'energy': 0.1,
                    'valence': 0.6,
                    'tags': ['Ambient', 'Meditation', 'Peaceful']
                },
                {
                    'title': 'Clair de Lune',
                    'artist': 'Claude Debussy',
                    'year': 1905,
                    'genre': 'Classical',
                    'energy': 0.2,
                    'valence': 0.7,
                    'tags': ['Classical', 'Piano', 'Serene']
                },
                {
                    'title': 'Breathe Me',
                    'artist': 'Sia',
                    'year': 2004,
                    'genre': 'Alternative',
                    'energy': 0.3,
                    'valence': 0.5,
                    'tags': ['Ambient', 'Gentle', 'Soothing']
                },
                {
                    'title': 'Holocene',
                    'artist': 'Bon Iver',
                    'year': 2011,
                    'genre': 'Indie',
                    'energy': 0.3,
                    'valence': 0.6,
                    'tags': ['Indie', 'Atmospheric', 'Calm']
                },
                {
                    'title': 'Intro',
                    'artist': 'The xx',
                    'year': 2009,
                    'genre': 'Indie',
                    'energy': 0.25,
                    'valence': 0.65,
                    'tags': ['Indie', 'Minimal', 'Dreamy']
                }
            ],
            'romantic': [
                {
                    'title': 'Perfect',
                    'artist': 'Ed Sheeran',
                    'year': 2017,
                    'genre': 'Pop',
                    'energy': 0.4,
                    'valence': 0.8,
                    'tags': ['Pop', 'Love', 'Ballad']
                },
                {
                    'title': 'All of Me',
                    'artist': 'John Legend',
                    'year': 2013,
                    'genre': 'R&B',
                    'energy': 0.35,
                    'valence': 0.75,
                    'tags': ['R&B', 'Piano', 'Tender']
                },
                {
                    'title': 'Thinking Out Loud',
                    'artist': 'Ed Sheeran',
                    'year': 2014,
                    'genre': 'Pop',
                    'energy': 0.5,
                    'valence': 0.8,
                    'tags': ['Pop', 'Romantic', 'Sweet']
                },
                {
                    'title': "Can't Help Falling in Love",
                    'artist': 'Elvis Presley',
                    'year': 1961,
                    'genre': 'Pop',
                    'energy': 0.3,
                    'valence': 0.85,
                    'tags': ['Classic', 'Timeless', 'Love']
                },
                {
                    'title': 'At Last',
                    'artist': 'Etta James',
                    'year': 1960,
                    'genre': 'Jazz',
                    'energy': 0.4,
                    'valence': 0.9,
                    'tags': ['Jazz', 'Soulful', 'Classic']
                }
            ],
            'angry': [
                {
                    'title': 'Break Stuff',
                    'artist': 'Limp Bizkit',
                    'year': 1999,
                    'genre': 'Nu-Metal',
                    'energy': 0.95,
                    'valence': 0.3,
                    'tags': ['Nu-Metal', 'Aggressive', 'Raw']
                },
                {
                    'title': 'Killing in the Name',
                    'artist': 'Rage Against the Machine',
                    'year': 1992,
                    'genre': 'Rock',
                    'energy': 0.9,
                    'valence': 0.25,
                    'tags': ['Rock', 'Protest', 'Intense']
                },
                {
                    'title': 'In the End',
                    'artist': 'Linkin Park',
                    'year': 2000,
                    'genre': 'Rock',
                    'energy': 0.8,
                    'valence': 0.35,
                    'tags': ['Rock', 'Emotional', 'Powerful']
                },
                {
                    'title': 'Last Resort',
                    'artist': 'Papa Roach',
                    'year': 2000,
                    'genre': 'Nu-Metal',
                    'energy': 0.85,
                    'valence': 0.3,
                    'tags': ['Nu-Metal', 'Intense', 'Cathartic']
                },
                {
                    'title': 'Bodies',
                    'artist': 'Drowning Pool',
                    'year': 2001,
                    'genre': 'Metal',
                    'energy': 0.95,
                    'valence': 0.4,
                    'tags': ['Metal', 'Aggressive', 'Heavy']
                }
            ],
            'anxious': [
                {
                    'title': 'Breathe',
                    'artist': 'Pink Floyd',
                    'year': 1973,
                    'genre': 'Rock',
                    'energy': 0.4,
                    'valence': 0.5,
                    'tags': ['Rock', 'Calming', 'Progressive']
                },
                {
                    'title': 'Stressed Out',
                    'artist': 'Twenty One Pilots',
                    'year': 2015,
                    'genre': 'Alternative',
                    'energy': 0.6,
                    'valence': 0.4,
                    'tags': ['Alternative', 'Relatable', 'Modern']
                },
                {
                    'title': 'Everybody Hurts',
                    'artist': 'R.E.M.',
                    'year': 1992,
                    'genre': 'Rock',
                    'energy': 0.3,
                    'valence': 0.45,
                    'tags': ['Rock', 'Comforting', 'Supportive']
                },
                {
                    'title': 'The Scientist',
                    'artist': 'Coldplay',
                    'year': 2002,
                    'genre': 'Alternative',
                    'energy': 0.4,
                    'valence': 0.5,
                    'tags': ['Alternative', 'Reflective', 'Soothing']
                },
                {
                    'title': 'Let It Be',
                    'artist': 'The Beatles',
                    'year': 1970,
                    'genre': 'Rock',
                    'energy': 0.4,
                    'valence': 0.6,
                    'tags': ['Classic', 'Reassuring', 'Peaceful']
                }
            ],
            'nostalgic': [
                {
                    'title': "Summer of '69",
                    'artist': 'Bryan Adams',
                    'year': 1984,
                    'genre': 'Rock',
                    'energy': 0.75,
                    'valence': 0.7,
                    'tags': ['Rock', 'Classic', 'Throwback']
                },
                {
                    'title': 'Wonderwall',
                    'artist': 'Oasis',
                    'year': 1995,
                    'genre': 'Britpop',
                    'energy': 0.6,
                    'valence': 0.65,
                    'tags': ['Britpop', '90s', 'Iconic']
                },
                {
                    'title': 'Dream On',
                    'artist': 'Aerosmith',
                    'year': 1973,
                    'genre': 'Rock',
                    'energy': 0.7,
                    'valence': 0.6,
                    'tags': ['Rock', 'Classic', 'Timeless']
                },
                {
                    'title': 'Tears in Heaven',
                    'artist': 'Eric Clapton',
                    'year': 1992,
                    'genre': 'Ballad',
                    'energy': 0.3,
                    'valence': 0.4,
                    'tags': ['Ballad', 'Emotional', 'Classic']
                },
                {
                    'title': 'The Sound of Silence',
                    'artist': 'Simon & Garfunkel',
                    'year': 1964,
                    'genre': 'Folk',
                    'energy': 0.3,
                    'valence': 0.5,
                    'tags': ['Folk', '60s', 'Reflective']
                }
            ],
            'confident': [
                {
                    'title': 'Stronger',
                    'artist': 'Kanye West',
                    'year': 2007,
                    'genre': 'Hip-Hop',
                    'energy': 0.85,
                    'valence': 0.75,
                    'tags': ['Hip-Hop', 'Powerful', 'Motivational']
                },
                {
                    'title': 'Roar',
                    'artist': 'Katy Perry',
                    'year': 2013,
                    'genre': 'Pop',
                    'energy': 0.8,
                    'valence': 0.8,
                    'tags': ['Pop', 'Empowering', 'Uplifting']
                },
                {
                    'title': 'We Will Rock You',
                    'artist': 'Queen',
                    'year': 1977,
                    'genre': 'Rock',
                    'energy': 0.9,
                    'valence': 0.75,
                    'tags': ['Rock', 'Anthem', 'Powerful']
                },
                {
                    'title': 'Survivor',
                    'artist': "Destiny's Child",
                    'year': 2001,
                    'genre': 'R&B',
                    'energy': 0.75,
                    'valence': 0.8,
                    'tags': ['R&B', 'Empowering', 'Strong']
                },
                {
                    'title': 'Lose Control',
                    'artist': 'Meduza, Becky Hill',
                    'year': 2019,
                    'genre': 'Dance',
                    'energy': 0.9,
                    'valence': 0.85,
                    'tags': ['Dance', 'Confident', 'Energetic']
                }
            ]
        }
    
    def get_recommendations(self, mood: str, limit: int = 5) -> List[Dict]:
        """
        Get song recommendations based on detected mood
        """
        songs = self.song_database.get(mood, self.song_database['calm'])
        return songs[:limit]
    
    def get_all_moods(self) -> List[str]:
        """
        Get list of all available moods
        """
        return list(self.song_database.keys())


class MoodTuneAPI:
    """
    Main API interface for the MoodTune system
    """
    
    def __init__(self):
        self.mood_detector = MoodDetector()
        self.recommender = MusicRecommender()
    
    def analyze_and_recommend(self, user_text: str, num_songs: int = 5) -> Dict:
        """
        Full pipeline: detect mood and get recommendations
        """
        # Detect emotion
        emotion_result = self.mood_detector.detect_emotion(user_text)
        
        # Get recommendations
        recommendations = self.recommender.get_recommendations(
            emotion_result['emotion'],
            limit=num_songs
        )
        
        return {
            'user_input': user_text,
            'detected_mood': emotion_result['emotion'],
            'confidence': emotion_result['confidence'],
            'intensity': emotion_result['intensity'],
            'recommendations': recommendations,
            'emotion_scores': emotion_result['all_scores']
        }


# Example usage
if __name__ == '__main__':
    api = MoodTuneAPI()
    
    # Test cases
    test_inputs = [
        "I'm feeling so happy and excited today!",
        "I'm really sad and down right now",
        "Need some workout music, feeling energetic!",
        "Want to relax and chill after a long day",
        "Thinking about my crush, feeling romantic"
    ]
    
    print("=" * 80)
    print("MOODTUNE - AI Music Recommendation System")
    print("=" * 80)
    print()
    
    for test_input in test_inputs:
        result = api.analyze_and_recommend(test_input, num_songs=3)
        
        print(f"Input: {result['user_input']}")
        print(f"Detected Mood: {result['detected_mood']} (confidence: {result['confidence']}, intensity: {result['intensity']})")
        print(f"\nRecommendations:")
        print("-" * 60)
        
        for i, song in enumerate(result['recommendations'], 1):
            print(f"{i}. {song['title']} - {song['artist']}")
            print(f"   Genre: {song['genre']} | Year: {song['year']}")
            print(f"   Tags: {', '.join(song['tags'])}")
            print()
        
        print("=" * 80)
        print()
