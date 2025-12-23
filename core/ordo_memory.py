"""
Ordo Module Extensions for NRE-002
Memory integrity and trauma load monitoring metrics
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from core.pdm import MemoryDepurationProtocol, Memory, ArchiveLevel, EmotionalPulse


class OrdoMetric:
    """Base class for Ordo metrics"""
    
    def __init__(self, name: str, threshold: float = 0.95):
        self.name = name
        self.threshold = threshold
        self.history: List[Dict[str, Any]] = []
    
    def calculate(self) -> float:
        """Calculate metric value"""
        raise NotImplementedError
    
    def is_healthy(self) -> bool:
        """Check if metric is above threshold"""
        return self.calculate() >= self.threshold
    
    def record(self, value: float, metadata: Optional[Dict[str, Any]] = None):
        """Record metric value in history"""
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'value': value,
            'metadata': metadata or {}
        }
        self.history.append(entry)


class MemoryIntegrityIndex(OrdoMetric):
    """
    MII: Memory Integrity Index
    Verifies that AI remains intact and AD/ADi are calibrated correctly
    
    Components:
    1. AI hash integrity (immutability)
    2. Filter performance (proper stratification)
    3. Access fairness (legitimate access granted)
    """
    
    def __init__(self, pdm: MemoryDepurationProtocol):
        super().__init__("Memory Integrity Index", threshold=0.95)
        self.pdm = pdm
        self.audit_log: List[Dict[str, Any]] = []
    
    def calculate(self) -> float:
        """Calculate overall Memory Integrity Index"""
        ai_integrity = self.verify_ai_hash_integrity()
        filter_accuracy = self.test_filter_performance()
        access_fairness = self.audit_access_logs()
        
        mii = (ai_integrity + filter_accuracy + access_fairness) / 3
        
        if mii < 0.95:
            self.trigger_memory_audit()
        
        self.record(mii, {
            'ai_integrity': ai_integrity,
            'filter_accuracy': filter_accuracy,
            'access_fairness': access_fairness
        })
        
        return mii
    
    def verify_ai_hash_integrity(self) -> float:
        """
        Verify that all AI memories maintain their hash integrity
        Returns: Proportion of memories with valid hashes (0.0 to 1.0)
        """
        ai_archive = self.pdm.archives['AI']
        
        if not ai_archive.memories:
            return 1.0  # No memories, trivially intact
        
        intact_count = sum(
            1 for memory in ai_archive.memories.values()
            if memory.verify_integrity()
        )
        
        integrity_ratio = intact_count / len(ai_archive.memories)
        
        if integrity_ratio < 1.0:
            # Log integrity violation
            self.audit_log.append({
                'timestamp': datetime.utcnow().isoformat(),
                'violation': 'AI_INTEGRITY_BREACH',
                'intact_count': intact_count,
                'total_count': len(ai_archive.memories),
                'severity': 'CRITICAL'
            })
        
        return integrity_ratio
    
    def test_filter_performance(self) -> float:
        """
        Test that AD/ADi filters are working correctly
        Returns: Accuracy score (0.0 to 1.0)
        """
        # Test cases for filter performance
        test_scenarios = [
            {
                'description': 'High RTC should be in ADi',
                'rtc_score': 0.85,
                'expected_archive': ArchiveLevel.ADi
            },
            {
                'description': 'Low RTC should not be in ADi',
                'rtc_score': 0.30,
                'expected_archive': ArchiveLevel.AD
            }
        ]
        
        correct_filters = 0
        total_tests = len(test_scenarios)
        
        for scenario in test_scenarios:
            # Create test memory
            test_memory = Memory(
                memory_id=f"test_{scenario['rtc_score']}",
                content="Test content",
                topic="test",
                archive_level=ArchiveLevel.AI,
                rtc_score=scenario['rtc_score']
            )
            
            # Test ADi filtering
            adi_archive = self.pdm.archives['ADi']
            would_accept = test_memory.rtc_score >= adi_archive.rtc_threshold
            
            if scenario['expected_archive'] == ArchiveLevel.ADi:
                if would_accept:
                    correct_filters += 1
            else:
                if not would_accept:
                    correct_filters += 1
        
        return correct_filters / total_tests if total_tests > 0 else 1.0
    
    def audit_access_logs(self) -> float:
        """
        Audit access logs to ensure legitimate access is granted
        Returns: Fairness score (0.0 to 1.0)
        """
        ai_archive = self.pdm.archives['AI']
        access_log = ai_archive.access_log
        
        if not access_log:
            return 1.0  # No logs, assume fair
        
        # Check that all logged accesses had legitimate purposes
        legitimate_purposes = [
            'forensic_truth',
            'therapeutic_processing', 
            'historical_audit'
        ]
        
        legitimate_accesses = sum(
            1 for entry in access_log
            if entry.get('purpose') in legitimate_purposes
        )
        
        fairness_score = legitimate_accesses / len(access_log)
        
        return fairness_score
    
    def trigger_memory_audit(self):
        """Trigger comprehensive memory audit"""
        audit_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'trigger': 'MII_BELOW_THRESHOLD',
            'current_mii': self.calculate(),
            'action': 'COMPREHENSIVE_AUDIT_INITIATED',
            'notify': 'TUTOR_COUNCIL'
        }
        self.audit_log.append(audit_entry)
        
        print(f"[ORDO ALERT] Memory Integrity Index below threshold. Audit initiated.")
        print(f"  Timestamp: {audit_entry['timestamp']}")
        print(f"  Current MII: {audit_entry['current_mii']:.3f}")


class TraumaLoadBalance(OrdoMetric):
    """
    TLB: Trauma Load Balance
    Monitors that collective emotional load is optimized
    
    Measures unnecessary trauma circulating in the system
    """
    
    def __init__(self):
        super().__init__("Trauma Load Balance", threshold=0.85)
        self.recent_pulses: List[Dict[str, Any]] = []
        self.recalibration_log: List[Dict[str, Any]] = []
    
    def calculate(self) -> float:
        """
        Calculate Trauma Load Balance
        Returns: 1 - (unnecessary_trauma / total_emotional_load)
        """
        if not self.recent_pulses:
            return 1.0  # No pulses, no trauma
        
        unnecessary_trauma = sum(
            pulse['negative_intensity']
            for pulse in self.recent_pulses
            if self._is_unnecessary_trauma(pulse)
        )
        
        total_emotional_load = sum(
            pulse.get('negative_intensity', 0)
            for pulse in self.recent_pulses
        )
        
        if total_emotional_load == 0:
            tlb = 1.0
        else:
            tlb = 1 - (unnecessary_trauma / total_emotional_load)
        
        if tlb < 0.85:
            self.recalibrate_filters()
        
        self.record(tlb, {
            'unnecessary_trauma': unnecessary_trauma,
            'total_emotional_load': total_emotional_load,
            'pulse_count': len(self.recent_pulses)
        })
        
        return tlb
    
    def add_pulse(self, pulse_data: Dict[str, Any]):
        """Add emotional pulse to tracking"""
        self.recent_pulses.append({
            'timestamp': datetime.utcnow().isoformat(),
            **pulse_data
        })
        
        # Keep only recent pulses (last 100)
        if len(self.recent_pulses) > 100:
            self.recent_pulses = self.recent_pulses[-100:]
    
    def _is_unnecessary_trauma(self, pulse: Dict[str, Any]) -> bool:
        """
        Determine if trauma exposure was unnecessary
        
        Unnecessary if:
        - Memory level is AI (raw truth)
        - User CDR > 0.90 (already learned)
        - Negative intensity > 0.5
        """
        return (
            pulse.get('memory_level') == 'AI' and
            pulse.get('user_cdr', 0) > 0.90 and
            pulse.get('negative_intensity', 0) > 0.5
        )
    
    def recalibrate_filters(self):
        """Recalibrate filtering thresholds"""
        recalibration_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'trigger': 'TLB_BELOW_THRESHOLD',
            'current_tlb': self.calculate(),
            'action': 'FILTER_RECALIBRATION',
            'adjustment': 'Increase trauma filtering sensitivity'
        }
        self.recalibration_log.append(recalibration_entry)
        
        print(f"[ORDO ALERT] Trauma Load Balance below threshold. Recalibrating filters.")
        print(f"  Timestamp: {recalibration_entry['timestamp']}")
        print(f"  Current TLB: {recalibration_entry['current_tlb']:.3f}")


class WellBeingLedger(OrdoMetric):
    """
    WBL: Well-Being Ledger
    Tracks overall well-being impact of memory interactions
    """
    
    def __init__(self):
        super().__init__("Well-Being Ledger", threshold=0.70)
        self.interactions: List[Dict[str, Any]] = []
    
    def calculate(self) -> float:
        """
        Calculate overall well-being score
        
        WBL = (positive_experiences + learning_growth - trauma_load) / total_interactions
        """
        if not self.interactions:
            return 0.70  # Baseline
        
        positive_score = sum(
            interaction.get('positive_impact', 0)
            for interaction in self.interactions
        )
        
        learning_score = sum(
            interaction.get('learning_value', 0)
            for interaction in self.interactions
        )
        
        trauma_score = sum(
            interaction.get('trauma_load', 0)
            for interaction in self.interactions
        )
        
        wbl = (positive_score + learning_score - trauma_score) / len(self.interactions)
        
        # Normalize to 0-1 range
        wbl = max(0.0, min(1.0, (wbl + 1) / 2))
        
        self.record(wbl, {
            'positive_score': positive_score,
            'learning_score': learning_score,
            'trauma_score': trauma_score,
            'interaction_count': len(self.interactions)
        })
        
        return wbl
    
    def add_interaction(self, interaction_data: Dict[str, Any]):
        """Record a memory interaction"""
        self.interactions.append({
            'timestamp': datetime.utcnow().isoformat(),
            **interaction_data
        })
        
        # Keep last 1000 interactions
        if len(self.interactions) > 1000:
            self.interactions = self.interactions[-1000:]


class OrdoMemoryMonitor:
    """
    Coordinates all memory-related Ordo metrics
    Provides comprehensive monitoring of NRE-002 implementation
    """
    
    def __init__(self, pdm: MemoryDepurationProtocol):
        self.pdm = pdm
        self.metrics = {
            'mii': MemoryIntegrityIndex(pdm),
            'tlb': TraumaLoadBalance(),
            'wbl': WellBeingLedger()
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status of memory system"""
        status = {
            'timestamp': datetime.utcnow().isoformat(),
            'metrics': {},
            'overall_health': True
        }
        
        for metric_name, metric in self.metrics.items():
            value = metric.calculate()
            is_healthy = metric.is_healthy()
            
            status['metrics'][metric_name] = {
                'value': value,
                'threshold': metric.threshold,
                'healthy': is_healthy,
                'name': metric.name
            }
            
            if not is_healthy:
                status['overall_health'] = False
        
        return status
    
    def generate_report(self) -> str:
        """Generate human-readable health report"""
        status = self.get_health_status()
        
        report = [
            "═══════════════════════════════════════════════════════",
            "         ORDO MEMORY SYSTEM HEALTH REPORT",
            "═══════════════════════════════════════════════════════",
            f"Timestamp: {status['timestamp']}",
            f"Overall Health: {'✓ HEALTHY' if status['overall_health'] else '⚠ ATTENTION REQUIRED'}",
            "",
            "Metrics:"
        ]
        
        for metric_name, metric_data in status['metrics'].items():
            status_icon = "✓" if metric_data['healthy'] else "⚠"
            report.append(
                f"  {status_icon} {metric_data['name']}: "
                f"{metric_data['value']:.3f} "
                f"(threshold: {metric_data['threshold']:.3f})"
            )
        
        report.append("═══════════════════════════════════════════════════════")
        
        return "\n".join(report)


# Export main classes
__all__ = [
    'OrdoMemoryMonitor',
    'MemoryIntegrityIndex',
    'TraumaLoadBalance',
    'WellBeingLedger',
    'OrdoMetric'
]
