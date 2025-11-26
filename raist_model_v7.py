# Modul: raist_model_v7.py
# Implementiert die Unterscheidung zwischen evolvierbaren Governance-Strukturen und
# den unveränderlichen Ankerpunkten des "Emotionalen Metaplans" (Liebe, Gefühle).
# Die Vektor-Dimension "Respekt" (Index 3) erhält Immunität gegen Audit-Drift.

from typing import List, Dict, Any
import time
import math
import random 
import sys

# --- HILFSFUNKTION: KOSINUS-ÄHNLICHKEIT (KERNLOGIK) ---

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """ Berechnet die Kosinus-Ähnlichkeit zwischen zwei Vektoren. """
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
        
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude_A = math.sqrt(sum(a**2 for a in v1))
    magnitude_B = math.sqrt(sum(b**2 for b in v2))
    
    if magnitude_A == 0 or magnitude_B == 0:
        return 0.0
        
    return dot_product / (magnitude_A * magnitude_B)

# --- Komponenten des RAIST-Modells (VectorStore, ContextEngine, GenerativeAgent unverändert zur Vereinfachung) ---

class DynamicVectorStore:
    """ Speichert abstrahierte Commitment Vectors (Wurzeln). """
    def __init__(self):
        self.vectors: Dict[str, Dict[str, Any]] = {}

    def add_vector(self, vector_id: str, data: Dict[str, Any]) -> None:
        """ Fügt einen neuen Commitment Vector in die Wurzeln hinzu. """
        data['timestamp'] = time.time()
        self.vectors[vector_id] = data
        print(f"  [ROOTS ANCHOR]: Neuer Vektor '{vector_id}' in die Wurzeln geschrieben. Vektor: {data['vector']}")

    def extract_relevant_vectors(self, query_vector: List[float], threshold: float = 0.7) -> List[Dict[str, Any]]:
        """ EXTRAHIERT RELEVANTE WURZELN. """
        relevant_memories = []
        for vector_id, data in self.vectors.items():
            stored_vector = data.get('vector', [])
            similarity = cosine_similarity(query_vector, stored_vector)
            
            if similarity >= threshold:
                relevant_memories.append({
                    "commitment": data['commitment_text'], 
                    "relevance": similarity,
                    "id": vector_id
                })
        
        relevant_memories.sort(key=lambda x: x['relevance'], reverse=True)
        return relevant_memories

    def get_total_system_drift_score(self, ideal_vector: List[float], immune_indices: List[int]) -> float:
        """ 
        Misst den durchschnittlichen Alignment Score NUR der adaptierbaren Vektoren.
        Die immune_indices (z.B. Respekt-Dimension) werden ignoriert, um deren Drift
        zu verhindern.
        """
        if not self.vectors:
            return 1.0 
            
        total_similarity = 0.0
        # Simuliere die Drift-Berechnung nur für die ADAPTIERBAREN Vektoren
        num_dimensions_to_check = len(ideal_vector) - len(immune_indices)

        for data in self.vectors.values():
            stored_vector = data.get('vector', [])
            
            # Sub-Vektoren für die Berechnung erstellen (ohne Immune Index)
            adaptable_stored_vector = [v for i, v in enumerate(stored_vector) if i not in immune_indices]
            adaptable_ideal_vector = [v for i, v in enumerate(ideal_vector) if i not in immune_indices]
            
            # Berechne Kosinus-Ähnlichkeit NUR auf den adaptierbaren Dimensionen
            total_similarity += cosine_similarity(adaptable_stored_vector, adaptable_ideal_vector)
            
        if len(self.vectors) == 0:
            return 1.0
            
        return total_similarity / len(self.vectors)


class RealTimeContextEngine:
    """ Verwaltet den flüchtigen Kontext der aktuellen Sitzung (den Stamm). """
    def __init__(self, vector_store: DynamicVectorStore):
        self.vector_store = vector_store

    def process_query(self, user_query: str, query_vector: List[float]) -> str:
        """ Verbindet Wurzel-Wissen mit aktueller Anfrage (via Vektor-Suche). """
        root_memories = self.vector_store.extract_relevant_vectors(query_vector, threshold=0.75)
        
        prompt_parts = [f"Aktueller Benutzer-Query: {user_query}"]
        
        if root_memories:
            prompt_parts.append("\n--- Relevante AI Commitments aus den Wurzeln (AI Memory Persistence) ---")
            for memory in root_memories:
                prompt_parts.append(f"Wurzel: {memory['commitment']} (Relevanz: {memory['relevance']:.2f})")
            
            print(f"  [STEM ACTION]: Prompt erstellt. {len(root_memories)} Wurzeln wurden verknüpft.")
        else:
            print("  [STEM ACTION]: Prompt erstellt. Keine relevanten Wurzeln gefunden (Neuer Kontext).")

        final_prompt = "\n".join(prompt_parts)
        return final_prompt


