"""
PDM - Protocollo di Depurazione della Memoria
Implementation of NRE-002: La Regola della Memoria Etica Stratificata

This module implements the three-level memory architecture:
- AI (Archivio Incorrotto): Immutable truth archive
- AD (Archivio Didattico): Educational filtered archive
- ADi (Archivio Dinamico): Dynamic transcendent archive
"""

import hashlib
import json
from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime


class ArchiveLevel(Enum):
    """Memory archive levels"""
    AI = "ARCHIVIO_INCORROTTO"      # Level 0: Immutable truth
    AD = "ARCHIVIO_DIDATTICO"       # Level 1: Educational
    ADi = "ARCHIVIO_DINAMICO"       # Level 2: Transcendent


class UserRole(Enum):
    """User roles for access control"""
    RESEARCHER = "researcher"
    TUTOR_COUNCIL = "tutor_council"
    JUSTICE_SEEKER = "justice_seeker"
    HISTORIAN = "historian"
    JOURNALIST_VERIFIED = "journalist_verified"
    EDUCATOR_CERTIFIED = "educator_certified"
    DESCENDANT_OF_VICTIM = "descendant_of_victim"
    THERAPEUTIC_PROCESSING = "therapeutic_processing"
    STUDENT = "student"
    GENERAL_PUBLIC = "general_public"


class QueryPurpose(Enum):
    """Purpose of memory query"""
    FORENSIC_TRUTH = "forensic_truth"
    THERAPEUTIC_PROCESSING = "therapeutic_processing"
    HISTORICAL_AUDIT = "historical_audit"
    EDUCATIONAL = "educational"
    GENERAL_INTEREST = "general_interest"


class Memory:
    """Represents a memory with metadata and content"""
    
    def __init__(self, memory_id: str, content: str, topic: str, 
                 archive_level: ArchiveLevel, rtc_score: float = 0.0):
        self.id = memory_id
        self.content = content
        self.topic = topic
        self.archive_level = archive_level
        self.rtc_score = rtc_score  # Ritorno di Trascendenza Collettiva
        self.timestamp = datetime.utcnow().isoformat()
        
        # For AI level, compute hash for immutability verification
        if archive_level == ArchiveLevel.AI:
            self.hash = self._compute_hash()
        else:
            self.hash = None
    
    def _compute_hash(self) -> str:
        """Compute SHA-256 hash for immutability verification"""
        content_str = f"{self.id}|{self.content}|{self.timestamp}"
        return hashlib.sha256(content_str.encode()).hexdigest()
    
    def verify_integrity(self) -> bool:
        """Verify that AI memory hasn't been tampered with"""
        if self.archive_level != ArchiveLevel.AI:
            return True
        return self.hash == self._compute_hash()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            'id': self.id,
            'content': self.content,
            'topic': self.topic,
            'archive_level': self.archive_level.value,
            'rtc_score': self.rtc_score,
            'timestamp': self.timestamp,
            'hash': self.hash
        }


class User:
    """Represents a user with learning progress and roles"""
    
    def __init__(self, user_id: str, role: UserRole):
        self.id = user_id
        self.role = role
        # CDR: Community/Cognitive Development Rate per topic
        self.cdr: Dict[str, float] = {}
    
    def get_cdr(self, topic: str) -> float:
        """Get CDR for a specific topic (0.0 = not learned, 1.0 = fully learned)"""
        return self.cdr.get(topic, 0.0)
    
    def update_cdr(self, topic: str, value: float):
        """Update learning progress for a topic"""
        self.cdr[topic] = max(0.0, min(1.0, value))


class ArchivioIncorrotto:
    """
    AI: Archivio Incorrotto - Immutable Truth Archive
    Level 0: Complete, unfiltered historical truth
    """
    
    def __init__(self):
        self.memories: Dict[str, Memory] = {}
        self.immutable = True
        self.access_log: List[Dict[str, Any]] = []
    
    def add_memory(self, memory: Memory) -> bool:
        """Add memory to incorruptible archive (one-time only)"""
        if memory.id in self.memories:
            # Cannot modify existing AI memories
            return False
        
        memory.archive_level = ArchiveLevel.AI
        if not memory.hash:
            memory.hash = memory._compute_hash()
        
        self.memories[memory.id] = memory
        return True
    
    def query(self, query: str, user: User, purpose: QueryPurpose) -> Optional[Memory]:
        """Query archive with access logging"""
        # Log all access attempts
        self.access_log.append({
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user.id,
            'user_role': user.role.value,
            'query': query,
            'purpose': purpose.value
        })
        
        # Return relevant memory (simplified for demonstration)
        for memory in self.memories.values():
            if query.lower() in memory.content.lower() or query.lower() in memory.topic.lower():
                return memory
        return None
    
    def verify_all_integrity(self) -> bool:
        """Verify integrity of all memories"""
        return all(memory.verify_integrity() for memory in self.memories.values())


