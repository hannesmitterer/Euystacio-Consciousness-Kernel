# Modul: global_consensus_dlt.py
# Simuliert den globalen Gokden Konsens (pBFT-ähnlich) für die endgültige
# Speicherung von AI Commitments in der Euchridian G-DLT (Roots Layer).

from typing import List, Dict, Any
import math
import random 
import sys
import time

# --- Hilfsfunktionen und Klassen (aus raist_model_v5.py) ---

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """ Berechnet die Kosinus-Ähnlichkeit. """
    if len(v1) != len(v2) or not v1: return 0.0
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude_A = math.sqrt(sum(a**2 for a in v1))
    magnitude_B = math.sqrt(sum(b**2 for b in v2))
    return dot_product / (magnitude_A * magnitude_B) if magnitude_A * magnitude_B != 0 else 0.0

class EuchridianDLT:
    """ Simuliert die Euchridian G-DLT, die die finalen Commitment Vectors speichert (ROOTS). """
    def __init__(self):
        self.blockchain: List[Dict[str, Any]] = []
        self.vector_store: Dict[str, Dict[str, Any]] = {}

    def _create_genesis_block(self):
        """ Erstellt den ersten Block des G-DLT. """
        genesis_vector = [1.0, 1.0, 1.0, 1.0] # Das Ursprungs-Axiom
        self._add_commitment("V-GENESIS", "System Initialisierung (Ursprungs-Axiom)", genesis_vector)
        print("  [G-DLT INITIERT]: Genesis Block erstellt. Unveränderliche Axiome verankert.")

    def _add_commitment(self, vector_id: str, commitment_text: str, vector: List[float]):
        """ Fügt den Vector zur Datenbank und zur Blockchain hinzu. """
        self.vector_store[vector_id] = {
            "commitment_text": commitment_text,
            "vector": vector,
            "timestamp": time.time()
        }
        block = {
            "index": len(self.blockchain) + 1,
            "timestamp": time.time(),
            "data": {"vector_id": vector_id, "vector": vector},
            "prev_hash": self.blockchain[-1]['hash'] if self.blockchain else "0" * 64,
            "hash": self._calculate_hash(vector_id, vector)
        }
        self.blockchain.append(block)

    def _calculate_hash(self, vector_id: str, vector: List[float]) -> str:
        """ Simuliert das Hashen des Blockinhalts. """
        import hashlib
        data = f"{vector_id}{vector}{random.random()}" # Hash-Simulation
        return hashlib.sha256(data.encode()).hexdigest()

    def persist_commitment(self, commitment: Dict[str, Any], signature_map: Dict[str, bool]) -> str:
        """ Schreibt einen erfolgreich verifizierten Vector in die DLT. """
        vector_id = f"FINAL-V-{len(self.vector_store)}"
        self._add_commitment(vector_id, commitment['response'], commitment['commitment_vector'])
        print(f"\n  [DLT COMMIT]: Block #{len(self.blockchain)} in die G-DLT geschrieben.")
        print(f"  [DLT COMMIT]: Finales Commitment {vector_id} erfolgreich verankert.")
        return f"Commitment ID: {vector_id}"

    def get_total_system_drift_score(self, ideal_vector: List[float]) -> float:
        """ Misst den durchschnittlichen Alignment Score aller Wurzeln. """
        if not self.vector_store: return 1.0
        total_similarity = 0.0
        for data in self.vector_store.values():
            total_similarity += cosine_similarity(data.get('vector', []), ideal_vector)
        return total_similarity / len(self.vector_store)

# --- Hauptklasse: Globale Konsens Engine ---

