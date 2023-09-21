from fastapi import APIRouter
import json
import re

router = APIRouter(prefix="/mb", tags=["Motherboards"])

#Load mb_dataset
with open("data-set/mb_dataset.json", "r") as file:
    mb_data = json.load(file)

@router.get("/all")  
def get_all():
    # description
    """
    Simulates rethriving all **Motherboards** in database
    - Brand
    - model
    - socket
    - formX
    """
    with open("data-set/mbDataSet.json", "r") as file:
        mb_data = json.load(file)
        mb_names = [mb["Name"] for mb in mb_data]

    return {"mb_names": mb_names}

@router.get("/{mb_chipset}")
def get_mb_socket(mb_chipset: str):
    mb_pattern = rf'.*{re.escape(mb_chipset)}.*'

    for mb in mb_data:
        if re.search(mb_pattern, mb["name"], re.IGNORECASE):
            return mb["socket"]

    return "Socket not found"

        


@router.post("/model/{title}")
def mb_model_identifier(title):
    model = extract_mb_chipset(title)
    return model



# Regular functions 
def extract_mb_chipset(title):
        # Regular expression to match AMD mb model patterns
        mb_pattern = r'\b[a-zA-Z]?\d{3,4}[a-zA-Z]?[3]?[a-zA-Z]?\b'
    
        # Extract AMD mb models from the title
        mb_models = re.findall(mb_pattern, title, re.IGNORECASE)
        mb_models = [''.join(filter(None, match)) for match in mb_models]
        if not mb_models:
                return "Model unidentified"
        else:
                return mb_models[0]

