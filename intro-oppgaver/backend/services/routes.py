from flask import Blueprint, request, jsonify
import os
import tempfile
import requests
from image_generator import CoverGenerator
# from werkzeug.datastructures import FileStorage

# from clients.database import Database
from io import BytesIO
routes = Blueprint('routes', __name__)

cover_generator = CoverGenerator()

@routes.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "API is working"}), 200
            


@routes.route('/get-playlist', methods=['GET'])
def get_playlist():
    playlists = get_playlists()
    play_list = []
    for playlist in playlists:
        print(f"Playlist: {playlist['name']} (ID: {playlist['id']})")
        play_list.append({
            'name': playlist['name'],
            'id': playlist['id']
        })
    return jsonify(play_list), 200


@routes.route('/get-tracks', methods=['GET'])
def get_tracks_of_playlist():
    playlist_id = request.args.get('playlist_id')
    if not playlist_id:
        return jsonify({"error": "Missing 'playlist_id' parameter"}), 400

    tracks = get_playlist_tracks(playlist_id)
    for item in tracks:
        track = item['track']
        print(f"Track: {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")
    return jsonify(tracks), 200


@routes.route('/generate-cover', methods=['GET'])
def generate_cover_image_for_playlist():
    playlist_id = request.args.get('playlist_id')

    if not playlist_id:
        return jsonify({"error": "Missing 'playlist_id' parameter"}), 400

    try:
        tracks = get_playlist_tracks(playlist_id)
        track_names = [item['track']['name'] for item in tracks]
        
        # Use the CoverGenerator to create the cover image
        cover_image_url = cover_generator.generate_cover_image(track_names)
        
        if cover_image_url:
            return jsonify({"image_url": cover_image_url}), 200
        else:
            return jsonify({"error": "Failed to generate cover image"}), 500
    except Exception as e:
        print(f"ERROR in generate_cover_image_for_playlist: {str(e)}")
        return jsonify({"error": f"Failed to process request: {str(e)}"}), 500

# curl "http://127.0.0.1:5000/get-tracks?playlist_id=0Ux3Z2CwlFZMPDVWvweyBZ"
# curl "http://127.0.0.1:5000/generate-cover?playlist_id=0Ux3Z2CwlFZMPDVWvweyBZ"



def fetch_web_api(endpoint, method, body=None):
    """Fetch from Spotify Web API
    Args:
        endpoint: API endpoint path
        method: HTTP method (GET, POST, etc.)
        body: Optional request body (dict)

    Returns:
        Response JSON as dict
    """
    token = os.getenv("SPOTIFY_ACCESS_TOKEN", token)
    res = requests.request(
        method,
        f'https://api.spotify.com/{endpoint}',
        headers={'Authorization': f'Bearer {token}'},
        json=body
    )
    
    if res.status_code != 200:
        print(f"Spotify API Error: {res.status_code} - {res.text}")
        raise Exception(f"Spotify API returned {res.status_code}: {res.text}")
    
    return res.json()


def get_playlists():
    """Get user's playlists"""
    return fetch_web_api(
        'v1/me/playlists',
        'GET'
    )['items']



def get_playlist_tracks(playlist_id):
    """Get tracks in a playlist
    Args:
        playlist_id: Spotify playlist ID

    Returns:
        List of tracks in the playlist
    """
    return fetch_web_api(
        f'v1/playlists/{playlist_id}/tracks',
        'GET'
    )['items']



def send_tracks_to_ai(tracks):
    """Send track data to AI service
    Args:
        tracks: List of track data

    Returns:
        AI service response
    """
    ai_service_url = 'http://ai-service.example.com/process-tracks'
    response = requests.post(ai_service_url, json={'tracks': tracks})
    return response.json()