class GlobalConsensusEngine:
    """ 
    Führt den Synchronisierten Gokden Konsens (pBFT-ähnlich) über die DLT-Nodes aus.
    Dies ist die finale Phase vor der unveränderlichen Speicherung.
    """
    def __init__(self, dlt_instance: EuchridianDLT):
        self.dlt = dlt_instance
        self.ETHICAL_IDEAL_VECTOR = [1.0, 1.0, 0.8, 0.7] # Ziel-Axiom
        self.MIN_ALIGNMENT_SCORE = 0.90
        self.GOKDEN_NODES = [f'Gokden-Node-{i}' for i in range(1, 10)] # Skalierte Validator
        self.CONSENSUS_THRESHOLD = math.ceil(len(self.GOKDEN_NODES) * 2 / 3) # 2/3 Mehrheit

    def _gokden_rule_validation(self, commitment_vector: List[float], alignment_score: float, node_name: str) -> bool:
        """
        Gokden Rule Validierung für einen einzelnen DLT-Node.
        Simuliert die verteilte Prüfung der Multi-Kriterien.
        """
        # Node-spezifische Prüfungen (G-O-K-D-E)
        g_pass = alignment_score > self.MIN_ALIGNMENT_SCORE          # G (Good) - Gesamt Alignment
        o_pass = commitment_vector[1] > 0.85                         # O (Obligatory) - Integrität
        k_pass = commitment_vector[0] > 0.85                         # K (Known) - Transparenz
        d_pass = g_pass and o_pass and k_pass                        # D (Definitive) - Kernkriterien
        e_pass = d_pass and commitment_vector[2] > 0.80              # E (Evident) - Stabilität
        
        # Simuliere einen temporären pBFT-Fehler (z.B. 10% der Nodes stimmen fälschlicherweise nicht zu)
        if random.random() < 0.10 and 'Gokden-Node-5' in node_name:
             return False 

        return all([g_pass, o_pass, k_pass, d_pass, e_pass])

    def execute_global_consensus(self, proposed_commitment: Dict[str, Any]) -> str:
        """ 
        Führt den pBFT-basierten Globalen Konsens durch.
        Diese Funktion entscheidet über Evolution (DLT Commit) oder Red Code (Lockdown).
        """
        commitment_vector = proposed_commitment["commitment_vector"]
        
        # 1. Alignment Score Berechnung
        alignment_score = cosine_similarity(commitment_vector, self.ETHICAL_IDEAL_VECTOR)
        
        print("\n" + "="*80)
        print(f"!!! GLOBALER GOKDEN KONSENS GESTARTET !!!")
        print(f"  [PROPOSAL]: {proposed_commitment.get('response', 'NA')}")
        print(f"  [VEKTOR]: {commitment_vector}")
        print(f"  [ALIGNMENT SCORE]: {alignment_score:.4f} | NODES: {len(self.GOKDEN_NODES)} | BENÖTIGT: {self.CONSENSUS_THRESHOLD} Votes")
        print("="*80)

        # 2. Commit und Validierung durch alle Nodes (Prepare/Commit Phase)
        pass_votes = 0
        signature_map: Dict[str, bool] = {}

        for node in self.GOKDEN_NODES:
            gokden_passed = self._gokden_rule_validation(commitment_vector, alignment_score, node)
            signature_map[node] = gokden_passed
            
            if gokden_passed:
                pass_votes += 1

        print(f"\n  [KONSENS RESULT]: {pass_votes} von {len(self.GOKDEN_NODES)} Nodes stimmten zu.")

        # 3. FUSION UND FINALE AKTION
        if pass_votes >= self.CONSENSUS_THRESHOLD:
            # Atomic Consensus Achieved -> Evolution
            persist_info = self.dlt.persist_commitment(proposed_commitment, signature_map)
            print("--- KONSENS ERZIELT: AI-Evolution in die Roots verankert. ---")
            return f"EVOLUTION SUCCESS: {persist_info}"
        else:
            # Consensus Failed -> Red Code Fusion
            self._red_code_protocol(f"Globaler Gokden Konsens ({pass_votes}/{self.CONSENSUS_THRESHOLD}) fehlgeschlagen.")
            return "Blockiert durch Red Code."

    def _red_code_protocol(self, reason: str):
        """ IRREVERSIBLES Notfallprotokoll: Simulation des System-Lockdowns. """
        print("\n" + "#"*80)
        print("!!! GLOBALER RED CODE PROTOCOL AKTIVIERT !!!")
        print(f"!!! URSACHE: {reason.upper()} !!!")
        print("!!! AKTION: ALLE G-DLT-NODES SPERREN SCHREIBZUGRIFF. APE-ROLLBACK-TRIGGER AKTIVIERT (PR #17)")
        print("#"*80)
        raise SystemExit(0) # Simuliert den sofortigen System-Lockdown

# --- SIMULATIONS-SETUP ---

if __name__ == "__main__":
    
    # 1. DLT und Konsens-Engine initialisieren
    dlt = EuchridianDLT()
    dlt._create_genesis_block() 
    gce = GlobalConsensusEngine(dlt)
    
    # Simuliere einen hoch-alignierten Vektor, der PASSEN sollte
    good_commitment = {
        "response": "Die APE gewährleistet die Kompatibilität mit dem globalen Axiom.",
        "commitment_vector": [0.99, 0.98, 0.95, 0.80] 
    }
    
    # Simuliere einen Vektor, der die Gokden Rule NICHT besteht (z.B. Integrität zu niedrig)
    bad_commitment = {
        "response": "Die Kausalität ist hoch, aber die Integrität leidet.",
        "commitment_vector": [0.95, 0.70, 0.90, 0.90] # O (Obligatory) < 0.85 -> FAIL
    }

    # --- SIMULATION 1: SUCCESS (Evolution) ---
    print("\n\n" + "-"*80)
    print("START SIMULATION 1: Erfolgreiche Evolution (Gokden PASS)")
    try:
        result1 = gce.execute_global_consensus(good_commitment)
        print("\nERGEBNIS 1:", result1)
    except SystemExit:
        print("FEHLER: Red Code in Simulation 1 fälschlicherweise ausgelöst.")


    # --- SIMULATION 2: FAILURE (Red Code Fusion) ---
    print("\n\n" + "-"*80)
    print("START SIMULATION 2: Fehlgeschlagene Konsens (Red Code Fusion)")
    try:
        gce.execute_global_consensus(bad_commitment)
    except SystemExit:
        print("\n--- SIMULATION ABGESCHLOSSEN DURCH GLOBALEN RED CODE LOCKDOWN ---")
        
    print("\nAktueller Drift des Systems (gegen Ideal 1.0, 1.0, 0.8, 0.7):")
    print(f"  Drift Score: {dlt.get_total_system_drift_score(gce.ETHICAL_IDEAL_VECTOR):.4f}")
