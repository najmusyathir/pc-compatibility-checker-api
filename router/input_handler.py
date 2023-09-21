from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from nlp.nlp_implementation import nlp_title_classification
from router.cpu_handler import cpu_family_identifier, get_cpu_socket
from router.mb_handler import mb_model_identifier, get_mb_socket

import hashlib
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

#Identify component scope
@router.post("/component_identifier")
async def component_identifier(item_details_list: List[ItemDetails]):
    print("\nReceive request from extension: Funtion is running: \n")

    new_entries = []
    new_entries2 = []
    cpu_socket = ""
    mb_socket = ""

    #Output Message
    compatible = "Item compatible"
    incompatible =  "Error: Item incompatible. Please check CPU Socket.\n"

    # Fill the component_type in input data
    for item_details in item_details_list:
        com_type = nlp_title_classification(item_details.title)
        new_entry = {
                "title": item_details.title,
                "sku": item_details.sku,
                "checkbox": item_details.checkbox,
                "img": item_details.img,
                "com_type": com_type,
            }
        new_entries.append(new_entry)

    # Find the component_model after fetch the component_type
    for entry in new_entries:
        com_type = entry['com_type']

        if com_type == "cpu":
            title = entry['title']
            cpu_model = cpu_family_identifier(title)
            
            cpu_socket = get_cpu_socket(cpu_model)

            new_entry = { "cpu":{
                    "title": entry['title'],  
                    "sku": entry['sku'],  
                    "checkbox": entry['checkbox'],  
                    "img": entry['img'],  
                    "com_type": entry['com_type'],  
                    "cpu_model": cpu_model,
                    "cpu_socket": cpu_socket
                }
            }
            new_entries2.append(new_entry)

        elif com_type == "mb":
            title = entry['title']
            mb_chipset = mb_model_identifier(title)
            mb_socket = get_mb_socket(mb_chipset)

            if mb_socket is None:
                mb_socket = "Socket not found"

            new_entry = { "mb":
                {
                    "title": entry['title'],  
                    "sku": entry['sku'],  
                    "checkbox": entry['checkbox'],  
                    "img": entry['img'],  
                    "com_type": entry['com_type'],  
                    "mb_chipset": mb_chipset,
                    "mb_socket": mb_socket
                }
            }
            new_entries2.append(new_entry)

    
    if cpu_socket.lower() == mb_socket.lower():
        print(compatible, "\nSocket type: ", cpu_socket.upper())
        output = compatible

    else:
         print(incompatible,"\nCPU Socket: ",cpu_socket, "\nMB Socket: ",mb_socket)
         output = incompatible

    output_entry = {
            "output": output,
            "cpu_socket": cpu_socket.upper(),
            "mb_socket": mb_socket.upper()
        }
    new_entries2.append(output_entry)

    

    return new_entries2

# // Funtions


# Show input and push data into github
# !!! In maintenance !!!
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
                "com_type": "",
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
    
    #Save the data only if it is successful >> code below
    # with open(os.path.join("data-set", "input_training_dataset.json"), "w") as f:
    #     f.write(updated_data)

    
    # Update the file in the GitHub repository
    repo_owner = "najmusyathir"  # Replace with your GitHub username or organization name
    repo_name = "pc-compatibility-checker-api"  # Replace with your GitHub repository name
    file_path_in_repo = "data-set/input_training_dataset.json"  # Specify the path to the file in your repository
    access_token = "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"  # Your personal access token

    # Convert the JSON data to bytes and then Base64 encode it
    updated_data_bytes = updated_data.encode("utf-8")
    updated_data_base64 = base64.b64encode(updated_data_bytes).decode("utf-8")
    
    # Fetch the latest commit SHA for the repository (replace 'main' with your branch name)
    async with httpx.AsyncClient() as client:
    # Fetch the latest commit SHA for the repository (replace 'main' with your branch name)
        latest_commit_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/main"
        latest_commit_response = await client.get(latest_commit_url, headers={"Authorization": f"Bearer {access_token}"})
        latest_commit_data = latest_commit_response.json()
        latest_commit_sha = latest_commit_data["sha"]

        # Fetch the content of the existing file
        existing_file_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path_in_repo}"
        existing_file_response = await client.get(existing_file_url, headers={"Authorization": f"Bearer {access_token}"})
        existing_file_data = existing_file_response.json()
        existing_file_sha = existing_file_data["sha"]

        # Check if the file content matches the SHA
        if existing_file_sha != latest_commit_sha:
            raise HTTPException(status_code=409, detail="File has been modified by someone else.")

        # If the file content matches, proceed with the update
        update_data = {
            "message": "Update input_training_dataset.json",
            "sha": existing_file_sha,  # Use the SHA from the existing file
            "content": updated_data_base64
        }

        response = await client.put(
            f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path_in_repo}",
            json=update_data,
            headers={"Authorization": f"Bearer {access_token}"}
        )

        # Handle the response
        if response.status_code == 200:
            with open(os.path.join("data-set", "input_training_dataset.json"), "w") as f:
                f.write(updated_data)
        else:
            # Log the response from GitHub, including the response body
            logging.debug(f"GitHub response: {response.status_code} - {response.text}")
            raise HTTPException(status_code=500, detail=response.text)


