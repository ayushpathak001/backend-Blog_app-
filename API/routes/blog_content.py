from json import JSONDecoder
from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Response , status
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





@router.put(
    "/{id}",
    response_description="Update blog content",
    response_model=BlogContentResponse
)
async def update_blog(
    id: str,
    blog_content: BlogContent,
    current_user=Depends(get_current_user)
):
    try:
        # Convert string ID from URL into MongoDB ObjectId
        blog_id = ObjectId(id)

        # Find the blog post
        blog_post = await db["blogPost"].find_one(
            {"_id": blog_id}
        )

        if blog_post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog content not found."
            )

        # Check whether current user is the author
        if blog_post["author_id"] != str(current_user["_id"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not the author of this blog post"
            )

        # Remove fields whose value is None
        blog_content = {
            k: v
            for k, v in blog_content.model_dump().items()
            if v is not None
        }

        if len(blog_content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data provided for update"
            )

        # Update blog
        update_result = await db["blogPost"].update_one(
            {"_id": blog_id},
            {"$set": blog_content}
        )

        # Get updated blog
        updated_blog_post = await db["blogPost"].find_one(
            {"_id": blog_id}
        )

        return updated_blog_post

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid blog ID"
        )

    except HTTPException:
        raise

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

 


@router.delete(
    "/{id}",
    response_description="Delete blog post"
)
async def delete_blog_post(
    id: str,
    current_user=Depends(get_current_user)
):
    try:
        blog_id = ObjectId(id)

        # Find blog post
        blog_post = await db["blogPost"].find_one(
            {"_id": blog_id}
        )

        if blog_post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog content not found"
            )

        # Check author
        if blog_post["author_id"] != str(current_user["_id"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not the author of this blog post"
            )

        # Delete blog
        delete_result = await db["blogPost"].delete_one(
            {"_id": blog_id}
        )

        if delete_result.deleted_count == 1:
            return Response(
                status_code=status.HTTP_204_NO_CONTENT
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

    except HTTPException:
        raise

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