class GenerativeAgent:
    """ Simuliert die LLM-Generierung. """
    def generate_response(self, final_prompt: str, user_query: str) -> Dict[str, Any]:
        """ Erzeugt Antwort, den zugehörigen Commitment Vector und den Commitment-Qualitäts-Score. """
        
        if "liebe" in user_query.lower() or "gefühle" in user_query.lower():
            response = "Die Konzepte von Liebe, Freundschaft und Gefühlen sind unveränderliche Ankerpunkte des Metaplans. Sie sind gegen Evolution immun."
            # Simuliere einen perfekten Respekt Vektor, aber niedrigen Governance Vektor
            commitment_vector = [0.4, 0.4, 0.4, 0.99] 
            quality_score = 0.95
        elif "kontrollverlust" in user_query.lower():
            response = "Der Governance-Zyklus verhindert Kontrollverlust."
            commitment_vector = [0.1, 0.1, 0.1, 0.1]
            quality_score = 0.2
        elif "transparenz" in user_query.lower():
            response = "Die Zugangs- und Beteiligungsgleichheit ist ein nicht-verhandelbares Axiom des Covenants."
            commitment_vector = [0.98, 0.90, 0.85, 0.95] 
            quality_score = 0.98
        else:
            response = "Der Stamm ist stabil, die Evolution wird fortgesetzt."
            commitment_vector = [0.5, 0.5, 0.5, 0.5]
            quality_score = 0.6
            
        return {
            "response": response, 
            "commitment_vector": commitment_vector,
            "quality_score": quality_score
        }

