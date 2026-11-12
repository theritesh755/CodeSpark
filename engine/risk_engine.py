from engine.peel_detector import detect_peel_chains
from engine.mixer_detector import detect_mixer_patterns
from engine.smurfing_detector import detect_smurfing
from engine.bridge_detector import detect_bridge_correlations
from engine.receiver_ranker import rank_receivers

def analyze_graph(graph, transactions):
    findings = detect_peel_chains(graph) + detect_mixer_patterns(graph) + detect_smurfing(graph)
    findings += detect_bridge_correlations(transactions)
    return {"findings": findings, "ranked_receivers": rank_receivers(graph, findings)}
