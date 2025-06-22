from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime, timedelta, date
from typing import List, Optional
import jwt
import hashlib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./trip_planner.db")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app
app = FastAPI(
    title="🎒 Trip Planner API",
    description="RESTful API for the Backpacking Trip Planner",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# ============================================================================
# DATABASE MODELS
# ============================================================================

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    trips = relationship("Trip", back_populates="owner", cascade="all, delete-orphan")

class Trip(Base):
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    destinations = Column(Text)
    travel_style = Column(String)
    group_size = Column(Integer, default=1)
    total_budget = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    owner = relationship("User", back_populates="trips")
    days = relationship("TripDay", back_populates="trip", cascade="all, delete-orphan")
    budget_categories = relationship("BudgetCategory", back_populates="trip", cascade="all, delete-orphan")

class TripDay(Base):
    __tablename__ = "trip_days"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    date = Column(Date)
    location = Column(String)
    transport_type = Column(String)
    transport_from = Column(String)
    transport_to = Column(String)
    transport_time = Column(String)
    transport_cost = Column(Float, default=0.0)
    accommodation_type = Column(String)
    accommodation_name = Column(String)
    accommodation_cost = Column(Float, default=0.0)
    notes = Column(Text)
    
    trip = relationship("Trip", back_populates="days")

class BudgetCategory(Base):
    __tablename__ = "budget_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    category_name = Column(String, nullable=False)
    budgeted_amount = Column(Float, default=0.0)
    spent_amount = Column(Float, default=0.0)
    
    trip = relationship("Trip", back_populates="budget_categories")

# Create tables
Base.metadata.create_all(bind=engine)

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TripDayCreate(BaseModel):
    day_number: int
    date: Optional[date] = None
    location: Optional[str] = None
    transport_type: Optional[str] = None
    transport_from: Optional[str] = None
    transport_to: Optional[str] = None
    transport_time: Optional[str] = None
    transport_cost: Optional[float] = 0.0
    accommodation_type: Optional[str] = None
    accommodation_name: Optional[str] = None
    accommodation_cost: Optional[float] = 0.0
    notes: Optional[str] = None

class TripDayResponse(TripDayCreate):
    id: int
    trip_id: int
    
    class Config:
        from_attributes = True

class BudgetCategoryCreate(BaseModel):
    category_name: str
    budgeted_amount: float
    spent_amount: Optional[float] = 0.0

class BudgetCategoryResponse(BudgetCategoryCreate):
    id: int
    trip_id: int
    
    class Config:
        from_attributes = True

class TripCreate(BaseModel):
    name: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    destinations: Optional[str] = None
    travel_style: Optional[str] = None
    group_size: Optional[int] = 1
    total_budget: Optional[float] = 0.0
    days: Optional[List[TripDayCreate]] = []
    budget_categories: Optional[List[BudgetCategoryCreate]] = []

class TripUpdate(TripCreate):
    pass

class TripResponse(BaseModel):
    id: int
    user_id: int
    name: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    destinations: Optional[str] = None
    travel_style: Optional[str] = None
    group_size: int
    total_budget: float
    created_at: datetime
    updated_at: datetime
    days: List[TripDayResponse] = []
    budget_categories: List[BudgetCategoryResponse] = []
    
    class Config:
        from_attributes = True

class TripSummary(BaseModel):
    id: int
    name: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    destinations: Optional[str] = None
    total_budget: float
    total_days: int
    total_cost: float
    completion_rate: float
    created_at: datetime
    updated_at: datetime

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    return hash_password(password) == hashed_password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def calculate_trip_completion(trip: Trip) -> float:
    if not trip.days:
        return 0.0
    
    total_days = len(trip.days)
    completed_days = 0
    
    for day in trip.days:
        required_fields = [day.location, day.transport_from, day.transport_to, day.accommodation_type]
        completed_fields = sum(1 for field in required_fields if field)
        if completed_fields >= 3:  # At least 75% of required fields
            completed_days += 1
    
    return completed_days / total_days if total_days > 0 else 0.0

def calculate_trip_cost(trip: Trip) -> float:
    total_cost = 0.0
    for day in trip.days:
        total_cost += (day.transport_cost or 0.0) + (day.accommodation_cost or 0.0)
    for budget_category in trip.budget_categories:
        total_cost += budget_category.spent_amount or 0.0
    return total_cost

# ============================================================================
# AUTH ENDPOINTS
# ============================================================================

@app.post("/auth/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Create new user
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.post("/auth/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_credentials.username).first()
    
    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@app.get("/auth/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# ============================================================================
# TRIP ENDPOINTS
# ============================================================================

@app.get("/trips", response_model=List[TripSummary])
def get_trips(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    trips = db.query(Trip).filter(Trip.user_id == current_user.id).all()
    
    trip_summaries = []
    for trip in trips:
        total_cost = calculate_trip_cost(trip)
        completion_rate = calculate_trip_completion(trip)
        
        trip_summary = TripSummary(
            id=trip.id,
            name=trip.name,
            start_date=trip.start_date,
            end_date=trip.end_date,
            destinations=trip.destinations,
            total_budget=trip.total_budget,
            total_days=len(trip.days),
            total_cost=total_cost,
            completion_rate=completion_rate,
            created_at=trip.created_at,
            updated_at=trip.updated_at
        )
        trip_summaries.append(trip_summary)
    
    return trip_summaries

@app.get("/trips/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == current_user.id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@app.post("/trips", response_model=TripResponse)
def create_trip(trip: TripCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_trip = Trip(
        user_id=current_user.id,
        name=trip.name,
        start_date=trip.start_date,
        end_date=trip.end_date,
        destinations=trip.destinations,
        travel_style=trip.travel_style,
        group_size=trip.group_size,
        total_budget=trip.total_budget
    )
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    
    # Add days
    for day_data in trip.days:
        db_day = TripDay(trip_id=db_trip.id, **day_data.dict())
        db.add(db_day)
    
    # Add budget categories
    for budget_data in trip.budget_categories:
        db_budget = BudgetCategory(trip_id=db_trip.id, **budget_data.dict())
        db.add(db_budget)
    
    db.commit()
    db.refresh(db_trip)
    return db_trip

@app.put("/trips/{trip_id}", response_model=TripResponse)
def update_trip(trip_id: int, trip: TripUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == current_user.id).first()
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Update trip details
    for field, value in trip.dict(exclude={'days', 'budget_categories'}).items():
        if value is not None:
            setattr(db_trip, field, value)
    
    db_trip.updated_at = datetime.utcnow()
    
    # Update days (delete existing and recreate)
    db.query(TripDay).filter(TripDay.trip_id == trip_id).delete()
    for day_data in trip.days:
        db_day = TripDay(trip_id=trip_id, **day_data.dict())
        db.add(db_day)
    
    # Update budget categories
    db.query(BudgetCategory).filter(BudgetCategory.trip_id == trip_id).delete()
    for budget_data in trip.budget_categories:
        db_budget = BudgetCategory(trip_id=trip_id, **budget_data.dict())
        db.add(db_budget)
    
    db.commit()
    db.refresh(db_trip)
    return db_trip

@app.delete("/trips/{trip_id}")
def delete_trip(trip_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == current_user.id).first()
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    db.delete(db_trip)
    db.commit()
    return {"message": "Trip deleted successfully"}

# ============================================================================
# ANALYTICS ENDPOINTS
# ============================================================================

@app.get("/trips/{trip_id}/analytics")
def get_trip_analytics(trip_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == current_user.id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Calculate analytics
    total_days = len(trip.days)
    total_cost = calculate_trip_cost(trip)
    completion_rate = calculate_trip_completion(trip)
    
    # Transport analysis
    transport_stats = {}
    accommodation_stats = {}
    daily_costs = []
    
    for day in trip.days:
        # Transport stats
        transport = day.transport_type or "Unknown"
        transport_stats[transport] = transport_stats.get(transport, 0) + 1
        
        # Accommodation stats
        accommodation = day.accommodation_type or "Unknown"
        accommodation_stats[accommodation] = accommodation_stats.get(accommodation, 0) + 1
        
        # Daily costs
        day_cost = (day.transport_cost or 0.0) + (day.accommodation_cost or 0.0)
        daily_costs.append({
            "day": day.day_number,
            "cost": day_cost,
            "location": day.location or "Unknown"
        })
    
    # Budget breakdown
    budget_breakdown = {
        "transport": sum((day.transport_cost or 0.0) for day in trip.days),
        "accommodation": sum((day.accommodation_cost or 0.0) for day in trip.days)
    }
    
    for budget_category in trip.budget_categories:
        budget_breakdown[budget_category.category_name] = budget_category.spent_amount or 0.0
    
    return {
        "trip_id": trip_id,
        "total_days": total_days,
        "total_cost": total_cost,
        "completion_rate": completion_rate,
        "average_daily_cost": total_cost / total_days if total_days > 0 else 0,
        "budget_utilization": (total_cost / trip.total_budget) * 100 if trip.total_budget > 0 else 0,
        "transport_stats": transport_stats,
        "accommodation_stats": accommodation_stats,
        "daily_costs": daily_costs,
        "budget_breakdown": budget_breakdown
    }

@app.get("/users/stats")
def get_user_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    trips = db.query(Trip).filter(Trip.user_id == current_user.id).all()
    
    total_trips = len(trips)
    total_days = sum(len(trip.days) for trip in trips)
    total_budget = sum(trip.total_budget for trip in trips)
    total_spent = sum(calculate_trip_cost(trip) for trip in trips)
    
    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "total_trips": total_trips,
        "total_days_planned": total_days,
        "total_budget": total_budget,
        "total_spent": total_spent,
        "average_trip_length": total_days / total_trips if total_trips > 0 else 0,
        "budget_efficiency": (total_spent / total_budget) * 100 if total_budget > 0 else 0
    }

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0"
    }

@app.get("/")
def root():
    return {
        "message": "🎒 Trip Planner API",
        "docs": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