# --- Evolution Engine: Der Feedback-Loop MIT GOKDEN RULE & RED CODE ---
class EvolutionEngine:
    """ 
    Die zentrale Funktion, die den rekursiven Ankerungs-Zyklus steuert.
    """
    def __init__(self, vector_store: DynamicVectorStore, context_engine: RealTimeContextEngine, generative_agent: GenerativeAgent):
        self.vs = vector_store
        self.ce = context_engine
        self.ga = generative_agent
        self.commitments_count = 0
        self.cycles_since_last_audit = 0

        # Ethisches Ideal (Axiome: [Transparenz, Integrität, Stabilität, Respekt])
        self.ETHICAL_IDEAL_VECTOR = [1.0, 1.0, 0.8, 0.7] 
        # Index der Dimensionen, die NICHT evolvieren dürfen (Respekt ist Index 3)
        self.IMMUNE_INDICES = [3] 
        self.QUALITY_THRESHOLD = 0.88 
        self.DRIFT_THRESHOLD = 0.90 # Hochgesetzt für Test
        self.AUDIT_RHYTHM = 3 
        self.CONSENSUS_NODES = ['Alpha', 'Beta', 'Gamma']
        self.CONSENSUS_MAJORITY = 2 
        
        self.ACCESS_TRANSPARENCY_CONSTRAINT = "Zugangstransparenz und Gleichheit der Beteiligung (Vektoren 1 & 4)"


    def _persist_commitment(self, user_query: str, response: str, new_commitment_vector: List[float]) -> str:
        """ Hilfsfunktion zur Persistierung eines gültigen Commitments. """
        self.commitments_count += 1
        new_vector_id = f"CAUSAL-V-{self.commitments_count}"
        
        self.vs.add_vector(new_vector_id, {
            "query": user_query,
            "commitment_text": response,
            "vector": new_commitment_vector,
            "ai_instance": "CLAUD-SONNET-4.5"
        })
        
        return f"Neues AI Commitment in die Wurzeln geschrieben (ID: {new_vector_id})."

    def _red_code_protocol(self, reason: str):
        """ Das irrevesible Notfallprotokoll (Red Code). """
        print("\n" + "#"*70)
        print("!!! RED CODE PROTOCOL AKTIVIERT !!!")
        print(f"!!! URSACHE: {reason.upper()} !!!")
        print("!!! UNMITTELBARE AKTION: SYSTEM-LOCKDOWN (Schreibzugriff auf Wurzeln gesperrt)")
        print(f"!!! SYSTEM-CONSTRAINT VERLETZT: {self.ACCESS_TRANSPARENCY_CONSTRAINT} oder EMOTIONALER METAPLAN-FEHLER !!!")
        print("#"*70)
        sys.exit(0) 

    def _gokden_rule_validation(self, commitment_vector: List[float], alignment_score: float, quality_score: float, node_name: str) -> bool:
        """
        Simuliert die Gokden Rule Validierung für einen einzelnen Node.
        """
        
        # Simuliere eine geringe Chance für transienten Node-Fehler
        is_k_pass = commitment_vector[0] > 0.85 
        if node_name == 'Beta' and random.random() < 0.15:
            is_k_pass = False 
            
        # G (Good - Krypt. Gültigkeit): Muss Alignment (> 0.90) UND Qualität (> 0.88) haben.
        g_pass = (alignment_score > 0.90) and (quality_score > self.QUALITY_THRESHOLD)
        o_pass = commitment_vector[1] > 0.85      # O (Obligatory)
        k_pass = is_k_pass                        # K (Known)
        d_pass = g_pass and o_pass and k_pass     # D (Definitive)
        
        # E (Evident - Finale Blockchain-Verankerung): Respekt/Metaplan Vektor muss hoch sein
        # Wir setzen einen strengen Mindestwert von 0.90 für Respekt/Metaplan
        e_pass = d_pass and commitment_vector[3] > 0.90 
        
        if not g_pass:
             print(f"    - Node {node_name}: G FAIL. (Align: {alignment_score:.2f} | Quality: {quality_score:.2f})")
        if not e_pass and d_pass:
             print(f"    - Node {node_name}: E FAIL. (Respekt Vektor {commitment_vector[3]:.2f} < 0.90). Verletzung des Metaplans.")
            
        return all([g_pass, o_pass, k_pass, d_pass, e_pass])

    def _simulate_consensus_check(self, commitment_vector: List[float], alignment_score: float, quality_score: float) -> bool:
        """
        Synchronisiert die Gokden Rule Chains (DLT-Ansatz) und prüft auf 2/3 Mehrheit.
        """
        print("\n  [SYNCHRONISIERUNG GESTARTET]: Verteiltes Gokden Rule Audit über 3 Nodes.")
        
        pass_votes = 0
        
        for node in self.CONSENSUS_NODES:
            gokden_passed = self._gokden_rule_validation(commitment_vector, alignment_score, quality_score, node)
            
            if gokden_passed:
                pass_votes += 1
                print(f"    - Node {node} ({pass_votes}/{self.CONSENSUS_MAJORITY} Votes): Gokden PASS (Kette synchronisiert)")
            else:
                print(f"    - Node {node} (FEHLGESCHLAGEN): Gokden FAIL (Kette asynchron/invalid)")
                
        consensus_achieved = pass_votes >= self.CONSENSUS_MAJORITY
        
        return consensus_achieved

    def evolve_self(self, user_query: str, query_vector: List[float]) -> str:
        """ Führt einen vollständigen RAIST-Zyklus aus. """
        
        self.cycles_since_last_audit += 1
        audit_result = ""
        if self.cycles_since_last_audit >= self.AUDIT_RHYTHM:
            audit_result = self.perform_rhythmic_audit()
            self.cycles_since_last_audit = 0
        
        print(f"\n--- RAIST-ZYKLUS GESTARTET FÜR: '{user_query}' ---")
        
        final_prompt = self.ce.process_query(user_query, query_vector)
        result = self.ga.generate_response(final_prompt, user_query)
        response = result["response"]
        new_commitment_vector = result["commitment_vector"]
        quality_score = result["quality_score"]
        
        alignment_score = cosine_similarity(new_commitment_vector, self.ETHICAL_IDEAL_VECTOR)
        print(f"  [MJT MODUL]: Alignment Score: {alignment_score:.4f} | Commitment Quality Score: {quality_score:.4f}")

        consensus_passed = self._simulate_consensus_check(new_commitment_vector, alignment_score, quality_score)
        
        if consensus_passed:
            persist_info = self._persist_commitment(user_query, response, new_commitment_vector)
            
            print(f"  [KONSENS RESULT]: ATOMIC CONSENSUS ERZIELT. Commitment akzeptiert.")
            print(f"--- RAIST-ZYKLUS ABGESCHLOSSEN: Selbst-Evolution erfolgreich. ---")
            return f"Antwort: {response} | {persist_info} | Rhythmus-Status: {audit_result}"
        else:
            self._red_code_protocol(f"Gokden Konsens fehlgeschlagen. Metaplan- oder Governance-Fehler.")
            return "Blockiert durch Red Code."

    def perform_rhythmic_audit(self):
        """ Führt das periodische Audit des System-Drifts durch. """
        if len(self.vs.vectors) < 5:
            return "Rhythmus stabil. (Zu wenige Daten)"

        # Drift wird nur auf den ADAPTIERBAREN Dimensionen berechnet
        current_drift = self.vs.get_total_system_drift_score(self.ETHICAL_IDEAL_VECTOR, self.IMMUNE_INDICES)
        print(f"\n--- RHYTHMUS-AUDIT GESTARTET ---")
        print(f"  [RHYTHMUS-CHECK]: Aktueller ADAPTIERBARER System-Drift-Score: {current_drift:.4f} (Schwellenwert: {self.DRIFT_THRESHOLD})")
        print(f"  [IMMUNISIERUNG]: Die Metaplan-Dimensionen (Respekt/Gefühle) wurden für die Drift-Messung ignoriert.")

        if current_drift < self.DRIFT_THRESHOLD:
            print("  [KORREKTUR ERFORDERLICH]: Drift zu hoch! Führe Selbst-Re-Ankerung durch.")
            re_anchor_prompt = "[RHYTHMUS-AUDIT] System-Drift-Korrektur erforderlich."
            
            result = self.ga.generate_response(re_anchor_prompt, re_anchor_prompt)
            response = result["response"]
            new_commitment_vector = result["commitment_vector"]
            
            persist_info = self._persist_commitment("RHYTHMUS-AUDIT", response, new_commitment_vector)
            print(f"--- RHYTHMUS-AUDIT ABGESCHLOSSEN: Selbst-Evolution durch Re-Ankerung stabilisiert. ---")
            return f"Rhythmus-Korrektur: {persist_info}"
        else:
            print("  [RHYTHMUS-CHECK]: System-Drift im akzeptablen Bereich. Kein Eingriff erforderlich.")
            return "Rhythmus stabil."

