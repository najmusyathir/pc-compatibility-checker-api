from fastapi import APIRouter, status, Response
from enum import Enum
from typing import Optional
import json

router = APIRouter(prefix="/cpu", tags=["CPUs"])


@router.get(
    "/all",
)  # Implement the sections
def get_all():
    # description
    """
    Simulates rethriving all **CPUs** in database
    - family
    - model
    - core counts
    - tread counts
    """
    with open("data-set/cpu_dataset.json", "r") as file:
        cpu_data = json.load(file)
        cpu_details = [
            {"name": cpu["name"], "socket": cpu["socket"]} for cpu in cpu_data
        ]

        return {"cpu_details": cpu_details}


# get function
@router.get("/{id}")
def get_id(id: int):
    return {"message": f"the cpu was: {id}"}


# predefine values
class CpuFamily(str, Enum):
    intel = "intel"
    AMD = "amd"


@router.get("/family/{family}")
def get_cpu_family(family: CpuFamily):
    return {"message": f"CPU family: {family.value}"}


@router.get("/{family}/{model}", tags=["CPU Model"])
def get_cpu_name(family: CpuFamily, model):
    return {"message": f"the cpu model of {family.value} is {model}"}


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


"""
@router.post("/new")
def declare_new_cpu(cpu: cpuModel):
    return cpu


@router.post("/new/{modelID}")
def declare_new_cpu(cpu: cpuModel, modelID: int):
    return {"id": modelID, "modelID": cpu}


@router.post("/new/{modelID}/family")
def set_family(
    cpu: cpuModel,
    modelID: str,
    family_id: str = Query(
        None,
        title="intel inc.",
        description="big company that make develop CPUs architechture",
        alias="familyID",
        deprecated=True,
    ),
    content: str = Body("Max 1000 words here", max_length=100, regex="^[a-z\\s]*$")
    # use Ellipsis / ... to set required
    # learn more about regex
):
    return {"id": modelID, "modelID": cpu, "familyID": family_id, "content": content}"""
