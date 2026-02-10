from dataclasses import dataclass

from clients.cover_image_generator_client import CoverImageGeneratorClient
from clients.playlist_description_generator_client import PlaylistDescriptionGeneratorClient
import uuid

def image_cover_prompt(tracks: list[str]):
    # Create a safe prompt that doesn't directly include potentially problematic song titles
    return f"""
        Create a boring and sad image for an album cover. The image should be dull and melancholic.
        Use muted gray tones and depressing imagery. Make it uninspiring and monotonous.
        The style should be plain and forgettable. Create something that lacks energy or excitement.
    """


def description_prompt(tracks: list[str]):
    return f"""
        Create a boring and uninspiring playlist description. Make it dull and monotonous.
        Use generic phrases and avoid any creativity or excitement. The description should be forgettable and bland.
        Make it sound tedious and unappealing, with no energy or enthusiasm.
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