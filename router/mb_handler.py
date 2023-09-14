from fastapi import APIRouter, status, Response
from enum import Enum
from typing import Optional
import json

router = APIRouter(prefix="/mb", tags=["Motherboards"])


@router.get(
    "/all",
)  # Implement the sections
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


# get function
@router.get("/{id}")
def get_id(id: int):
    return {"message": f"the mb was: {id}"}


# predefine values
class MbFamily(str, Enum):
    intel = "intel"
    AMD = "amd"


@router.get("/family/{family}")
def get_mb_family(family: MbFamily):
    return {"message": f"Motherboard family: {family.value}"}


@router.get("/{family}/{model}", tags=["Motherboard Model"])
def get_mb_name(family: MbFamily, model):
    return {"message": f"the mb model of {family.value} is {model}"}


# query values include some functions
@router.get(
    "/core/{mbModel}", status_code=status.HTTP_404_NOT_FOUND, tags=["Motherboard Model"]
)
def get_core_counts(
    mbModel="",
    core=2,
    threads: Optional[int] = None,
    avaibility: bool = False,
    response=Response,
):
    if mbModel == "":
        return {"message": "Motherboard model required"}
    else:
        if threads is None:
            if avaibility is True:
                return {"message": f"Core count of {mbModel} is {int(core)} of core/s"}
            else:
                return {"message": "Item unavailable"}
        else:
            if avaibility is True:
                return {
                    "message": f"Core count of {mbModel} is {int(core)} of core/s and {int(threads)} of threads"
                }
            else:
                return {"message": "Items unavailable"}