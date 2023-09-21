from fastapi import APIRouter, status, Response
from enum import Enum
from typing import Optional
import json
import re

router = APIRouter(prefix="/cpu", tags=["CPUs"])

# Load cpu_dataset
with open("data-set/cpu_dataset.json", "r") as file:
    cpu_data = json.load(file)

 # Get All CPU List
@router.get(
    "/all",
) 
def get_all():
    # description
    """
    Simulates rethriving all **CPUs** in database
    - family
    - model
    - core counts
    - tread counts
    """
    cpu_details = [
        {"name": cpu["name"], "socket": cpu["socket"]} for cpu in cpu_data
    ]
    return {"cpu_details": cpu_details}



def get_cpu_socket(cpu_model):
    cpu_model_words = cpu_model.split()
    
    for cpu in cpu_data:
        name_lower = cpu["name"].lower()
        if all(word.lower() in name_lower for word in cpu_model_words):
            return f"{cpu['socket']}"

    return "Socket not found"
    

@router.get("amd/{cpu_model}")
def get_amd_socket(cpu_model):
    cpu_model_words = cpu_model.split()  # Split the input into individual words

    for cpu in cpu_data:
        name_words = cpu["name"].lower().split()
        if all(word.lower() in name_words for word in cpu_model_words):
            output = cpu["socket"]+": " +cpu["name"]
            return output

    return "Socket not found"


# Regular Function

def cpu_family_identifier(title):

    if  "intel"in title.lower() and "amd" in title.lower():
        return "Error: Family identifier Error"

    elif "intel" in title.lower():
        model = extract_intel_models(title)
        return model
    
    elif "amd" in title.lower():
        model = extract_amd_models(title)
        return model

    else:
        model = extract_intel_models(title)
        if model is None:
            model = extract_amd_models(title)
            if model is None:
                return "Error: CPU Family not found"
            else:
                return "AMD "+model

        return "intel "+model

def extract_intel_models(title):
        
    family = re.findall(r'\b(celeron|pentium|xeon|[iI][3579])\b', title, re.IGNORECASE)

    # Extract AMD CPU models from the title
    intel_models = re.findall(r'\b\s?[- ]?([a-zA-Z]?\d{4,5}[a-zA-Z]?[a-zA-Z]?)\b', title, re.IGNORECASE)

    if not intel_models:
        return "Intel model unidentified"
    else:
        if intel_models:
            return f"{family[0]} {' '.join(intel_models)}"
        else:
            return ', '.join(intel_models)


def extract_amd_models(title):
    # Regular expression to match AMD CPU model patterns
    family = re.findall(r'\b(Athlon|Ryzen|Threadripper|Epyc)\b', title, re.IGNORECASE)

    # Extract AMD CPU models from the title
    amd_models = re.findall(r'\b\d{3,4}[a-zA-Z]?[3]?[a-zA-Z]?\b', title, re.IGNORECASE)

    if not amd_models:
        return "AMD model unidentified"
    else:
        if family:
            return f"AMD {family[0]} {' '.join(amd_models)}"
        else:
            return "AMD " + ', '.join(amd_models)


# Not using yet or not using at all

# query values include some functions
@router.get(
    "/core/{cpuModel}", status_code=status.HTTP_404_NOT_FOUND, tags=["CPU Model"]
)
def get_core_counts(
    cpuModel="",
    core=2,
    threads: Optional[int] = None,
    avaibility: bool = False,
    response=Response,
):
    if cpuModel == "":
        response.status_code = status.HTTP_400_BAD_REQUEST  # type: ignore
        return {"message": "CPU model required"}
    else:
        response.status_code = status.HTTP_200_OK  # type: ignore
        if threads is None:
            if avaibility is True:
                return {"message": f"Core count of {cpuModel} is {int(core)} of core/s"}
            else:
                return {"message": "Item unavailable"}
        else:
            if avaibility is True:
                return {
                    "message": f"Core count of {cpuModel} is {int(core)} of core/s and {int(threads)} of threads"
                }
            else:
                return {"message": "Items unavailable"}
    



    