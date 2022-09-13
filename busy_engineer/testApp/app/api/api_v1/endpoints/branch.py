import asyncio
from typing import Any, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.branch import (
    Branch,
    BranchCreate,
    BranchSearchResults,
    BranchUpdate,
)
from app.models.user import User

router = APIRouter()


@router.get("/{branch_id}", status_code=200, response_model=Branch)
def fetch_branch(
    *,
    branch_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    result = crud.branch.get(db=db, id=branch_id)
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Branch with ID {branch_id} not found"
        )
    
    return result


@router.get("/search/", status_code=200, response_model=BranchSearchResults)
def search_branch(
    *,
    keyword: str = Query(None, min_length=3, example="kangnam"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
)-> dict:
    branches = crud.branch.get_multi(db=db, limit=max_results)
    results = filter(lambda branch: keyword.lower() in branch.name.lower(), branches)
    
    return {"results": list(results)}


@router.post("/", status_code=201, response_model=Branch)
def create_branch(
    *,
    branch_in: BranchCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    if branch_in.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail=f"You can only submit branch as yourself"
        )
    branch = crud.branch.create(db=db, obj_in=branch_in)
    
    return branch


@router.put("/", status_code=201, response_model=Branch)
def update_branch(
    *,
    branch_in: BranchUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    branch = crud.branch.get(db, id=branch_in.id)
    if not branch:
        raise HTTPException(
            status_code=400, detail=f"Branch with ID: {branch_in.id} not found."
        )
    if branch.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail=f"You can only update your branches."
        )

    updated_branch = crud.branch.update(db=db, db_obj=branch, obj_in=branch_in)
    db.commit()
    return updated_branch


@router.delete("/{branch_id}")
async def remove_branch(
    *,
    branch_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Remove a single branch by ID
    """
    crud.branch.remove(db=db, id=branch_id)
    return branch_id