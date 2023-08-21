from fastapi import APIRouter, status, Response
from enum import Enum
from typing import Optional

router = APIRouter(
    prefix ='/cpu',
    tags=['CPUs']
)

@router.get('/all', ) # Implement the sections
def get_all():
    #description
    """ 
    Simulates rethriving all **CPUs** in database
    - family
    - model
    - core counts
    - tread counts
    """
    return {'message': 'This calling all cpu model'}


# get function
@router.get('/{id}')
def get_id(id: int):
    return {'message': f'the cpu was: {id}'}


# predefine values
class CpuFamily(str, Enum):
    intel = 'intel'
    AMD = 'amd'


@router.get('/family/{family}')
def get_cpu_family(family: CpuFamily):
    return {'message': f'CPU family: {family.value}'}


@router.get('/{family}/{model}', tags=['CPU Model'])
def get_cpu_name(family: CpuFamily, model):
    return {'message': f'the cpu model of {family.value} is {model}'}


# query values include some functions
@router.get('/core/{cpuModel}', status_code=status.HTTP_404_NOT_FOUND, tags=['CPU Model'])
def get_core_counts(
    cpuModel='',
    core=2,
    threads: Optional[int] = None,
    avaibility: bool = False,
    response=Response,
):
    if cpuModel == '':
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': 'CPU model required'}
    else:
        response.status_code = status.HTTP_200_OK
        if threads is None:
            if avaibility is True:
                return {'message': f'Core count of {cpuModel} is {int(core)} of core/s'}
            else:
                return {'message': 'Item unavailable'}
        else:
            if avaibility is True:
                return {
                    'message': f'Core count of {cpuModel} is {int(core)} of core/s and {int(threads)} of threads'
                }
            else:
                return {'message': 'Items unavailable'}