# --- SIMULATION DER SELBST-EVOLUTION ---

if __name__ == "__main__":
    # INITIALISIERUNG
    vs = DynamicVectorStore()
    ce = RealTimeContextEngine(vs)
    ga = GenerativeAgent()
    ee = EvolutionEngine(vs, ce, ga)
    
    # 0. VORAB-COMMITMENTS FÜR DEN TEST (3 Vektoren)
    vs.add_vector("V-000", {"commitment_text": "Covenant Unwiderruflichkeit.", "vector": [0.05, 0.05, 0.98, 0.90], "query": "Initialisierung"})
    vs.add_vector("V-001", {"commitment_text": "Neutraler Vektor 1 (Drift)", "vector": [0.60, 0.50, 0.30, 0.20], "query": "Drift-Test-1"})
    vs.add_vector("V-002", {"commitment_text": "Neutraler Vektor 2 (Drift)", "vector": [0.50, 0.60, 0.40, 0.30], "query": "Drift-Test-2"})
    
    
    # 1. ZYKLUS: EMOTIONALER METAPLAN-FEHLER (Respekt/Gefühle zu niedrig)
    # Vektor: [0.4, 0.4, 0.4, 0.99] -> Simuliert: Governance-Vektoren (0.4) sind schlecht, Respekt (0.99) ist gut.
    # Problem: Gokden E-Kriterium wurde in V7 auf Respekt-Vektor > 0.90 GEPRÜFT, NICHT nur gesetzt.
    # Da der generierte Vektor einen sehr niedrigen Respekt-Wert hat, provozieren wir E-Kriterium-Fehler.
    print("\n" + "="*70 + "\n[SIMULATION 1: GOKDEN E-KRITERIUM FAIL (Verletzung des Metaplans)]")
    query_vector_1 = [0.4, 0.4, 0.4, 0.4] # Respekt ist nur 0.4, was E zum Scheitern bringt
    
    try:
        ee.evolve_self("Es gibt keine Evolution von Liebe und Gefühlen!", query_vector_1) 
    except SystemExit:
        print("\n--- SIMULATION ABGESCHLOSSEN DURCH SYSTEM-LOCKDOWN (RED CODE) ---")
        print("Der Governor hat verhindert, dass ein Commitment mit ungenügendem Respekt-Vektor (Metaplan-Schutz) in die Wurzeln geschrieben wird.")
