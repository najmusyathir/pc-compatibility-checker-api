from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import json
import os 

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
    with open(os.path.join("data-set", "userDataSet.json"), "r") as f:
        existing_data = f.read()

    # Remove the last character (which should be a "]")
    existing_data = existing_data[:-1]
    
    new_data = json.dumps(user_data, indent=2)
    cleaned_new_data = new_data[1:-1]

    # Add a comma, new data, and a closing square bracket
    updated_data = existing_data + "," +cleaned_new_data + "]"

    # Save the updated userDataSet back to the JSON file
    with open(os.path.join("data-set", "userDataSet.json"), "w") as f:
        f.write(updated_data)

    # You can also send a response back
    # return {"message": "Data received and appended successfully"}