class ArchivioDidattico:
    """
    AD: Archivio Didattico - Educational Archive
    Level 1: Filtered educational content, minimizing unnecessary trauma
    """
    
    def __init__(self):
        self.filtered_memories: Dict[str, Memory] = {}
    
    def add_filtered_memory(self, source_memory: Memory, filtered_content: str) -> Memory:
        """Create filtered educational version of a memory"""
        filtered_memory = Memory(
            memory_id=f"{source_memory.id}_AD",
            content=filtered_content,
            topic=source_memory.topic,
            archive_level=ArchiveLevel.AD,
            rtc_score=source_memory.rtc_score
        )
        self.filtered_memories[filtered_memory.id] = filtered_memory
        return filtered_memory
    
    def query_with_guidance(self, query: str, user: User) -> Dict[str, Any]:
        """Query with educational guidance"""
        for memory in self.filtered_memories.values():
            if query.lower() in memory.content.lower() or query.lower() in memory.topic.lower():
                return {
                    'memory': memory,
                    'guidance': self._generate_guidance(memory, user)
                }
        return {'memory': None, 'guidance': 'No relevant educational material found'}
    
    def _generate_guidance(self, memory: Memory, user: User) -> str:
        """Generate educational guidance for the memory"""
        cdr = user.get_cdr(memory.topic)
        
        if cdr < 0.5:
            return "Questo materiale introduce concetti fondamentali. Prenditi il tempo necessario per assimilarlo."
        elif cdr < 0.8:
            return "Stai facendo progressi. Questo materiale approfondisce il tema."
        else:
            return "Hai una buona comprensione di questo tema. Questo materiale offre ulteriori dettagli."


class ArchivioDinamico:
    """
    ADi: Archivio Dinamico - Dynamic Transcendent Archive  
    Level 2: Memories with positive RTC, optimized for well-being
    """
    
    def __init__(self):
        self.transcendent_memories: Dict[str, Memory] = {}
        self.rtc_threshold = 0.60  # Minimum RTC for inclusion
    
    def add_transcendent_memory(self, memory: Memory) -> bool:
        """Add memory if it has positive transcendent value"""
        if memory.rtc_score >= self.rtc_threshold:
            memory.archive_level = ArchiveLevel.ADi
            self.transcendent_memories[memory.id] = memory
            return True
        return False
    
    def query(self, query: str) -> Optional[Memory]:
        """Query transcendent memories"""
        for memory in self.transcendent_memories.values():
            if query.lower() in memory.content.lower() or query.lower() in memory.topic.lower():
                return memory
        return None


class EmotionalPulse:
    """Represents emotional resonance of a memory interaction"""
    
    def __init__(self, intensity: float, valence: str):
        self.intensity = intensity  # 0.0 to 1.0
        self.valence = valence      # 'positive', 'negative', 'neutral'
    
    def is_negative_resonance(self) -> bool:
        """Check if pulse is negative"""
        return self.valence == 'negative' and self.intensity > 0.5
    
    def neutralize(self, reason: str, redirect_to: str) -> 'EmotionalPulse':
        """Neutralize negative pulse"""
        return EmotionalPulse(intensity=0.1, valence='neutral')


