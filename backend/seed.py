import os, time
from app.db.session import Base, engine, SessionLocal
from app.models.models import User, Skill, Interest, Availability, Project, TeamMember
from app.core.security import hash_password
from datetime import time as dtime

skills=[("Python","Programming"),("Java","Programming"),("C++","Programming"),("JavaScript","Programming"),("TypeScript","Programming"),("React","Frontend"),("Next.js","Frontend"),("FastAPI","Backend"),("Node.js","Backend"),("Machine Learning","AI/ML"),("Deep Learning","AI/ML"),("Computer Vision","AI/ML"),("NLP","AI/ML"),("PostgreSQL","Database"),("MongoDB","Database"),("Docker","Cloud/DevOps"),("UI/UX","Design"),("Figma","Design")]
interests=["AI","Web Development","Healthcare","Education","FinTech","Startups","Research","Hackathons","Open Source","Cybersecurity"]

def seed():
    Base.metadata.create_all(engine)
    db=SessionLocal()
    if db.query(Skill).count()==0:
        db.add_all([Skill(name=n,category=c) for n,c in skills]); db.add_all([Interest(name=n) for n in interests]); db.commit()
    if db.query(User).count()==0:
        sk={s.name:s for s in db.query(Skill).all()}
        users=[]
        demo=[("Aarav","aarav@kiit.edu","Python,Machine Learning,FastAPI","AI,Healthcare"),("Riya","riya@kiit.edu","React,Next.js,TypeScript,UI/UX","Web Development,Startups"),("Kabir","kabir@kiit.edu","PostgreSQL,FastAPI,Node.js","Web Development,Open Source"),("Ananya","ananya@kiit.edu","Computer Vision,Python,Deep Learning","AI,Research"),("Dev","dev@kiit.edu","Java,C++,Machine Learning","Hackathons,AI"),("Meera","meera@kiit.edu","Figma,UI/UX,React","Design,Education")]
        for i,(name,email,ss,ints) in enumerate(demo,1):
            u=User(name=name,email=email,password_hash=hash_password("password123"),college="KIIT University",branch="CSE",year=2,is_verified=True,bio=f"{name} is a student interested in collaborative projects.")
            u.skills=[sk[x] for x in ss.split(',')]; u.interests=[db.query(Interest).filter_by(name=x).first() for x in ints.split(',')]
            u.availability=[Availability(day=d,start_time=dtime(18),end_time=dtime(22)) for d in range(5)]
            db.add(u); db.flush(); users.append(u)
        db.commit()
        p=Project(owner_id=users[0].id,name="Smart Queue",description="AI-powered queue prediction and campus service optimization platform.",category="AI / Web Development",team_size=4,duration_weeks=6,weekly_hours=6,skills=[sk["Machine Learning"],sk["React"],sk["PostgreSQL"],sk["FastAPI"]])
        db.add(p); db.flush(); db.add(TeamMember(project_id=p.id,user_id=users[0].id,role="Project Lead")); db.commit()
    db.close()

if __name__=="__main__":
    # wait briefly when launched against dockerized postgres
    for _ in range(20):
        try: seed(); break
        except Exception as e:
            time.sleep(2)
    else: raise RuntimeError("Database unavailable")
