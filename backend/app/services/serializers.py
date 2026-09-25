def user_summary(user):
    prof = {s.id: 0.5 for s in user.skills}
    return {
        "id": user.id, "name": user.name, "email": user.email,
        "college": user.college, "branch": user.branch, "year": user.year,
        "bio": user.bio, "skills": [{"id": s.id, "name": s.name, "category": s.category, "proficiency": prof.get(s.id, .5)} for s in user.skills],
        "interests": [i.name for i in user.interests],
        "availability": [{"day": a.day, "start_time": a.start_time.strftime('%H:%M'), "end_time": a.end_time.strftime('%H:%M')} for a in user.availability],
        "projects": [{"id": p.id, "name": p.name, "category": p.category} for p in user.projects],
    }
