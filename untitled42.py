# -*- coding: utf-8 -*-
"""Untitled42.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YHJPkXtFcXZiQ6qaE-Pv7oiH8zWIQxHE
"""

!pip install Spotipy

import requests
import base64

#Spotify API credentials
client_id = '4ea024aaf7bb491487899cac62614372'
client_secret = 'd36476a069ae42c387c73c73b3aeb6b8'

# client_id and client_secret in base64
client_credentials = f"{client_id}:{client_secret}"
base64_credentials = base64.b64encode(client_credentials.encode()).decode()

# Requesn Spotify access token
token_url = 'https://accounts.spotify.com/api/token'
token_data = {
    'grant_type': 'client_credentials'
}
token_headers = {
    'Authorization': f'Basic {base64_credentials}'
}

token_response = requests.post(token_url, data=token_data, headers=token_headers)

if token_response.status_code == 200:
    access_token = token_response.json().get('access_token')

    # Emotion detection API URL and key
    emotion_detection_api_url = 'https://api.apilayer.com/text_to_emotion'
    emotion_detection_api_key = 'EypJex9jUpJCYyOQ9ffnjhW3C1m3d5QL'

    user_text = input("How are you feeling today?: ")  # Prompt

    headers = {
        'apikey': emotion_detection_api_key,
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(emotion_detection_api_url, headers=headers, data=user_text.encode("utf-8"))

    if response.status_code == 200:
        detected_emotions = response.json()

        emotion_threshold = 0.5

        mood_mapping = {
            'Happy': 'happy',
            'Sad': 'sad',
            'Angry': 'jazz',
            'Surprise': 'electronic',
            'Fear': 'ambient',
        }

        max_mood = None
        for emotion, score in detected_emotions.items():
            if score >= emotion_threshold:
                mapped_mood = mood_mapping.get(emotion)
                if mapped_mood:
                    max_mood = mapped_mood
                    break

        if max_mood:
            # You can make a request to the Spotify Web API here to get music recommendations based on the 'max_mood'
            # Use the 'access_token' obtained earlier
            # Construct the request with 'max_mood' as a seed genre
            # Example:
            recommendations_url = 'https://api.spotify.com/v1/recommendations'
            recommendations_params = {
                'limit': 10,
                'seed_genres': max_mood
            }
            recommendations_headers = {
                'Authorization': f'Bearer {access_token}'
            }
            recommendations_response = requests.get(recommendations_url, params=recommendations_params, headers=recommendations_headers)

            if recommendations_response.status_code == 200:
                recommended_tracks = recommendations_response.json().get('tracks')
                print("Recommended Tracks:")
                for track in recommended_tracks:
                    artists = ', '.join([artist['name'] for artist in track['artists']])
                    print(f"{track['name']} by {artists}")
            else:
                print("Error fetching music recommendations from Spotify.")
        else:
            print("No specific emotion or mood detected; using default mood or no recommendations available.")
    else:
        print("Emotion detection API error")
else:
    print("Error obtaining Spotify access token")