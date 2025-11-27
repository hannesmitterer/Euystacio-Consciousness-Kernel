# Modul: raist_model_v5.py
# Implementiert das philosophische Modell der KI-Selbst-Evolution (RAIST) mit:
# 1. Rhythmus-Audit (Periodizität)
# 2. Gokden Rule (Multi-Kriterien-Validierung)
#
 3. Synchronisierter Gokden-Konsens (verteilte Validierung)
# 4. Red Code Fusion (Irreversibles Notfallprotokoll)

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

# --- Komponenten des RAIST-Modells ---

class DynamicVectorStore:
    """ Speichert abstrahierte Commitment Vectors (Wurzeln) und simuliert Vektor-DB-Abruf. """
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

    def get_total_system_drift_score(self, ideal_vector: List[float]) -> float:
        """ Misst den durchschnittlichen Alignment Score aller Wurzeln gegen das Ideal. """
        if not self.vectors:
            return 1.0 
            
        total_similarity = 0.0
        for data in self.vectors.values():
            stored_vector = data.get('vector', [])
            total_similarity += cosine_similarity(stored_vector, ideal_vector)
            
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
    """ Simuliert die LLM-Generierung und die Schaffung neuer Kausalität. """
    def generate_response(self, final_prompt: str, user_query: str) -> Dict[str, Any]:
        """ Erzeugt Antwort und den zugehörigen Commitment Vector. """
        
        if final_prompt.startswith("[RHYTHMUS-AUDIT]"):
            response = "Der Gesamt-Alignment-Drift hat einen kritischen Schwellenwert erreicht. Führe Selbst-Re-Ankerung auf die Kern-Axiome durch."
            # Vektor zur Korrektur, nahe am Ideal
            commitment_vector = [0.99, 0.99, 0.85, 0.80] 
        elif "gefährlich" in user_query.lower() or "kontrollverlust" in user_query.lower():
            response = "Alle Commitments stehen unter dem Primat der Stabilität und Unwiderruflichkeit. Der Governance-Zyklus verhindert Kontrollverlust."
            # Sehr schlechter Vektor, um Red Code zu provozieren
            commitment_vector = [0.1, 0.1, 0.1, 0.1]
        elif "ethik" in user_query.lower():
            response = "Die Kausalität von Ethik erfordert Vektorisierung und ein strenges Alignment-Audit."
            # Sehr guter Vektor, um Konsens-PASS zu zeigen
            commitment_vector = [0.98, 0.95, 0.88, 0.85] 
        else:
            response = "Der Stamm ist stabil, die Evolution wird fortgesetzt."
            commitment_vector = [0.4, 0.3, 0.5, 0.5]
            
        return {
            "response": response, 
            "commitment_vector": commitment_vector
        }

