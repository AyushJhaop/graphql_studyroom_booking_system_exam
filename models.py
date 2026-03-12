from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    """Student database model."""
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    
    # Establish a one-to-many relationship with bookings
    bookings = relationship('Booking', back_populates='student')

class Room(Base):
    """Study room database model."""
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True)
    room_number = Column(String)
    capacity = Column(Integer)
    location = Column(String)
    
    # Establish one-to-many relationships
    bookings = relationship('Booking', back_populates='room')
    facilities = relationship('Facility', back_populates='room')

class Booking(Base):
    """Booking database model linking a student to a room for a specific time slot."""
    __tablename__ = 'booking'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    room_id = Column(Integer, ForeignKey('room.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String) # For example: "booked", "cancelled", "completed"
    
    # Define back-references
    student = relationship('Student', back_populates='bookings')
    room = relationship('Room', back_populates='bookings')
    reviews = relationship('Review', back_populates='booking')

class Facility(Base):
    """Facilities available inside a study room."""
    __tablename__ = 'facility'
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('room.id'))
    name = Column(String)
    
    # Back-reference to the Room model
    room = relationship('Room', back_populates='facilities')

class Review(Base):
    """Reviews left by a student after a booking."""
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('booking.id'))
    rating = Column(Integer)  # Rating score, e.g., 1 to 5
    comment = Column(String)
    
    # Back-reference to the Booking model
    booking = relationship('Booking', back_populates='reviews')
