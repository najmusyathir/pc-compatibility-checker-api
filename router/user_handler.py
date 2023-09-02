from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import logging
import json
import os 
import httpx
import base64

router = APIRouter(prefix="/input", tags=["Data Handler"])


class ItemDetails(BaseModel):
    title: str
    sku: str
    checkbox: bool
    img: str


@router.post("/show_inputs")
async def show_inputs(item_details_list: List[ItemDetails]):
    # Process input data
    # Load existing data from the JSON file
    try:
        # Use os.path.join to create the correct file path
        file_path = os.path.join(os.path.dirname(__file__), "data-set", "input_training_dataset.json")
        with open(file_path, "r") as f:
            user_data = json.load(f)
    except FileNotFoundError:
        user_data = []

    # Prepare the new data to be appended
    new_entries = []

    for item_details in item_details_list:
        new_entry = {
           "data": {
                "title": item_details.title,
                "sku": item_details.sku,
                "checkbox": item_details.checkbox,
                "img": item_details.img,
                "component_type": "",
            },
        }
        new_entries.append(new_entry)

    # Append the new data to the existing data
    user_data.extend(new_entries)
    
        # Read the existing data from the file
    with open(os.path.join("data-set", "input_training_dataset.json"), "r") as f:
        existing_data = f.read()

    # Remove the last character (which should be a "]")
    existing_data = existing_data[:-1]
    
    new_data = json.dumps(user_data, indent=2)
    cleaned_new_data = new_data[1:-1]

    # Add a comma, new data, and a closing square bracket
    updated_data = existing_data + "," +cleaned_new_data + "]"

    # Save the updated userDataSet back to the JSON file
    logging.debug("Saving updated userDataSet to JSON file")
    with open(os.path.join("data-set", "input_training_dataset.json"), "w") as f:
        f.write(updated_data)

    # You can also send a response back
    # return {"message": "Data received and appended successfully"}
    
        # Update the file in the GitHub repository
    repo_owner = "najmusyathir"  # Replace with your GitHub username or organization name
    repo_name = "pc-compatibility-checker-api"  # Replace with your GitHub repository name
    file_path_in_repo = "data-set/input_training_dataset.json"  # Specify the path to the file in your repository
    access_token = "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"  # Your personal access token

# Convert the JSON data to bytes and then Base64 encode it
    updated_data_bytes = updated_data.encode("utf-8")
    updated_data_base64 = base64.b64encode(updated_data_bytes).decode("utf-8")

    update_data = {
        "message": "Update input_training_dataset.json",
        "content": updated_data_base64
    }

    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path_in_repo}",
            json=update_data,
            headers={"Authorization": f"Bearer {access_token}"}
        )

        # Handle the response
        if response.status_code == 200:
            return {"message": "Data received, appended, and updated successfully on GitHub"}
        else:
            # Log the response from GitHub, including the response body
            logging.debug(f"GitHub response: {response.status_code} - {response.text}")
            raise HTTPException(status_code=500, detail=response.text)


