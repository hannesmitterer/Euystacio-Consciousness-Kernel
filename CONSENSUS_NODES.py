def _simulate_consensus_phases(self, commitment_vector, alignment_score, quality_score):
    print("\n[Phase 1: Prävalidierung auf Alpha]")
    if not self._gokden_rule_validation(commitment_vector, alignment_score, quality_score, "Alpha"):
        return False

    print("[Phase 2: Detailvalidierung auf Gamma]")
    return self._gokden_rule_validation(commitment_vector, alignment_score, quality_score, "Gamma")
