from fastapi import APIRouter, HTTPException

from app.models import Message, Post, PostCreate, PostsPublic, PostUpdate

router = APIRouter(prefix="/posts", tags=["posts"])

PAGE_DEFAULT = 1
SIZE_DEFAULT = 10
SIZE_MAX = 20


@router.get("/", response_model=PostsPublic)
async def read_posts(
    q: str | None = None, page_in: int = PAGE_DEFAULT, size_in: int = SIZE_DEFAULT
):
    page = max(PAGE_DEFAULT, page_in)
    size = SIZE_DEFAULT if size_in < 1 else min(size_in, SIZE_MAX)
    skip = (page - 1) * size

    base_query = Post.find({"$text": {"$search": q}}) if q else Post.find()
    count = await base_query.count()

    pages = (count + size - 1) // size
    has_next = page < pages
    has_prev = page > 1

    posts = await base_query.skip(skip).limit(size).to_list()

    return PostsPublic(
        data=posts,
        count=count,
        page=page,
        pages=pages,
        size=size,
        has_next=has_next,
        has_prev=has_prev,
    )


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
