from fastapi import FastAPI, APIRouter, HTTPException, Request, Query, Depends
from fastapi.templating import Jinja2Templates

from typing import Optional, Any
from pathlib import Path
from sqlalchemy.orm import Session

from app.schemas.recipe import RecipeSearchResults, Recipe, RecipeCreate
from app import deps
from app import crud


ROOT = Path(__file__).resolve().parent.parent
BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))


app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()


@api_router.get("/", status_code=200)
def root(
        request: Request,
        db: Session = Depends(deps.get_db),
    ) -> dict:
    """Root

    Returns:
        "msg": "Hello!!"
    """
    recipes = crud.recipe.get_multi(db=db, limit=10)
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "recipes": recipes}
    )


@api_router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe)
def fetch_recipe(
        *,
        recipe_id: int,
        db: Session = Depends(deps.get_db),
    ) -> Any:
    """

    Args:
        recipe_id (int): recipe_id

    Returns:
        result: {results}
    """
    result = crud.recipeget(db=db, id=recipe_id)
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Recipe with ID {recipe_id} not found"
        )
         
    return result


@api_router.get("/search/", status_code=200, response_model=RecipeSearchResults)
def search_recipes(
        *,
        keyword: Optional[str] = Query(None, min_length=3, example="chicken"),
        max_results: Optional[int] = 10,
        db: Session = Depends(deps.get_db)
    ) -> dict:
    """

    Args:
        keyword (Optional[str], optional): search keyword. Defaults to None.
        max_results (Optional[int], optional): max_result. Defaults to 10.

    Returns:
        dict: recipes
    """
    recipes = crud.recipe.get_multi(db=db, limit=max_results)
    if not keyword:
        return {"result": recipes}

    results = filter(lambda recipe: keyword.lower() in recipe.label.lower(), recipes)
    return {"result": list(results)[:max_results]}


@api_router.post("/recipe/", status_code=201, response_model=Recipe)
def create_recipe(
        *,
        recipe_in: RecipeCreate,
        db: Session = Depends(deps.get_db)
    ) -> dict:
    """

    Args:
        recipe_in (RecipeCreate): recipe - in memory only

    Returns:
        dict: recipe model
    """
    recipe = crud.recipe.create(db=db, obj_in=recipe_in)
    
    return recipe


@api_router.put("/recipe", status_code=200)
def update_recipe(
        *,
        recipe_update: Recipe,
        db: Session = Depends(deps.get_db)
    ) -> dict:
    recipe = crud.recipe.update(db=db, db_obj=Recipe, obj_in=recipe_update)
    
    
    return recipe


@api_router.delete("/recipe/{recipe_id}/", status_code=200)
def remove_recipe(
        *,
        recipe_id: int,
        db: Session = Depends(deps.get_db)
    ) -> int:
    crud.recipe.remove(db=db, id=recipe_id)
    
    return recipe_id


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
