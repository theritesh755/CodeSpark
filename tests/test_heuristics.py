import networkx as nx
from engine.peel_detector import detect_peel_chains
from engine.mixer_detector import detect_mixer_patterns

def test_peel_detector():
    g = nx.DiGraph()
    g.add_edge("a", "b", value=90)
    g.add_edge("a", "c", value=10)
    g.add_edge("b", "d", value=80)
    assert detect_peel_chains(g)

def test_mixer_detector():
    g = nx.DiGraph()
    for i in range(4):
        g.add_edge(f"in{i}", "m")
        g.add_edge("m", f"out{i}")
    assert detect_mixer_patterns(g)
