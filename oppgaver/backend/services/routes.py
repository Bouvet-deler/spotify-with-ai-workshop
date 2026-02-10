from flask import Blueprint, request, jsonify
import os
import tempfile
import requests
from playlist_generator import CoverGenerator, DescriptionGenerator

from clients.blob_storage_client import BlobStorageClient
from io import BytesIO
routes = Blueprint('routes', __name__)

cover_generator = CoverGenerator()
description_generator = DescriptionGenerator()
blob_storage = BlobStorageClient()


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

# TODO: 1.3.2 'Implement the route for generating cover image for a playlist
@routes.route('/TODO', methods=['TODO'])
def generate_cover_image_for_playlist():
    playlist_id = request.args.get('playlist_id')
    user_id = request.args.get('userId')

    if not playlist_id:
        return jsonify({"error": "Missing 'playlist_id' parameter"}), 400
    
    if not user_id:
        return jsonify({"error": "Missing 'userId' parameter"}), 400

    try:
        tracks = get_playlist_tracks(playlist_id)
        track_names = [item['track']['name'] for item in tracks]
        
        # TODO 1.3.3: Find out witch class and method from you should use to generate the cover image, and call it here to get the DALL-E image URL
        dalle_image_url = "TODO"
        
        if dalle_image_url:
            # Upload the image to blob storage and get permanent URL
            blob_image_url = blob_storage.upload_image_from_url(dalle_image_url, user_id, playlist_id)
             # TODO 1.3.4: Return the blob_image_url in the response so it can be used in the frontend to display the image
            return "todo", 200
        else:
            return jsonify({"error": "Failed to generate cover image"}), 500
    except Exception as e:
        print(f"ERROR in generate_cover_image_for_playlist: {str(e)}")
        return jsonify({"error": f"Failed to process request: {str(e)}"}), 500


@routes.route('/generate-description', methods=['GET'])
def generate_description_for_playlist():
    playlist_id = request.args.get('playlist_id')
    user_id = request.args.get('userId')

    if not playlist_id:
        return jsonify({"error": "Missing 'playlist_id' parameter"}), 400
    
    if not user_id:
        return jsonify({"error": "Missing 'userId' parameter"}), 400

    try:
        tracks = get_playlist_tracks(playlist_id)
        track_names = [item['track']['name'] for item in tracks]
        description = description_generator.generate_description(track_names)
        
        if description:
            return jsonify({"description": description}), 200
        else:
            return jsonify({"error": "Failed to generate description"}), 500
    except Exception as e:
        print(f"ERROR in generate_description_for_playlist: {str(e)}")
        return jsonify({"error": f"Failed to process request: {str(e)}"}), 500


@routes.route('/cover-images', methods=['GET'])
def get_cover_images():
    user_id = request.args.get('userId')
    
    if not user_id:
        return jsonify({"error": "user_id query parameter is required"}), 400

    try:
        cover_images = blob_storage.list_user_covers(user_id)
        
        # Fetch all playlists to get names
        try:
            playlists = get_playlists()
            playlist_map = {p['id']: p['name'] for p in playlists}
            
            # Add playlist names to cover images
            for cover in cover_images:
                playlist_id = cover.get('playlistId')
                cover['playlistName'] = playlist_map.get(playlist_id, 'Unknown Playlist')
        except Exception as e:
            print(f"WARNING: Could not fetch playlist names: {str(e)}")
            # Continue without playlist names
            for cover in cover_images:
                cover['playlistName'] = 'Unknown Playlist'
        
        return jsonify(cover_images), 200
    except Exception as e:
        print(f"ERROR in get_cover_images: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request."}), 500


def fetch_web_api(endpoint, method, body=None):
    """Fetch from Spotify Web API
    Args:
        endpoint: API endpoint path
        method: HTTP method (GET, POST, etc.)
        body: Optional request body (dict)

    Returns:
        Response JSON as dict
    """
    token = os.getenv("SPOTIFY_ACCESS_TOKEN")
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
