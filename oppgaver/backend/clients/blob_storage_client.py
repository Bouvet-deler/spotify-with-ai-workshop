import os
import uuid
from io import BytesIO
from azure.storage.blob import BlobServiceClient, ContentSettings
import requests


class BlobStorageClient:
    def __init__(self):
        connection_string = os.getenv("AZURE_BLOB_STORAGE_CONNECTION_STRING")
        self.container_name = os.getenv("AZURE_BLOB_STORAGE_CONTAINER_NAME", "spotify-workshop")
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.container_name)
        
        # Ensure container exists
        try:
            self.container_client.get_container_properties()
            print(f"Container '{self.container_name}' exists and is accessible")
        except Exception:
            print(f"Container not found, creating container: {self.container_name}")
            from azure.storage.blob import PublicAccess
            self.container_client.create_container(public_access=PublicAccess.Blob)

    def upload_image_from_url(self, image_url: str, user_id: str, playlist_id: str) -> str:
        """
        Downloads an image from a URL and uploads it to Azure Blob Storage
        
        Args:
            image_url: The URL of the image to download
            user_id: User ID for organizing blobs
            playlist_id: Playlist ID for unique identification
            
        Returns:
            The public URL of the uploaded blob
        """
        try:
            # Download the image from the URL
            print(f"Downloading image from: {image_url}")
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            image_data = BytesIO(response.content)
            
            # Create a unique blob name
            blob_name = f"covers/{user_id}/{playlist_id}.png"
            
            # Upload to blob storage

            # TODO: 2.1 - Get the blob client 
            blob_client = "TODO"
            
            # Set content type for proper image display
            content_settings = ContentSettings(content_type='image/png')
            
            print(f"Uploading image to blob storage: {blob_name}")

            # TODO: 2.2 - Upload the image data to blob storage
            blob_client.TODO
            
            # TODO: 2.3 Return the public URL
            blob_url = TODO
            print(f"Successfully uploaded image to: {blob_url}")
            
            # Verify the blob is accessible
            print(f"Blob properties: container={self.container_name}, blob={blob_name}")
            
            return blob_url
            
        except requests.RequestException as e:
            print(f"ERROR downloading image: {str(e)}")
            raise Exception(f"Failed to download image from URL: {str(e)}")
        except Exception as e:
            print(f"ERROR uploading to blob storage: {str(e)}")
            raise Exception(f"Failed to upload image to blob storage: {str(e)}")

    def list_user_covers(self, user_id: str) -> list:
        """
        Lists all cover images for a specific user
        
        Args:
            user_id: User ID
            
        Returns:
            List of dictionaries containing blob information
        """
        try:
            prefix = f"covers/{user_id}/"
            # TODO : 3.2 - List blobs with the specified prefix to get all covers for the user
            blob_list = TODO
            
            cover_images = []
            for blob in blob_list:
                # Extract playlist_id from blob name (covers/user_id/playlist_id.png)
                playlist_id = blob.name.split('/')[-1].replace('.png', '')
                # TODO : 3.3 - Get the blob client for the current blob to access its URL and properties
                blob_client = TODO
                
                # TODO : 3.4 Fyll inn 
                cover_images.append({
                    "id": TODO,
                    "playlistId": TODO,
                    "imageUrl": TODO,
                    "createdAt": TODO if blob.creation_time else None
                })
            
            print(f"Found {len(cover_images)} covers for user {user_id}")
            return cover_images
        except Exception as e:
            print(f"ERROR listing blobs: {str(e)}")
            return []

    def delete_blob(self, user_id: str, playlist_id: str) -> bool:
        """
        Deletes a blob from storage
        
        Args:
            user_id: User ID
            playlist_id: Playlist ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            blob_name = f"covers/{user_id}/{playlist_id}.png"
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            blob_client.delete_blob()
            print(f"Successfully deleted blob: {blob_name}")
            return True
        except Exception as e:
            print(f"ERROR deleting blob: {str(e)}")
            return False
