from fastapi import  Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schema, Oauth2
from ..database import get_db
from typing import List, Optional


router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
    )


# @router.get("/", response_model= List[schema.Post] )
@router.get("/")
def get_posts(db: Session = Depends(get_db),current_user : int = Depends(Oauth2.get_current_user), limit: int = 10, skip = 0
              , search : Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM post """)
    # posts = cursor.fetchall()

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
    #     models.Votes, models.Votes.post_id == models.Post.id, isouter= True).group_by(models.Post.id).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schema.Post)
def create_posts(post: schema.CreatePost,db: Session = Depends(get_db),current_user : int = Depends(Oauth2.get_current_user)):#From body of Postman
    # cursor.execute("""  INSERT INTO post (title,content,published) VALUES (%s,%s,%s)  RETURNING * """,(post.title,
    #         post.content, post.published))
    # new_posts = cursor.fetchone()

    # conn.commit()#finalizing change
    new_posts = models.Post(user_id = current_user.id, **post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)

    return new_posts
 

@router.get("/{id}", response_model= schema.Post)
def get_post(id : int,db: Session = Depends(get_db),current_user : int = Depends(Oauth2.get_current_user)): #response : Response to run the other way
    # cursor.execute(f""" SELECT * FROM post WHERE id = {(str(id))} """)
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} was not found")
    
    # if post.user_id !=  current_user.id:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return{"messagae":f"Post with id {id} does not exist"}
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id : int, db: Session = Depends(get_db), current_user : int = Depends(Oauth2.get_current_user)):

    # cursor.execute(""" DELETE FROM post WHERE id = %s RETURNING * """, (str(id),) )
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    print(post)   

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Post with id {id} was not found")

    
    
    if post.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
    
    post.delete(synchronize_session= False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    


@router.put("/{id}",  response_model = schema.Post)
def update_post(id: int, updated_post: schema.UpdatePost, db: Session = Depends(get_db),current_user : int = Depends(Oauth2.get_current_user)):
    #cursor.execute(""" UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content,
                                                                                     #post.published,(str(id))))
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    # updated_post = cursor.fetchone()
    # conn.commit()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
    
    if post.user_id !=  current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
    
    post_query.update(updated_post.dict(), synchronize_session= False)

    db.commit()
    
    return post_query.first()


#@router.get("/", response_model= List[schema.Post] )

# @router.get("/userposts", response_model= List[schema.Post] )
# def get_userposts(db: Session = Depends(get_db),current_user : int = Depends(Oauth2.get_current_user)):
#     print(current_user.user_id)
#     post = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    l
#     return post


