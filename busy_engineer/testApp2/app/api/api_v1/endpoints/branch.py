import asyncio
from typing import Any, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.clients.reddit import RedditClient
from app.schemas.branch import (
    Branch,
    BranchCreate,
    BranchUpdate,
    BranchSearchResults,
)
from app.models.user import User

router = APIRouter()
BRANCH_SUBREDDITS = ["branch", "easybranch", "TopSecretbranch"]


@router.get("/{branch_id}", status_code=200, response_model=Branch)
def fetch_branch(
    *,
    branch_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    
    result = crud.branch.get(db=db, id=branch_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Branch with ID {branch_id} not found"
        )

    return result


@router.get("/search/", status_code=200, response_model=BranchSearchResults)
def search_branches(
    *,
    keyword: str = Query(None, min_length=1, example="강남"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:

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
    """
    Create a new branch in the database.
    """
    if branch_in.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail=f"You can only submit branches as yourself"
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


# async def get_reddit_top_async(subreddit: str) -> list:
#     async with httpx.AsyncClient() as client:
#         response = await client.get(
#             f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limit=5",
#             headers={"User-agent": "recipe bot 0.1"},
#         )

#     subreddit_recipes = response.json()
#     subreddit_data = []
#     for entry in subreddit_recipes["data"]["children"]:
#         score = entry["data"]["score"]
#         title = entry["data"]["title"]
#         link = entry["data"]["url"]
#         subreddit_data.append(f"{str(score)}: {title} ({link})")
#     return subreddit_data


# @router.get("/ideas/async")
# async def fetch_ideas_async(
#     user: User = Depends(deps.get_current_active_superuser),
# ) -> dict:
#     results = await asyncio.gather(
#         *[get_reddit_top_async(subreddit=subreddit) for subreddit in RECIPE_SUBREDDITS]
#     )
#     return dict(zip(RECIPE_SUBREDDITS, results))


# @router.get("/ideas/")
# def fetch_ideas(reddit_client: RedditClient = Depends(deps.get_reddit_client)) -> dict:
#     return {
#         key: reddit_client.get_reddit_top(subreddit=key) for key in RECIPE_SUBREDDITS
#     }
