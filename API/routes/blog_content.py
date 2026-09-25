from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException , status
from fastapi.encoders import jsonable_encoder

from oauth2 import get_current_user
from schemas import BlogContent, BlogContentResponse , db
from datetime import datetime



router = APIRouter(
    prefix="/blog" , 
    tags=["Blog Content"]
)


# TODO :Crud 

@router.post("" , response_description= "Create blog content" , response_model=BlogContentResponse)
async def create_blog(blog_content :BlogContent , current_user =Depends(get_current_user) ):
    try:
        blog_content = jsonable_encoder(blog_content)

        # additional information
        blog_content["author_name"] = current_user["name"]
        blog_content["author_id"] = str(current_user["_id"])
        blog_content["created_at"] = str(datetime.utcnow())

        new_blog_content = await db["blogPost"].insert_one(blog_content)

        created_blog_post = await db["blogPost"].find_one({"_id" : new_blog_content.inserted_id})


  

        return created_blog_post

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , 
            detail="Internal server error"
        )



@router.get(
    "",
    response_description="Get blog content",
    response_model=List[BlogContentResponse]
)
async def get_blogs(
    limit: int = 4,
    orderby: str = "created_at"
):
    try:
        blog_posts = await db["blogPost"].find({}).sort(
            orderby, -1
        ).to_list(limit)

        return blog_posts

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )



@router.get(
    "/{id}",
    response_description="Get blog content",
    response_model=BlogContentResponse
)
async def get_blogs(
    id : str
):
    try:
        blog_posts = await db["blogPost"].find_one({"_id" : ObjectId(id)})

        if blog_posts is None:
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="blog with id not found"
        )

        return blog_posts

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


    