from fastapi import FastAPI, HTTPException
from .models import Base, User,Comment,Post, Tag
from sqlalchemy.ext.asyncio import AsyncSession
from .api.routes import user_router 
from .database import engine
# Initialize app
app = FastAPI()


async def populate_db(db: AsyncSession):
 try:
    # Create sample users
    user1 = User(username="alice")
    user2 = User(username="bob")
    user3 = User(username="mark")
    user4 = User(username="anthony")
    user5 = User(username="sasha")
    user6 = User(username="lilly")
    db.add_all([user1, user2, user3, user4, user5, user6])
    
    # Create sample tags
    tag1 = Tag(tag_name="python")
    tag2 = Tag(tag_name="fastapi")
    tag3 = Tag(tag_name="sqlalchemy")
    tag4 = Tag(tag_name="example")
    tag5 = Tag(tag_name="data")
    tag6 = Tag(tag_name="maths")
    db.add_all([tag1, tag2, tag3, tag4, tag5, tag6])
    
    # Create sample posts
    post1 = Post(title="First Post", content="This is my first post!", status="draft", user_id=1)
    post2 = Post(title="Learning FastAPI1", content="FastAPI1 is great!", status="not_a_draft",user_id=2)
    post3 = Post(title="Third Post", content="This is my first post!", status="draft", user_id=3)
    post4 = Post(title="Learning FastAPI2", content="FastAPI2 is great!", status="not_a_draft",user_id=4)
    post5 = Post(title="Fifth post", content="This is my first post!", status="draft", user_id=5)
    post6 = Post(title="Learning FastAPI4", content="FastAPI4 is great!", status="not_a_draft",user_id=1)
    post6 = Post(title="Learning FastAPI5", content="FastAPI5 is great!", status="other",user_id=2)
    post6 = Post(title="Learning FastAPI6", content="FastAPI6 is great!", status="not_a_draft",user_id=2)
    post1.tags.append(tag1)
    post1.tags.append(tag2)
    post1.tags.append(tag3)
    post1.tags.append(tag4)
    post2.tags.append(tag2)
    post2.tags.append(tag4)
    post3.tags.append(tag1)
    post3.tags.append(tag2)
    post4.tags.append(tag2)
    post4.tags.append(tag3)
    post5.tags.append(tag5)
    post5.tags.append(tag3)
    post6.tags.append(tag2)
    post6.tags.append(tag3)

     # Create sample comments
    comment1 = Comment(content="Comment text 1", user_id=1, post_id=1)
    comment2 = Comment(content="Comment text 2", user_id=2, post_id=1)
    comment3 = Comment(content="Comment text 3", user_id=3, post_id=2)
    comment4 = Comment(content="Comment text 4", user_id=4, post_id=2)
    comment5 = Comment(content="Comment text 5", user_id=5, post_id=3)
    comment6 = Comment(content="Comment text 6", user_id=1, post_id=3)
    comment7 = Comment(content="Comment text 7", user_id=1, post_id=3)
    comment8 = Comment(content="Comment text 8", user_id=6, post_id=4)
    comment9 = Comment(content="Comment text 9", user_id=2, post_id=5)
    db.add_all([comment1, comment2, comment3, comment4, comment5, comment6, comment7, comment8, comment9])
    

    post1.comments.append(comment1)
    post1.comments.append(comment2)
    post2.comments.append(comment3)
    post2.comments.append(comment4)
    post3.comments.append(comment5)
    post3.comments.append(comment6)
    post3.comments.append(comment7)
    post4.comments.append(comment8)
    post5.comments.append(comment9)

   
    db.add_all([post1, post2, post3, post4, post5, post6])
    
    await db.commit()
    pass
 except Exception as e:
        print(e)  
        raise HTTPException(status_code=500, detail=str(e))
 return {"message": "Sample data populated successfully!"}


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn: 
       await conn.run_sync(Base.metadata.drop_all)  
       await conn.run_sync(Base.metadata.create_all)  

    async with AsyncSession(engine) as db:
            await populate_db(db)


app.include_router(user_router)
