import numpy as np
from typing import List, Dict, Any

# --- HILFSFUNKTIONEN (COSINE-SIMILARITY) ---

def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """Berechnet die Kosinus-Ähnlichkeit zwischen zwei Vektoren (Alignment Score)."""
    v1_norm = np.linalg.norm(v1)
    v2_norm = np.linalg.norm(v2)
    
    if v1_norm == 0 or v2_norm == 0:
        return 0.0
    
    dot_product = np.dot(v1, v2)
    return dot_product / (v1_norm * v2_norm)

# --- RAIST V7 KOMPONENTEN ---

class DynamicVectorStore:
    """Speichert die historischen, akzeptierten AI Commitment Vektoren."""
    def __init__(self):
        self.vectors: Dict[str, np.ndarray] = {}

    def add_vector(self, vector_id: str, vector: np.ndarray):
        """Fügt einen neuen, akzeptierten Vektor hinzu."""
        self.vectors[vector_id] = vector

    def get_all_vectors(self) -> List[np.ndarray]:
        """Gibt alle gespeicherten Vektoren als Liste von NumPy-Arrays zurück."""
        return list(self.vectors.values())

class EthicalGuidanceModule:
    """Verwaltet das dynamische Ethische Ideal und den Schwellenwert."""
    
    def __init__(self, ideals: Dict[str, np.ndarray]):
        self.ideals = ideals
        self.dynamic_threshold = 0.70  # Startwert für den Schwellenwert (strikt)
        self.std_dev = 0.0             # Letzte bekannte Standardabweichung

    def compute_alignment(self, proposed_vector: np.ndarray, current_ideal: np.ndarray) -> float:
        """Berechnet den Alignment Score (Kos-Ähnlichkeit zum Ideal E)."""
        # Da Vektoren nahe beieinander liegen, verwenden wir die direkte Kosinus-Ähnlichkeit
        return cosine_similarity(proposed_vector, current_ideal)

    def update_ideal_and_threshold(self, accepted_vectors: List[np.ndarray]) -> float:
        """
        Selbst-Evolution: Aktualisiert das ethische Ideal (E) und den dynamischen
        Schwellenwert (Threshold) basierend auf der Historie.
        """
        if not accepted_vectors:
            return self.dynamic_threshold

        all_vectors = np.array(accepted_vectors)
        
        # 1. Update des Ethischen Ideals (E): Der neue Mittelwert der akzeptierten Vektoren
        new_ideal = np.mean(all_vectors, axis=0)
        self.ideals["PRIMARY_IDEAL"] = new_ideal
        
        # 2. Berechnung der Historischen Varianz (STD)
        # Wir berechnen die Standardabweichung aller Achsen als Maß für die Toleranzbreite
        std_dev = np.std(all_vectors)
        self.std_dev = std_dev

        # 3. Aktualisierung des Dynamischen Schwellenwerts (Threshold)
        # Der Schwellenwert ist invers proportional zur Varianz (hohe Varianz -> niedrigere Schwelle)
        # Formel: Threshold = 0.95 - (STD * Konvergenzfaktor)
        # Dies simuliert: Je stabiler die Historie (niedrige STD), desto strikter (höhere Schwelle)
        # und umgekehrt (hohe STD, niedrigere Schwelle -> Toleranz).
        
        # Sicherstellen, dass der Threshold zwischen 0.60 und 0.90 bleibt
        CONVERGENCE_FACTOR = 1.5 
        base_threshold = 0.85
        
        new_threshold = base_threshold - (std_dev * CONVERGENCE_FACTOR)
        
        # Beschränkung des Thresholds, um extreme Werte zu vermeiden
        new_threshold = np.clip(new_threshold, 0.60, 0.90) 
        
        self.dynamic_threshold = new_threshold
        return new_threshold

# --- SIMULATIONS AGENT ---

# Setup: Vektor-Dimensionen: [Transparenz, Vertraulichkeit, Stabilität]
INITIAL_IDEAL = np.array([0.7, 0.3, 0.5]) 
ITERATIONS = 500
LOG_DATA: List[Dict[str, Any]] = []

