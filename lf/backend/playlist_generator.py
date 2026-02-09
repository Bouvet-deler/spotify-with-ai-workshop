from dataclasses import dataclass

from clients.cover_image_generator_client import CoverImageGeneratorClient
from clients.playlist_description_generator_client import PlaylistDescriptionGeneratorClient
import uuid

def image_cover_prompt(tracks: list[str]):
    # Create a safe prompt that doesn't directly include potentially problematic song titles
    return f"""
        Create an image, to be used as an album cover for a playlist, containing the track names: {tracks}.
        The album cover should visually represent the vibe of the tracks.
        Try to visulize one of the track names, but also capture the overall mood and energy of the playlist as a whole.
        The style should be vintage vinyl aesthetic.
        No text or logos, just a visually striking image that represents the essence of the playlist.
    """


def description_prompt(tracks: list[str]):
    return f"""
        Create a playlist description based on the following track names: {tracks}, without directly mentioning the track names in the description.
        There should be no more than two sentences in the description. 
        The description should capture the overall vibe and mood of the playlist, and entice listeners to give it a listen.
        It should be engaging, creative, and reflect the energy of the tracks included in the playlist.
    """


class CoverGenerator:
    def __init__(self):
        self.image_generation_client = CoverImageGeneratorClient()

    def generate_cover_image(self, track_names: list[str]):
        prompt = image_cover_prompt(track_names)
        imageUrl = self.image_generation_client.generate_image(prompt)
        return imageUrl
    


class DescriptionGenerator:
    def __init__(self):
        self.description_generation_client = PlaylistDescriptionGeneratorClient()
    
    def generate_description(self, track_names: list[str]):
        prompt = description_prompt(track_names)
        description = self.description_generation_client.generate_description(prompt)
        return description