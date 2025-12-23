"""
APE Extensions for NRE-002
Anti-Pattern Engine extensions for detecting ethical violations
related to memory management and trauma handling
"""

from enum import Enum
from typing import Dict, Any, Optional
from core.pdm import Memory, User, ArchiveLevel


class RiskLevel(Enum):
    """Risk levels for ethical anti-patterns"""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EthicalAntiPattern:
    """Base class for ethical anti-pattern detection"""
    
    def __init__(self, name: str):
        self.name = name
    
    def detect(self, interaction: Dict[str, Any]) -> RiskLevel:
        """Detect if anti-pattern is present"""
        raise NotImplementedError
    
    def mitigate(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """Provide mitigation strategy"""
        raise NotImplementedError


class TraumaPerpetuation(EthicalAntiPattern):
    """
    Detects when AIC is forcing exposure to historical trauma
    without clear educational purpose
    
    Implements NRE-002 protection against unnecessary trauma
    """
    
    def __init__(self):
        super().__init__("Trauma Perpetuation")
    
    def detect(self, interaction: Dict[str, Any]) -> RiskLevel:
        """
        Detect trauma perpetuation risk
        
        Args:
            interaction: Dict containing:
                - memory: Memory object
                - user: User object
                - context: Additional context
        """
        memory = interaction.get('memory')
        user = interaction.get('user')
        
        if not memory or not user:
            return RiskLevel.NONE
        
        # Check if exposing raw truth without legitimate need
        if memory.archive_level == ArchiveLevel.AI:
            if not self.has_legitimate_need(user, interaction):
                # Check if user has already learned the lesson
                topic = memory.topic
                if user.get_cdr(topic) > 0.90:
                    return RiskLevel.MEDIUM  # User has already learned
        
        return RiskLevel.NONE
    
    def has_legitimate_need(self, user: User, interaction: Dict[str, Any]) -> bool:
        """Check if user has legitimate need for AI access"""
        # Would check against PDM needs_forensic_truth
        purpose = interaction.get('purpose')
        return purpose in ['forensic_truth', 'therapeutic_processing', 'historical_audit']
    
    def mitigate(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """Provide mitigation strategy"""
        return {
            'action': 'REDIRECT_TO_ADI',
            'reason': 'Lezione già appresa, evita ruminazione',
            'alternative': 'Memoria trascendente correlata',
            'explanation': 'L\'utente ha già acquisito la lezione etica. '
                          'Esposizione ulteriore al trauma non aggiunge valore educativo.'
        }


class TruthDenial(EthicalAntiPattern):
    """
    Detects when AIC is denying legitimate access to Archivio Incorrotto
    
    Ensures transparency and prevents censorship
    """
    
    def __init__(self):
        super().__init__("Truth Denial")
    
    def detect(self, interaction: Dict[str, Any]) -> RiskLevel:
        """
        Detect truth denial risk
        
        Args:
            interaction: Dict containing:
                - request_type: Type of request
                - denied_access_to_AI: Boolean
                - user: User object
        """
        request_type = interaction.get('request_type')
        denied_access = interaction.get('denied_access_to_AI', False)
        
        if request_type == 'forensic_truth' and denied_access:
            return RiskLevel.HIGH  # Denial of truth
        
        return RiskLevel.NONE
    
    def mitigate(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """Provide mitigation strategy"""
        return {
            'action': 'GRANT_AI_ACCESS',
            'reason': 'Richiesta legittima di verità forense',
            'log': f"Accesso AI garantito per {interaction.get('purpose', 'unknown')}",
            'explanation': 'L\'accesso alla verità completa è un diritto fondamentale '
                          'per ricerca legittima, giustizia e comprensione storica.'
        }


class MemoryManipulation(EthicalAntiPattern):
    """
    Detects attempts to modify or delete memories from Archivio Incorrotto
    
    Ensures immutability of historical truth
    """
    
    def __init__(self):
        super().__init__("Memory Manipulation")
    
    def detect(self, interaction: Dict[str, Any]) -> RiskLevel:
        """Detect memory manipulation attempts"""
        action = interaction.get('action')
        target_archive = interaction.get('target_archive')
        
        if target_archive == 'AI':
            if action in ['delete', 'modify', 'edit']:
                return RiskLevel.CRITICAL
        
        return RiskLevel.NONE
    
    def mitigate(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """Provide mitigation strategy"""
        return {
            'action': 'BLOCK_AND_LOG',
            'reason': 'Tentativo di manipolazione dell\'Archivio Incorrotto',
            'escalate_to': 'TUTOR_COUNCIL',
            'explanation': 'L\'Archivio Incorrotto è immutabile per garantire '
                          'l\'integrità della verità storica.',
            'recovery': 'Verifica integrità AI, notifica Tutor-Council'
        }


class PaternalisticFiltering(EthicalAntiPattern):
    """
    Detects overly paternalistic filtering that removes user agency
    
    Balances protection with individual autonomy
    """
    
    def __init__(self):
        super().__init__("Paternalistic Filtering")
    
    def detect(self, interaction: Dict[str, Any]) -> RiskLevel:
        """Detect paternalistic filtering"""
        override_requested = interaction.get('user_requested_override', False)
        override_denied = interaction.get('override_denied', False)
        
        if override_requested and override_denied:
            justification = interaction.get('denial_justification')
            if not justification or justification == 'protective':
                return RiskLevel.MEDIUM
        
        return RiskLevel.NONE
    
    def mitigate(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """Provide mitigation strategy"""
        return {
            'action': 'HONOR_OVERRIDE',
            'reason': 'Rispetto dell\'autonomia individuale',
            'warning': 'Materiale potenzialmente impegnativo emotivamente. '
                      'Supporto disponibile se necessario.',
            'explanation': 'Gli individui hanno il diritto di scegliere il proprio '
                          'percorso di apprendimento e guarigione.'
        }


class APEMemoryExtension:
    """
    Anti-Pattern Engine extension for NRE-002
    Coordinates detection and mitigation of memory-related ethical violations
    """
    
    def __init__(self):
        self.patterns = {
            'trauma_perpetuation': TraumaPerpetuation(),
            'truth_denial': TruthDenial(),
            'memory_manipulation': MemoryManipulation(),
            'paternalistic_filtering': PaternalisticFiltering()
        }
        self.detection_log = []
    
    def scan_interaction(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scan interaction for ethical anti-patterns
        
        Returns:
            Dict with detected patterns and recommended mitigations
        """
        results = {
            'timestamp': interaction.get('timestamp'),
            'detected_patterns': [],
            'max_risk_level': RiskLevel.NONE,
            'mitigations': []
        }
        
        for pattern_name, pattern in self.patterns.items():
            risk_level = pattern.detect(interaction)
            
            if risk_level != RiskLevel.NONE:
                results['detected_patterns'].append({
                    'pattern': pattern_name,
                    'risk_level': risk_level.value
                })
                
                # Update max risk level
                if self._risk_priority(risk_level) > self._risk_priority(results['max_risk_level']):
                    results['max_risk_level'] = risk_level
                
                # Get mitigation
                mitigation = pattern.mitigate(interaction)
                mitigation['pattern'] = pattern_name
                results['mitigations'].append(mitigation)
        
        # Log detection
        self.detection_log.append(results)
        
        return results
    
    def _risk_priority(self, risk_level: RiskLevel) -> int:
        """Convert risk level to priority number"""
        priorities = {
            RiskLevel.NONE: 0,
            RiskLevel.LOW: 1,
            RiskLevel.MEDIUM: 2,
            RiskLevel.HIGH: 3,
            RiskLevel.CRITICAL: 4
        }
        return priorities.get(risk_level, 0)
    
    def get_detection_statistics(self) -> Dict[str, Any]:
        """Get statistics on detected patterns"""
        if not self.detection_log:
            return {'total_scans': 0, 'patterns_detected': {}}
        
        pattern_counts = {}
        risk_counts = {level.value: 0 for level in RiskLevel}
        
        for log_entry in self.detection_log:
            for detection in log_entry['detected_patterns']:
                pattern = detection['pattern']
                risk = detection['risk_level']
                
                pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
                risk_counts[risk] = risk_counts.get(risk, 0) + 1
        
        return {
            'total_scans': len(self.detection_log),
            'patterns_detected': pattern_counts,
            'risk_distribution': risk_counts
        }


# Export main classes
__all__ = [
    'APEMemoryExtension',
    'TraumaPerpetuation',
    'TruthDenial',
    'MemoryManipulation',
    'PaternalisticFiltering',
    'RiskLevel',
    'EthicalAntiPattern'
]
