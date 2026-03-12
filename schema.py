import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from database import db_session
from models import Student as StudentModel
from models import Room as RoomModel
from models import Booking as BookingModel
from models import Facility as FacilityModel
from models import Review as ReviewModel
from datetime import datetime

# ==========================================
# 1. DEFINE GRAPHQL TYPES (BASED ON MODELS)
# ==========================================

class Student(SQLAlchemyObjectType):
    class Meta:
        model = StudentModel
        interfaces = (graphene.relay.Node, )

class Room(SQLAlchemyObjectType):
    class Meta:
        model = RoomModel
        interfaces = (graphene.relay.Node, )

class Booking(SQLAlchemyObjectType):
    class Meta:
        model = BookingModel
        interfaces = (graphene.relay.Node, )

class Facility(SQLAlchemyObjectType):
    class Meta:
        model = FacilityModel
        interfaces = (graphene.relay.Node, )

class Review(SQLAlchemyObjectType):
    class Meta:
        model = ReviewModel
        interfaces = (graphene.relay.Node, )


# ==========================================
# 2. DEFINE QUERIES (READING DATA)
# ==========================================
class Query(graphene.ObjectType):
    # Definition of available queries
    rooms = graphene.List(Room, capacityGreaterThan=graphene.Int())
    facilities = graphene.List(Facility, roomId=graphene.Int(required=True))
    bookings = graphene.List(Booking, studentId=graphene.Int(required=True))

    def resolve_rooms(self, info, capacityGreaterThan=None):
        """Resolver for fetching rooms, supports filtering by capacity."""
        query = Room.get_query(info)
        if capacityGreaterThan is not None:
            # Filter where capacity is strictly greater than given value
            query = query.filter(RoomModel.capacity > capacityGreaterThan)
        return query.all()

    def resolve_facilities(self, info, roomId):
        """Resolver for fetching facilities for a specific room."""
        query = Facility.get_query(info)
        return query.filter(FacilityModel.room_id == roomId).all()

    def resolve_bookings(self, info, studentId):
        """Resolver for listing all bookings of a specific student."""
        query = Booking.get_query(info)
        return query.filter(BookingModel.student_id == studentId).all()


# ==========================================
# 3. DEFINE MUTATIONS (MODIFYING DATA)
# ==========================================

class BookRoomInput(graphene.InputObjectType):
    """Input fields required to book a room."""
    studentId = graphene.Int(required=True)
    roomId = graphene.Int(required=True)
    startTime = graphene.String(required=True) # Expected format: "YYYY-MM-DDTHH:MM:SS"
    endTime = graphene.String(required=True)

class BookRoom(graphene.Mutation):
    """Mutation to book a study room."""
    class Arguments:
        input = BookRoomInput(required=True)

    # We return the booked room data directly
    Output = Booking

    def mutate(self, info, input):
        # 1. Parse date strings to Python datetime objects
        start = datetime.fromisoformat(input.startTime)
        end = datetime.fromisoformat(input.endTime)

        # 2. Business logic: Prevent time conflicts
        # Overlap logic: (existing_start < new_end) AND (existing_end > new_start)
        conflicts = db_session.query(BookingModel).filter(
            BookingModel.room_id == input.roomId,
            BookingModel.status == 'booked',
            BookingModel.start_time < end,
            BookingModel.end_time > start
        ).count()

        if conflicts > 0:
            raise Exception("Time conflict: The room is already booked for the selected time.")

        # 3. Create the booking entry and set default status
        booking = BookingModel(
            student_id=input.studentId,
            room_id=input.roomId,
            start_time=start,
            end_time=end,
            status="booked"
        )
        db_session.add(booking)
        db_session.commit()
        return booking


class CancelBooking(graphene.Mutation):
    """Mutation to cancel an existing booking."""
    class Arguments:
        id = graphene.Int(required=True)

    Output = Booking

    def mutate(self, info, id):
        # 1. Fetch the existing booking from ID
        booking = db_session.query(BookingModel).get(id)
        if not booking:
            raise Exception("Booking not found.")

        # 2. Update status
        booking.status = "cancelled"
        db_session.commit()
        return booking


class AddReviewInput(graphene.InputObjectType):
    """Input fields to leave a review after studying."""
    bookingId = graphene.Int(required=True)
    rating = graphene.Int(required=True)
    comment = graphene.String()

class AddReview(graphene.Mutation):
    """Mutation to add a review to a past booking."""
    class Arguments:
        input = AddReviewInput(required=True)

    Output = Review

    def mutate(self, info, input):
        # 1. Ensure the booking exists before reviewing
        booking = db_session.query(BookingModel).get(input.bookingId)
        if not booking:
            raise Exception("Booking not found.")

        # 2. Add review
        review = ReviewModel(
            booking_id=input.bookingId,
            rating=input.rating,
            comment=input.comment
        )
        db_session.add(review)
        db_session.commit()
        return review

# Map available mutations into a root class
class Mutation(graphene.ObjectType):
    bookRoom = BookRoom.Field()
    cancelBooking = CancelBooking.Field()
    addReview = AddReview.Field()

# ==========================================
# 4. EXPORT SCHEMA
# ==========================================
# Combine Queries and Mutations into final Schema to be exported to app.py
schema = graphene.Schema(query=Query, mutation=Mutation)
