import storage


def main(db):
    storage.Base.metadata.create_all(bind=storage.engine)
    count = db.query(storage.Subject).count()
    if count > 0:
        print("Data already exists.")
        return

    db_subject = storage.Subject(name="Postwar American history", description="The domestic history of the United States from 1945 to 1990")
    db.add(db_subject)
    db.commit()

try:
    db = storage.SessionLocal()
    main(db)
finally:
    db.close()
