from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/input", tags=["Data Handler"])

class ItemDetails(BaseModel):
    title: str
    sku: str
    checkbox: bool
    img: str

@router.post("/show_inputs")
async def show_inputs(item_details_list: List[ItemDetails]):
    # Process input data
    
    # You can access item_details_list directly and perform any necessary operations
    
    # For example, you can print the received data
    for item_details in item_details_list:
        print("Received Item Details:", item_details)
    
    # You can also send a response back
    return {"message": "Data received successfully"}
