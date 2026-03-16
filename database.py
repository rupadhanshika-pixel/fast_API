# Database Connection
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import mysql.connector


app = FastAPI()
def get_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="20102015",
        database="fast_api"
    )
    cursor = db.cursor(dictionary=True)
    try:
        yield cursor 
    finally:
        db.commit() 
        cursor.close() 
        db.close() 
        

class  user(BaseModel):
    name:str
    email:str
    age:int
    
# GET
@app.get('/viewuser')
def get_user(cursor=Depends(get_db)):
    cursor.execute("SELECT * FROM USERS")
    result=cursor.fetchall()
    return {"users":result}


# for single user
@app.get('/viewuser/{user_id}')
def get_user(user_id:int,cursor=Depends(get_db)):
    cursor.execute(f"SELECT * FROM USERS WHERE id={user_id}")
    result=cursor.fetchall()
    if not result:
        raise HTTPException(status_code=404,detail="User not found")    
    return {"user":result}

# POST
@app.post ("/create_user")
def create_user(user:user,cursor=Depends(get_db)):
    # cursor.execute(f"INSERT INTO USER (name,email,age) VALUES ('{user.name}','{user.email}',{user.age})")
    cursor.execute("INSERT INTO USERS (name,email,age) VALUES (%s,%s,%s)",(user.name,user.email,user.age))
    return {"message":"user created"}


# PUT
@app.put("/update_user/{user_id}", status_code=201)
def update_user(user_id:int,user:user,cursor=Depends(get_db)):
    cursor.execute(f"UPDATE USERS SET name ='{user.name}',email='{user.email}',age={user.age} WHERE id={user_id}")
    return {"message":"user updated"}

# DELETE
@app.delete("/delete_user/{user_id}", status_code=201)
def delete_user(user_id:int,cursor=Depends(get_db)):
    cursor.execute(f"SELECT * FROM USERS WHERE id={user_id}")
    result=cursor.fetchall()
    if not result:
        raise HTTPException(status_code=404,detail="User not found")
    cursor.execute(f"DELETE FROM USERS WHERE id={user_id}")
    return {"message":"user Deleted"}