from database import init_db, db_session
from models import Student, Room, Facility

def seed_database():
    """
    Populates our SQLite database with startup test data.
    This script should run once before starting the app to create tables.
    """
    print("1. Initializing Database...")
    init_db()

    # 2. Add sample students if missing
    if db_session.query(Student).count() == 0:
        print("2. Adding Students...")
        s1 = Student(name="Alice Smith", email="alice@example.com")
        s2 = Student(name="Bob Johnson", email="bob@example.com")
        db_session.add_all([s1, s2])

    # 3. Add sample rooms if missing
    if db_session.query(Room).count() == 0:
        print("3. Adding Study Rooms...")
        r1 = Room(room_number="101A", capacity=2, location="First Floor Library")
        r2 = Room(room_number="102B", capacity=6, location="Second Floor Lab")
        r3 = Room(room_number="205C", capacity=10, location="Main Building 2nd Floor")
        db_session.add_all([r1, r2, r3])
        
        # We need to commit here to generate IDs for rooms
        # IDs are required when linking foreign keys for tables like Facilities
        db_session.commit()

        print("4. Adding Facilities...")
        f1 = Facility(room_id=r1.id, name="Whiteboard")
        f2 = Facility(room_id=r1.id, name="Projector")
        f3 = Facility(room_id=r2.id, name="Smart TV")
        f4 = Facility(room_id=r3.id, name="Video Conferencing System")
        db_session.add_all([f1, f2, f3, f4])

    # Commit all final changes to SQLite
    db_session.commit()
    print("Database seeding completed.")

if __name__ == '__main__':
    seed_database()
