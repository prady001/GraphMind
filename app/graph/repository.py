from sqlalchemy.orm import Session
from .models import Node, Edge
from .database import SessionLocal
import uuid
from datetime import datetime
from typing import List

class ContextRepository:
    def __init__(self):
        self.db: Session = SessionLocal()

    # NODE OPERATIONS

    def create_node(self, type: str, content: str, confidence: float, source: str) -> Node:
        node = Node(
            id=str(uuid.uuid4()),
            type=type,
            content=content,
            confidence=confidence,
            source=source,
            version=1.0,
            active=True,
            created_at=datetime.utcnow(),
        )
        self.db.add(node)
        self.db.commit()
        self.db.refresh(node)
        return node

    def get_node(self, node_id: str) -> Node:
        return self.db.query(Node).filter(Node.id == node_id).first()

    def deactivate_node(self, node_id: str) -> Node:
        node = self.get_node(node_id)
        if node:
            node.active = False
            self.db.commit()
        return node

    def get_active_nodes(self, limit: int = 20) -> List[Node]:
        return (
            self.db.query(Node)
            .filter(Node.active == True)
            .order_by(Node.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_nodes_by_type(self, node_type: str) -> List[Node]:
        return (
            self.db.query(Node)
            .filter(Node.active == True, Node.type == node_type)
            .all()
        )

    # EDGE OPERATIONS
    def create_edge(self, from_node_id: str, to_node_id: str, relation_type: str) -> Edge:
        from_node = self.get_node(from_node_id)
        to_node = self.get_node(to_node_id)

        if not from_node or not to_node:
            raise ValueError("Invalid node reference")

        edge = Edge(
            id=str(uuid.uuid4()),
            from_node=from_node_id,
            to_node=to_node_id,
            relation_type=relation_type,
            created_at=datetime.utcnow(),
        )

        self.db.add(edge)
        self.db.commit()
        self.db.refresh(edge)
        return edge


    def get_edges_from(self, node_id: str) -> List[Edge]:
        return (
            self.db.query(Edge)
            .filter(Edge.from_node == node_id)
            .all()
        )

    def get_edges_to(self, node_id: str) -> List[Edge]:
        return (
            self.db.query(Edge)
            .filter(Edge.to_node == node_id)
            .all()
        )

    def get_connected_nodes(self, node_id: str) -> List[Node]:
        node = self.get_node(node_id)
        if not node:
            return []

        connected = []

        # Outgoing
        for edge in node.outgoing_edges:
            if edge.to_node_rel and edge.to_node_rel.active:
                connected.append(edge.to_node_rel)

        # Incoming
        for edge in node.incoming_edges:
            if edge.from_node_rel and edge.from_node_rel.active:
                connected.append(edge.from_node_rel)

        return connected


    def close(self):
        self.db.close()

    # graph navigation

    def get_subgraph(self, root_id: str, depth: int = 2) -> List[Node]:
        visited = set()
        queue = [(root_id, 0)]
        result = []

        while queue:
            current_id, current_depth = queue.pop(0)

            if current_id in visited or current_depth > depth:
                continue

            visited.add(current_id)

            node = self.get_node(current_id)
            if node and node.active:
                result.append(node)

                neighbors = self.get_connected_nodes(current_id)
                for neighbor in neighbors:
                    queue.append((neighbor.id, current_depth + 1))

        return result
        