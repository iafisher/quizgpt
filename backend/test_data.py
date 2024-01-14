import argparse

import storage
from main import subject_to_json


def clear_data(db):
    confirm = input("Are you sure? ").strip().lower()
    if not confirm.startswith("y"):
        print("Aborting.")
        return

    db.query(storage.Subject).delete()
    db.commit()


def create_data(db):
    storage.Base.metadata.create_all(bind=storage.engine)
    count = db.query(storage.Subject).count()
    if count > 0:
        print("Data already exists.")
        return

    db_subject = storage.Subject(
        name="Postwar American history",
        description="The domestic history of the United States from 1945 to 1990",
        instructions="Ask me questions about the domestic history of the US from 1945 to 1990."
    )
    db.add(db_subject)
    db.commit()


def print_data(db):
    subject_list = db.query(storage.Subject).all()
    for subject in subject_list:
        print(subject_to_json(subject))

    if len(subject_list) > 0:
        print()
    print(f"{len(subject_list)} row(s).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    clear_parser = subparsers.add_parser("clear")
    create_parser = subparsers.add_parser("create")
    print_parser = subparsers.add_parser("print")

    args = parser.parse_args()
    try:
        db = storage.SessionLocal()

        if args.command == "clear":
            clear_data(db)
        elif args.command == "create":
            create_data(db)
        elif args.command == "print":
            print_data(db)
        else:
            raise Exception(f"invalid subcommand: {args.command}")
    finally:
        db.close()
