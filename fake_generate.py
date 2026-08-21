from faker import Faker
from tasks.models import TaskModel
from users.models import UserModel
from core.database import SessionLocal


fake = Faker()
def seed_user(db):
    user = UserModel(username = fake.name())
    user.hash_password("123456789")
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"user create username:{user.username}, id:{user.id}")
    return user

def seed_task(db, user):
    for i in range(5):
        task = TaskModel(
            user_id = user.id ,
            title = fake.sentence(nb_words=6) ,
            description = fake.text(),
            is_complete = fake.boolean()
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        i += 1
    print(f"10 task created for user by {user.id} id")


def main():
    db = SessionLocal()
    try:
        user = seed_user(db)
        seed_task(db, user)
    finally:
        db.close()


if __name__ == "__main__":
    main()