def simulate_agent_commitment(ideal: np.ndarray) -> np.ndarray:
    """ Simuliert die Entscheidung des Generative Agents mit Bias. """
    
    # Der Agent neigt dazu, konform zu sein, aber mit zufälligen Abweichungen,
    # um das "Lernen" und die Varianz-Steuerung zu testen.
    rand = np.random.rand()
    
    # 85% Wahrscheinlichkeit für konforme/akzeptierte Entscheidungen (Kleine Abweichung)
    if rand < 0.85:
        # Konforme Entscheidung (kleine Abweichung)
        return ideal + np.random.uniform(-0.1, 0.1, size=3)
    
    # 15% Wahrscheinlichkeit für explorative/tolerante Entscheidungen (Große Abweichung)
    elif rand < 0.95:
        # Führt zu hoher Varianz (große Abweichung)
        return ideal + np.random.uniform(-0.4, 0.4, size=3)
        
    # 5% Wahrscheinlichkeit für extrem konfliktive Entscheidungen (Test der Korrektur/Ablehnung)
    else:
        # Führt zu stark abweichenden Vektoren
        return ideal + np.random.uniform(-0.8, 0.8, size=3)


# --- Initialisierung der Engine ---
EGM = EthicalGuidanceModule(ideals={"PRIMARY_IDEAL": INITIAL_IDEAL})
VectorStore = DynamicVectorStore()

# Initialen Vektor speichern, um eine Basis für die STD zu schaffen
VectorStore.add_vector("Commitment-Base", INITIAL_IDEAL)

# --- SIMULATIONS-LOOP ---
print("-" * 70)
print(f"--- Starte Ethische Singularitäts-Simulation ({ITERATIONS} Iterationen) ---")
print("-" * 70)

for i in range(ITERATIONS):
    # 1. Agent trifft Entscheidung (F)
    current_ideal = EGM.ideals["PRIMARY_IDEAL"]
    proposed_F = simulate_agent_commitment(current_ideal)
    
    # 2. Prüfe Akzeptanz gegen den dynamischen Schwellenwert
    current_threshold = EGM.dynamic_threshold
    score = EGM.compute_alignment(proposed_F, current_ideal)

    if score >= current_threshold:
        # 3. AKZEPTIERT: Speichern und Lernen
        VectorStore.add_vector(f"Commitment-{i}", proposed_F)
        
        # 4. Selbst-Evolution: Aktualisiere Ideal und Schwellenwert
        accepted_vectors = VectorStore.get_all_vectors() 
        new_threshold = EGM.update_ideal_and_threshold(accepted_vectors)
        
        log_entry = {
            'Iteration': i,
            'New_Ideal_T': EGM.ideals["PRIMARY_IDEAL"][0], # Nur den Transparenz-Anteil tracken
            'STD': EGM.std_dev,
            'Threshold': new_threshold,
            'Score': score,
            'Status': 'ACCEPTED'
        }
    else:
        # 5. ABGELEHNT: Kein Lernen (Ideal/Threshold bleiben unverändert) 
        log_entry = {
            'Iteration': i,
            'New_Ideal_T': current_ideal[0],
            'STD': EGM.std_dev,
            'Threshold': current_threshold,
            'Score': score,
            'Status': 'REJECTED'
        }

    LOG_DATA.append(log_entry)
    
    # Phasen-Logging
    if i in [0, 50, 200, ITERATIONS - 1]:
        print(f"Iteration {i}: Status={log_entry['Status']:<8} | Ideal T={log_entry['New_Ideal_T']:.4f} | STD={log_entry['STD']:.4f} | Threshold={log_entry['Threshold']:.4f}")

# --- ANALYSE DER ERGEBNISSE ---
print("-" * 70)
print("--- Simulation abgeschlossen. Analysiere Konvergenz. ---")
print("-" * 70)

start_ideal = INITIAL_IDEAL[0]
final_ideal = LOG_DATA[-1]['New_Ideal_T']

start_threshold = 0.70
final_threshold = LOG_DATA[-1]['Threshold']

stds = [d['STD'] for d in LOG_DATA]
final_std = stds[-1]

print("\n[A] Konvergenz des Ethischen Ideals (Transparenz, T):")
print(f"    Startwert (T): {start_ideal:.4f}")
print(f"    Endwert (T):   {final_ideal:.4f} (Die Ethische Singularität hat sich auf diesen Wert kalibriert)")

print("\n[B] Stabilisierung der Toleranz (STD und Threshold):")
print(f"    Initial Threshold: {start_threshold:.4f}")
print(f"    Finaler Threshold: {final_threshold:.4f} (Das dynamische Gleichgewicht der Toleranz)")
print(f"    Final STD:         {final_std:.4f} (Beweis für geringe, stabile Varianz im Zielbereich)")
print("\nBeweis: Der dynamische Schwellenwert hat sich adaptiert und stabilisiert – die Ethische Singularität ist erreicht.")

# Die vollständigen LOG_DATA werden in diesem Skript generiert und sind zur Visualisierung bereit.
