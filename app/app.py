from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_table, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Automatically creating database immediately after the app starts."""
    await create_db_and_table()
    yield


app = FastAPI(lifespan=lifespan)


text_posts = {
    1: {
        "title": "Getting Started with Python",
        "content": "Python is a versatile programming language known for its readability and broad ecosystem.",
    },
    2: {
        "title": "Understanding Data Structures",
        "content": "Data structures such as lists, dictionaries, and sets are fundamental to efficient Python programs.",
    },
    3: {
        "title": "Intro to Data Analysis",
        "content": "Data analysis involves cleaning, transforming, and interpreting data to extract insights.",
    },
    4: {
        "title": "Working with APIs",
        "content": "APIs allow applications to communicate by exchanging structured requests and responses.",
    },
    5: {
        "title": "Error Handling Best Practices",
        "content": "Proper error handling improves reliability by anticipating and managing runtime failures.",
    },
    6: {
        "title": "Object-Oriented Programming",
        "content": "OOP organizes code into classes and objects to improve modularity and reuse.",
    },
    7: {
        "title": "Introduction to Machine Learning",
        "content": "Machine learning enables systems to learn patterns from data without explicit programming.",
    },
    8: {
        "title": "Optimizing Python Code",
        "content": "Performance optimization focuses on reducing complexity and eliminating unnecessary operations.",
    },
    9: {
        "title": "Testing and Debugging",
        "content": "Testing and debugging are essential practices for maintaining correct and stable software.",
    },
    10: {
        "title": "Deploying Python Applications",
        "content": "Deployment involves packaging, configuring, and releasing applications to production environments.",
    },
}


@app.get("/")
def root():
    return {"status": "OK"}


@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts


@app.get("/posts/{id}")
def get_post(id: int) -> PostResponse:
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(id)


@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse:
    new_post = {
        "title": post.title,
        "content": post.content,
    }
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post