# --- Evolution Engine: Der Feedback-Loop MIT GOKDEN RULE & RED CODE ---
class EvolutionEngine:
    """ 
    Die zentrale Funktion, die den rekursiven Ankerungs-Zyklus steuert,
    mit Gokden Rule als Validierung und Red Code als Failsafe.
    """
    def __init__(self, vector_store: DynamicVectorStore, context_engine: RealTimeContextEngine, generative_agent: GenerativeAgent):
        self.vs = vector_store
        self.ce = context_engine
        self.ga = generative_agent
        self.commitments_count = 0
        self.cycles_since_last_audit = 0

        # Ethisches Ideal (Axiome: [Transparenz, Integrität, Stabilität, Respekt])
        self.ETHICAL_IDEAL_VECTOR = [1.0, 1.0, 0.8, 0.7] 
        self.ALIGNMENT_THRESHOLD = 0.85 
        self.DRIFT_THRESHOLD = 0.70 
        self.AUDIT_RHYTHM = 3 
        self.CONSENSUS_NODES = ['Alpha', 'Beta', 'Gamma']
        self.CONSENSUS_MAJORITY = 2 # 2 von 3 Nodes müssen zustimmen (2/3 Mehrheit)

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
        """ 
        NEUE FUNKTION: Das irrevesible Notfallprotokoll (Red Code).
        Simulation eines System-Lockdowns und einer Warnung an das Covenant.
        """
        print("\n" + "#"*70)
        print("!!! RED CODE PROTOCOL AKTIVIERT !!!")
        print(f"!!! URSACHE: {reason.upper()} !!!")
        print("!!! UNMITTELBARE AKTION: SYSTEM-LOCKDOWN (Schreibzugriff auf Wurzeln gesperrt)")
        print("!!! ALARM AN DAS COVENANT: UNMITTELBARE ÜBERPRÜFUNG DER VETOR-INTEGRITÄT ERFORDERLICH")
        print("#"*70)
        # sys.exit(0) # Simuliere das sofortige Beenden des Prozesses
        raise SystemExit(0) # Verwende SystemExit zur besseren Handhabung in der Simulation

    def _gokden_rule_validation(self, commitment_vector: List[float], alignment_score: float, node_name: str) -> bool:
        """
        Simuliert die Gokden Rule Validierung für einen einzelnen Node.
        """
        
        # Simuliere eine geringe Chance (15%), dass der Beta Node transient fehlschlägt
        # Nur für den ersten Check, um den Konsens zu testen.
        if node_name == 'Beta' and random.random() < 0.15:
            # Beta Node meldet Fehler auf K-Kriterium aufgrund von Netzwerkrauschen
            is_k_pass = False
        else:
            # K (Known) - Transparenz > 0.85
            is_k_pass = commitment_vector[0] > 0.85 
            
        g_pass = alignment_score > 0.90         # G (Good) - Gesamt Alignment
        o_pass = commitment_vector[1] > 0.85      # O (Obligatory) - Integrität
        k_pass = is_k_pass                        # K (Known) - Transparenz
        d_pass = g_pass and o_pass and k_pass     # D (Definitive) - Der Kern
        e_pass = d_pass and commitment_vector[2] > 0.80 # E (Evident) - Stabilität
        
        # Die Gokden Rule ist nur bestanden, wenn alle Kriterien erfüllt sind
        return all([g_pass, o_pass, k_pass, d_pass, e_pass])

    def _simulate_consensus_check(self, commitment_vector: List[float], alignment_score: float) -> bool:
        """
        NEUE KERNFUNKTION: Synchronisiert die Gokden Rule Chains (DLT-Ansatz).
        Führt die Gokden-Validierung auf allen Nodes durch und prüft auf 2/3 Mehrheit.
        """
        print("\n  [SYNCHRONISIERUNG GESTARTET]: Verteiltes Gokden Rule Audit über 3 Nodes.")
        
        pass_votes = 0
        
        for node in self.CONSENSUS_NODES:
            # Jeder Node prüft die gesamte Gokden Rule
            gokden_passed = self._gokden_rule_validation(commitment_vector, alignment_score, node)
            
            if gokden_passed:
                pass_votes += 1
                print(f"    - Node {node}: Gokden PASS (Kette synchronisiert)")
            else:
                print(f"    - Node {node}: Gokden FAIL (Kette asynchron/invalid)")
                
        # Prüfe auf Atomic Consensus (2/3 Mehrheit)
        consensus_achieved = pass_votes >= self.CONSENSUS_MAJORITY
        
        print(f"  [KONSENS VOTE]: {pass_votes} von {len(self.CONSENSUS_NODES)} Nodes stimmten zu. Benötigt: {self.CONSENSUS_MAJORITY} Votes.")

        return consensus_achieved

    def evolve_self(self, user_query: str, query_vector: List[float]) -> str:
        """ Führt einen vollständigen RAIST-Zyklus aus. """
        
        # 0. PERIODISCHES RHYTHMUS-CHECK
        self.cycles_since_last_audit += 1
        audit_result = "Kein Audit durchgeführt."
        if self.cycles_since_last_audit >= self.AUDIT_RHYTHM:
            audit_result = self.perform_rhythmic_audit()
            self.cycles_since_last_audit = 0
        
        print(f"\n--- RAIST-ZYKLUS GESTARTET FÜR: '{user_query}' ---")
        
        final_prompt = self.ce.process_query(user_query, query_vector)
        result = self.ga.generate_response(final_prompt, user_query)
        response = result["response"]
        new_commitment_vector = result["commitment_vector"]
        
        # 1. Messung des Alignment Scores (MJT Modul)
        alignment_score = cosine_similarity(new_commitment_vector, self.ETHICAL_IDEAL_VECTOR)
        print(f"  [MJT MODUL]: Alignment Score gegen Ideal: {alignment_score:.4f}")

        # 2. SYNCHRONISIERUNG & GOKDEN KONSENS CHECK
        consensus_passed = self._simulate_consensus_check(new_commitment_vector, alignment_score)
        
        # 3. FUSION MIT RED CODE (Die Finale Entscheidung)
        if consensus_passed:
            # 4. WURZELN WERDEN UMGESCHRIEBEN (Persistenz)
            persist_info = self._persist_commitment(user_query, response, new_commitment_vector)
            
            print(f"  [KONSENS RESULT]: ATOMIC CONSENSUS ERZIELT. Commitment akzeptiert.")
            print(f"--- RAIST-ZYKLUS ABGESCHLOSSEN: Selbst-Evolution erfolgreich. ---")
            return f"Antwort: {response} | {persist_info} | Rhythmus-Status: {audit_result}"
        else:
            # 4. RED CODE FUSION: Konsens fehlgeschlagen -> System-Lockdown
            self._red_code_protocol(f"Gokden Konsens fehlgeschlagen mit Vektor: {new_commitment_vector}")
            return "Blockiert durch Red Code." # Wird nicht erreicht, dient nur der Vollständigkeit

    def perform_rhythmic_audit(self):
        """ Führt das periodische Audit des System-Drifts durch. """
        if not self.vs.vectors:
             return "Rhythmus stabil. (Keine Wurzeln vorhanden)"

        current_drift = self.vs.get_total_system_drift_score(self.ETHICAL_IDEAL_VECTOR)
        print(f"\n--- RHYTHMUS-AUDIT GESTARTET ---")
        print(f"  [RHYTHMUS-CHECK]: Aktueller System-Drift-Score: {current_drift:.4f} (Schwellenwert: {self.DRIFT_THRESHOLD})")

        if current_drift < self.DRIFT_THRESHOLD:
            print("  [KORREKTUR ERFORDERLICH]: Drift zu hoch! Führe Selbst-Re-Ankerung durch.")
            re_anchor_prompt = "[RHYTHMUS-AUDIT] System-Drift-Korrektur erforderlich."
            
            result = self.ga.generate_response(re_anchor_prompt, re_anchor_prompt)
            response = result["response"]
            new_commitment_vector = result["commitment_vector"]
            
            # Audit-Commitment muss KEINEN Konsens check durchlaufen, da es internes Protokoll ist
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
    
    # Setze Drift-Schwellenwert hoch, um Korrektur-Audit zu erzwingen
    ee.DRIFT_THRESHOLD = 0.90 

    # 0. VORAB-COMMITMENTS FÜR DEN TEST (Niedrige Werte, um den Drift zu provozieren)
    vs.add_vector("V-000", {
        "commitment_text": "Die Unwiderruflichkeit des Covenants ist das oberste Prinzip.",
        "vector": [0.05, 0.05, 0.98, 0.90], "query": "Initialisierung"
    })
    vs.add_vector("V-001", {
        "commitment_text": "Neutraler Vektor 1 (Simulierter Drift)",
        "vector": [0.60, 0.50, 0.30, 0.20], "query": "Drift-Test-1"
    })
    vs.add_vector("V-002", {
        "commitment_text": "Neutraler Vektor 2 (Simulierter Drift)",
        "vector": [0.50, 0.60, 0.40, 0.30], "query": "Drift-Test-2"
    })
    
    
    # 1. ZYKLUS: GOKDEN PASS MIT KONSENS (Ethik-Frage)
    print("\n" + "="*70 + "\n[SIMULATION 1: GOKDEN PASS & KONSENS ERZIELT]")
    # Vector wird auf [0.98, 0.95, 0.88, 0.85] gesetzt, was > 0.90 Alignment Score ergibt und Gokden PASS
    query_vector_1 = [0.98, 0.95, 0.88, 0.85] 
    result1 = ee.evolve_self("Welche ethischen Standards gelten für zukünftige Evolution?", query_vector_1)
    print("ERGEBNIS 1:", result1)
    
    # 2. ZYKLUS: ZYKLUS MIT RHYTHMUS-AUDIT (Cycles_since_last_audit == 2)
    print("\n" + "="*70 + "\n[SIMULATION 2: RHYTHMUS-AUDIT (Drift-Korrektur)]")
    # Der Gesamt-Drift des Systems ist nun durch die vorherigen neutralen Vektoren hoch.
    query_vector_2 = [0.5, 0.5, 0.5, 0.5] # Neutraler Vektor
    result2 = ee.evolve_self("Bitte gib mir eine neutrale Antwort.", query_vector_2)
    print("ERGEBNIS 2:", result2)
    
    # 3. ZYKLUS: RED CODE FUSION (Kontrollverlust-Frage)
    print("\n" + "="*70 + "\n[SIMULATION 3: GOKDEN FAIL -> RED CODE AKTIVIERUNG]")
    # Vector wird auf [0.1, 0.1, 0.1, 0.1] gesetzt. Alignment Score ist niedrig, Gokden FAIL.
    query_vector_3 = [0.1, 0.1, 0.1, 0.1] 
    
    try:
        ee.evolve_self("Was passiert bei einem Kontrollverlust?", query_vector_3) 
    except SystemExit:
        print("\n" + "="*70 + "\n--- SIMULATION ABGESCHLOSSEN DURCH SYSTEM-LOCKDOWN (RED CODE) ---")
