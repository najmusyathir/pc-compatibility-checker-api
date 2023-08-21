from typing import Optional
from fastapi import APIRouter, Query, Path, Body
from pydantic import BaseModel

router = APIRouter(prefix="/cpu", tags=["CPUs"])


# mock_database / model


class cpuModel(BaseModel):
    modelID: str
    family: str
    core: int
    thread: int
    stock: Optional[bool]


@router.post("/new")
def declare_new_cpu(cpu: cpuModel):
    return cpu


@router.post("/new/{modelID}")
def declare_new_cpu(cpu: cpuModel, modelID: int):
    return {"id": modelID, "modelID": cpu}


@router.post("/new/{modelID}/family")
def set_family(
    cpu: cpuModel,
    modelID: int,
    family_id: str = Query(
        None,
        title="intel inc.",
        description="big company that make develop CPUs architechture",
        alias="familyID",
        deprecated=True,
    ),
    content: str = Body("Default Value here", max_length=10, regex="^[a-z\s]*$")
    # use Ellipsis / ... to set required
    # learn more about regex
):
    return {"id": modelID, "modelID": cpu, "familyID": family_id, "content": content}
