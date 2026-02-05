import openai
from openai import AzureOpenAI
import os

class CoverImageGeneratorClient:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-01",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment="dall-e-3"
        )

    def generate_image(self, prompt: str) -> str:
        try:
            print(f"Generating image with prompt: {prompt[:100]}...")  # Debug log
            response = self.client.images.generate(
                model="dall-e-3",  # TODO: oppgave 2.1.2 Sett riktig modell her
                prompt=prompt,
                size="1024x1024",  # TODO: oppgave 2.1.3 Sett riktig størrelse her
                quality="standard",
                n=1,
            )

            image_url = response.data[0].url
            print(f"Successfully generated image: {image_url}")  # Debug log
            return image_url

        # catch exceptions
        except openai.APIConnectionError as e:
            print("ERROR: The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
            return None
        except openai.RateLimitError as e:
            print("ERROR: A 429 status code was received; we should back off a bit.")
            return None
        except openai.APIStatusError as e:
            print("ERROR: Another non-200-range status code was received")
            print(f"Status code: {e.status_code}")
            print(f"Message: {e.message}")
            return None
        except Exception as e:
            print(f"ERROR: Unexpected exception occurred: {type(e).__name__}: {str(e)}")
            return None
