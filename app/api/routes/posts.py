from fastapi import APIRouter, HTTPException

from app.models import Message, Post, PostCreate, PostsPublic, PostUpdate

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=PostsPublic)
async def read_posts():
    posts = await Post.find().to_list()
    return PostsPublic(data=posts)


@router.get("/{id}", response_model=Post)
async def read_post(id: str):
    post = await Post.get(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/", response_model=Post)
async def create_post(post_in: PostCreate):
    post = Post(**post_in.model_dump())
    return await post.insert()


@router.put("/{id}", response_model=Post)
async def update_post(id: str, post_in: PostUpdate):
    post = await Post.get(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return await post.set({**post_in.model_dump(exclude_unset=True)})


@router.delete("/{id}", response_model=Message)
async def delete_post(id: str):
    post = await Post.get(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await post.delete()
    return Message(message="Post deleted successfully")
