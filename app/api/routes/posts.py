from beanie import DeleteRules, WriteRules
from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentUser
from app.models.post import Message, Post, PostCreate, PostsPublic, PostUpdate

router = APIRouter(prefix="/posts", tags=["posts"])

PAGE_DEFAULT = 1
SIZE_DEFAULT = 10
SIZE_MAX = 20


@router.get("/", response_model=PostsPublic)
async def read_posts(
    q: str | None = None, page_in: int = PAGE_DEFAULT, size_in: int = SIZE_DEFAULT
):
    """
    Retrieve posts with search and pagination.
    """
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


@router.get("/{id}", response_model=Post)
async def read_post(id: str):
    """
    Get post by ID.
    """
    post = await Post.get(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.post("/", response_model=Post)
async def create_post(post_in: PostCreate, current_user: CurrentUser):
    """
    Create a new post.
    """
    post = Post(**post_in.model_dump(), author=current_user.username)
    return await post.save(link_rule=WriteRules.WRITE)


@router.put("/{id}", response_model=Post)
async def update_post(id: str, post_in: PostUpdate, current_user: CurrentUser):
    """
    Update a post.
    """
    post = await Post.get(id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author != current_user.username:
        raise HTTPException(status_code=403, detail="Forbidden")

    return await post.replace(
        post_in.model_dump(exclude_unset=True), link_rule=WriteRules.WRITE
    )


@router.delete("/{id}", response_model=Message)
async def delete_post(id: str, current_user: CurrentUser):
    """
    Delete a post.
    """
    post = await Post.get(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author != current_user.username:
        raise HTTPException(status_code=403, detail="Forbidden")

    await post.delete(link_rule=DeleteRules.DELETE_LINKS)
    return Message(message="Post deleted successfully")
