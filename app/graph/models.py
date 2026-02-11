import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .database import Base

class Node(Base):
    __tablename__ = "nodes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False)
    source = Column(String, nullable=False)
    version = Column(Float, default=1.0)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    outgoing_edges = relationship(
        "Edge",
        foreign_keys="Edge.from_node",
        back_populates="from_node_rel",
    )

    incoming_edges = relationship(
        "Edge",
        foreign_keys="Edge.to_node",
        back_populates="to_node_rel",
    )

class Edge(Base):
    __tablename__ = "edges"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    from_node = Column(String, ForeignKey("nodes.id"))
    to_node = Column(String, ForeignKey("nodes.id"))
    relation_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    from_node_rel = relationship(
        "Node",
        foreign_keys=[from_node],
        back_populates="outgoing_edges",
    )
    to_node_rel = relationship(
        "Node",
        foreign_keys=[to_node],
        back_populates="incoming_edges",
    )
