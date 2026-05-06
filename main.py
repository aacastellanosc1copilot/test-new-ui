from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import uvicorn

DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(200), nullable=False)
    last_name = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    persons = db.query(Person).order_by(Person.id.desc()).all()
    return templates.TemplateResponse("index.html", {"request": request, "persons": persons})

@app.post("/submit")
def submit(request: Request, first_name: str = Form(...), last_name: str = Form(...), db: Session = Depends(get_db)):
    first = first_name.strip()
    last = last_name.strip()
    if first == "" and last == "":
        return RedirectResponse("/", status_code=303)
    person = Person(first_name=first, last_name=last)
    db.add(person)
    db.commit()
    return RedirectResponse("/", status_code=303)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)