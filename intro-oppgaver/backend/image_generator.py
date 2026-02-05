from dataclasses import dataclass

from clients.cover_image_generator_client import CoverImageGeneratorClient
import uuid

def image_cover_prompt(tracks: list[str]):
    # Create a safe prompt that doesn't directly include potentially problematic song titles
    num_tracks = len(tracks)
    return f"""
        Create an image, to be used as an album cover for a playlist, containing the track names: {tracks}.
        The album cover should visually represent the vibe of the tracks.
        Try to visulize one of the track names, but also capture the overall mood and energy of the playlist as a whole.
        The style should be vintage vinyl aesthetic.
        No text or logos, just a visually striking image that represents the essence of the playlist.

    """


class CoverGenerator:
    def __init__(self):
        self.image_generation_client = CoverImageGeneratorClient()

    def generate_cover_image(self, track_names: list[str]):
        prompt = image_cover_prompt(track_names)
        imageUrl = self.image_generation_client.generate_image(prompt)
        return imageUrl
    