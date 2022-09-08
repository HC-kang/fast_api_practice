from fastapi import FastAPI, APIRouter
from typing import Optional


RECIPES = [
    {
        "id": 1,
        "label": "Chicken Vesuvio",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio-recipe.html",
    },
    {
        "id": 2,
        "label": "Chicken Paprikash",
        "source": "No Recipes",
        "url": "http://norecipes.com/recipe/chicken-paprikash/",
    },
    {
        "id": 3,
        "label": "Cauliflower and Tofu Curry Recipe",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/02/cauliflower-and-tofu-curry-recipe.html",
    },
]


app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()


@api_router.get("/", status_code=200)
def root() -> dict:
    """Root

    Returns:
        "msg": "Hello!!"
    """
    return {"msg": "Hello!!"}


@api_router.get("/recipe/{recipe_id}", status_code=200)
def fetch_recipe(*, recipe_id: int) -> dict:
    """

    Args:
        recipe_id (int): recipe_id

    Returns:
        result: {results}
    """
    print(recipe_id)
    print(type(recipe_id))
    
    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if result:
        return result[0]


@api_router.get("/search/", status_code=200)
def search_recipes(
    keyword: Optional[str] = None, max_results: Optional[int] = 10
) -> dict:
    """

    Args:
        keyword (Optional[str], optional): search keyword. Defaults to None.
        max_results (Optional[int], optional): max_result. Defaults to 10.

    Returns:
        dict: recipes
    """
    if not keyword:
        return {"result": RECIPES[:max_results]}

    results = [recipe for recipe in RECIPES
               if keyword.lower() in recipe["label"].lower()]
    return {"result": results}
    


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
