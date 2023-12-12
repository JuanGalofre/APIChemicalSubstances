from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql


try:
    connection=psycopg2.connect(dbname="Substances",user="postgres",password="12345", host="localhost",cursor_factory=RealDictCursor)
    cursor = connection.cursor()
    print("Database connection was successfull")
except psycopg2.OperationalError as e:
    print("Database connection was not possible, error:", e)
class Post(BaseModel):
    name: str
    molecular_formula: str
    molar_mass: float
    cas: str
    sga_classified: bool = True 
    hazardous_reactions: Optional[str] = None



app = FastAPI()

@app.get("/")
async def root():
    return{"message":"What's up"}

#GETs

@app.get("/substances")
def get_substances():
    cursor.execute("""SELECT * from public."Basic substances" ORDER BY id ASC""")
    substances= cursor.fetchall()
    return {"data":substances}

@app.get("/substances/latest")
def get_substance():
    cursor.execute("""SELECT * from public."Basic substances" ORDER BY id DESC LIMIT 1 """)
    substance= cursor.fetchone()
    return {"data":substance}

@app.get("/substances/{id}")
def get_substance(id: int):
    
    query = sql.SQL("SELECT * FROM public.\"Basic substances\" WHERE id = %s")
    cursor.execute(query,(id,))
    substance= cursor.fetchone()
    if not substance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    else:
        return {"data":substance}

#POSTs

@app.post("/substances", status_code=status.HTTP_201_CREATED)
def create_substances(post: Post):
    dictPost=post.model_dump()
    query = sql.SQL("INSERT INTO public.\"Basic substances\" (name, molecular_formula,molar_mass,cas,sga_classified) VALUES (%s,%s,%s,%s,%s) returning *")
    cursor.execute(query,(dictPost["name"],dictPost["molecular_formula"],dictPost["molar_mass"],dictPost["cas"],dictPost["sga_classified"]))
    substance= cursor.fetchone()
    connection.commit()
    return{"message": "The data was successfully added", "confirmation":substance}

#Delete
@app.delete("/substances/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_formula(id: int):
    query = sql.SQL("DELETE FROM public.\"Basic substances\" WHERE id = %s returning *")
    cursor.execute(query,(id,))
    substance= cursor.fetchone()
    if not substance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"substance with id: {id} was not found")
    connection.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#Update
@app.put("/substances/{id}")
def update_formula(id: int, post: Post):
    post = post.model_dump()
    query = sql.SQL("UPDATE public.\"Basic substances\" SET name = %s, molecular_formula = %s, molar_mass = %s, cas = %s, sga_classified = %s  WHERE id = %s returning *")
    cursor.execute(query,(post["name"],post["molecular_formula"],post["molar_mass"],post["cas"],post["sga_classified"],id))
    substance= cursor.fetchone()
    if not substance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"substance with id: {id} was not found")
    connection.commit()
    return{"message": "The data was successfully modified", "confirmation":substance}