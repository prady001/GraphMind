from app.graph.repository import ContextRepository
from app.graph.models import Base
from app.graph.database import engine

# recria banco limpo
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

repo = ContextRepository()

# Criando nós
question = repo.create_node(
    type="QUESTION",
    content="Should I expand to the US?",
    confidence=1.0,
    source="user"
)

fact = repo.create_node(
    type="FACT",
    content="US has high regulatory complexity",
    confidence=0.9,
    source="llm"
)

assumption = repo.create_node(
    type="ASSUMPTION",
    content="High regulation increases operational cost",
    confidence=0.8,
    source="llm"
)

# Criando edges
repo.create_edge(question.id, fact.id, "SUPPORTED_BY")
repo.create_edge(fact.id, assumption.id, "LEADS_TO")

# Testando subgraph depth=1
subgraph_depth_1 = repo.get_subgraph(question.id, depth=1)

print("\nDepth 1:")
for node in subgraph_depth_1:
    print(node.type, node.content)

# Testando subgraph depth=2
subgraph_depth_2 = repo.get_subgraph(question.id, depth=2)

print("\nDepth 2:")
for node in subgraph_depth_2:
    print(node.type, node.content)

repo.close()
