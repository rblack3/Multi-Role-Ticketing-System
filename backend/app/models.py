from sqlalchemy import ForeignKey, String, DateTime, Integer, Enum, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
import enum

class Base(DeclarativeBase):
    pass

class UserRole(enum.Enum):
    CUSTOMER = "customer"
    BUSINESS = "business" 
    VENDOR = "vendor"

class TicketStatus(enum.Enum):
    OPEN = "open"
    BUSINESS_ASSIGNED = "business_assigned"
    VENDOR_CONTACTED = "vendor_contacted"
    VENDOR_RESPONDED = "vendor_responded"
    RESOLVED = "resolved"

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

class Ticket(Base):
    __tablename__ = "tickets"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus))

    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    business_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    vendor_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    customer: Mapped['User'] = relationship(foreign_keys=[customer_id])
    business: Mapped['User'] = relationship(foreign_keys=[business_id])
    vendor: Mapped['User'] = relationship(foreign_keys=[vendor_id])
    messages: Mapped['Message'] = relationship(back_populates="ticket")

class Message(Base):
    __tablename__ = "messages"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_id: Mapped[int] = mapped_column(Integer, ForeignKey("tickets.id"))
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)

    content: Mapped[str] = mapped_column(String(300), nullable=False)
    message_type: Mapped[str] = mapped_column(String, default="general")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    # Relationships
    ticket: Mapped['Ticket'] = relationship(back_populates="messages")
    sender: Mapped['User'] = relationship(foreign_keys=[sender_id])
    recipient: Mapped['User'] = relationship(foreign_keys=[recipient_id])