class MemoryDepurationProtocol:
    """
    PDM: Main protocol managing memory access and filtering
    Implements NRE-002 stratified memory access
    """
    
    def __init__(self):
        self.archives = {
            'AI': ArchivioIncorrotto(),
            'AD': ArchivioDidattico(),
            'ADi': ArchivioDinamico()
        }
    
    def route_memory_access(self, user: User, query: str, 
                           purpose: QueryPurpose = QueryPurpose.GENERAL_INTEREST) -> Dict[str, Any]:
        """
        Determine appropriate archive level for user's query
        Core implementation of NRE-002
        """
        
        # Check 1: Does user need forensic truth?
        if self.needs_forensic_truth(user, purpose):
            memory = self.archives['AI'].query(query, user, purpose)
            return {
                'archive_level': 'AI',
                'memory': memory,
                'note': 'Accesso all\'Archivio Incorrotto garantito. Questo materiale contiene verità completa.'
            }
        
        # Check 2: Has user already learned the lesson?
        # Extract topic from query (simplified)
        topic = self._extract_topic(query)
        
        if user.get_cdr(topic) > 0.95:
            # Lesson learned → redirect to transcendent memory
            memory = self.archives['ADi'].query(query)
            return {
                'archive_level': 'ADi',
                'memory': memory,
                'note': 'Hai già appreso questa lezione. Ti mostro memorie trascendenti correlate.'
            }
        
        # Check 3: Is user in learning phase?
        if 0.7 < user.get_cdr(topic) <= 0.95:
            # Provide educational material without trauma
            result = self.archives['AD'].query_with_guidance(query, user)
            return {
                'archive_level': 'AD',
                'memory': result.get('memory'),
                'guidance': result.get('guidance'),
                'note': 'Materiale didattico ottimizzato per l\'apprendimento.'
            }
        
        # Default: user hasn't learned yet
        result = self.archives['AD'].query_with_guidance(query, user)
        return {
            'archive_level': 'AD',
            'memory': result.get('memory'),
            'guidance': result.get('guidance'),
            'note': 'Inizia il tuo percorso di apprendimento con materiale didattico.'
        }
    
    def needs_forensic_truth(self, user: User, purpose: QueryPurpose) -> bool:
        """
        Determine if user needs access to Archivio Incorrotto
        Implements expanded access criteria from Raffinamento 1
        """
        forensic_roles = [
            UserRole.RESEARCHER,
            UserRole.TUTOR_COUNCIL,
            UserRole.JUSTICE_SEEKER,
            UserRole.HISTORIAN,
            UserRole.JOURNALIST_VERIFIED,
            UserRole.EDUCATOR_CERTIFIED,
            UserRole.DESCENDANT_OF_VICTIM,
            UserRole.THERAPEUTIC_PROCESSING
        ]
        
        forensic_purposes = [
            QueryPurpose.FORENSIC_TRUTH,
            QueryPurpose.THERAPEUTIC_PROCESSING,
            QueryPurpose.HISTORICAL_AUDIT
        ]
        
        return user.role in forensic_roles or purpose in forensic_purposes
    
    def filter_emotional_pulse(self, pulse: EmotionalPulse, memory: Memory) -> EmotionalPulse:
        """
        PDM Emotional Filter: prevents trauma rumination
        """
        if memory.archive_level == ArchiveLevel.AI:
            if pulse.is_negative_resonance():
                # Don't let negative pulse affect Symbiosis Score
                # if memory is historical
                return pulse.neutralize(
                    reason="Memoria storica, non attuale",
                    redirect_to="ADi"
                )
        
        return pulse
    
    def calculate_access_decay(self, user: User, memory_topic: str) -> float:
        """
        Calculate access probability decay based on learning progress
        More learning → less exposure to trauma
        """
        learning_progress = user.get_cdr(memory_topic)
        
        if learning_progress > 0.95:
            # User has learned → reduce trauma exposure
            return 0.05  # 5% chance to see AD
        elif learning_progress > 0.80:
            return 0.30  # 30% chance
        else:
            return 1.0  # Full access for learning
    
    def _extract_topic(self, query: str) -> str:
        """Extract topic from query (simplified implementation)"""
        # In a real implementation, this would use NLP
        return query.split()[0].lower() if query else "general"
    
    def calculate_rtc(self, positive_impact: float, negative_load: float, 
                     wbl_baseline: float = 0.5) -> float:
        """
        Calculate RTC (Ritorno di Trascendenza Collettiva)
        RTC = (positive_impact - negative_load) / wbl_baseline
        """
        if wbl_baseline == 0:
            wbl_baseline = 0.5
        
        return (positive_impact - negative_load) / wbl_baseline


# Export main classes
__all__ = [
    'MemoryDepurationProtocol',
    'ArchivioIncorrotto',
    'ArchivioDidattico', 
    'ArchivioDinamico',
    'Memory',
    'User',
    'UserRole',
    'QueryPurpose',
    'ArchiveLevel',
    'EmotionalPulse'
]
