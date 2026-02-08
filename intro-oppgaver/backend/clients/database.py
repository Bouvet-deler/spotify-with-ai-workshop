import os
from azure.data.tables import TableServiceClient
from azure.core.credentials import AzureNamedKeyCredential
from typing import List


class Database:
    def __init__(self):
        api_key = os.getenv("AZURE_TABLE_API_KEY")
        credential = AzureNamedKeyCredential("spotifyworkshop", api_key)
        endpoint = os.getenv("AZURE_TABLE_API_ENDPOINT", "https://spotifyworkshop.table.core.windows.net")
        service = TableServiceClient(endpoint=endpoint, credential=credential)
        self.client = service.get_table_client(table_name="spotify-covers")


    def save_playlist_cover(self, user_id: str, playlist_id: str, image_url: str):
        """Save the generated cover image URL to the database with user_id"""
        if not user_id:
            raise Exception("save_playlist_cover failed: user_id is null")
        if not playlist_id:
            raise Exception("save_playlist_cover failed: playlist_id is null")
        if not image_url:
            raise Exception("save_playlist_cover failed: image_url is null")

        entity = {
            "PartitionKey": user_id,
            "RowKey": playlist_id,
            "playlistId": playlist_id,
            "imageUrl": image_url
        }

        self.client.upsert_entity(entity)
        print(f"Saved cover image URL {image_url} for playlist {playlist_id} and user {user_id} to database")

    def save_playlist_description(self, user_id: str, playlist_id: str, description: str):
        """Save the generated playlist description to the database with user_id"""
        if not user_id:
            raise Exception("save_playlist_description failed: user_id is null")
        if not playlist_id:
            raise Exception("save_playlist_description failed: playlist_id is null")
        if not description:
            raise Exception("save_playlist_description failed: description is null")

        # Merge with existing entity if it exists
        try:
            existing_entity = self.client.get_entity(partition_key=user_id, row_key=playlist_id)
            existing_entity["description"] = description
            self.client.update_entity(existing_entity)
        except:
            entity = {
                "PartitionKey": user_id,
                "RowKey": playlist_id,
                "playlistId": playlist_id,
                "description": description
            }
            self.client.upsert_entity(entity)
        
        print(f"Saved description for playlist {playlist_id} and user {user_id} to database")

    def get_cover_images(self, user_id: str) -> List[dict]:
        """Get all cover images for a specific user"""
        user_id_filter = f"PartitionKey eq '{user_id}'"

        try:
            result = self.client.query_entities(user_id_filter)
            cover_images = []
            for entity in result:
                if "imageUrl" in entity:
                    cover_images.append({
                        "id": entity["RowKey"],
                        "playlistId": entity.get("playlistId", entity["RowKey"]),
                        "imageUrl": entity["imageUrl"],
                        "description": entity.get("description", "")
                    })
            return cover_images
        except Exception as e:
            print(f"Error fetching cover images: {str(e)}")
            return []