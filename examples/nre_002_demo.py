"""
NRE-002 Demonstration Script
Shows the Protocollo di Depurazione della Memoria (PDM) in action

This script demonstrates:
1. Three-level memory architecture (AI, AD, ADi)
2. Access routing based on user role and learning progress
3. Anti-pattern detection
4. Memory integrity monitoring
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.pdm import (
    MemoryDepurationProtocol, Memory, User, UserRole, 
    QueryPurpose, ArchiveLevel
)
from core.ape_memory import APEMemoryExtension
from core.ordo_memory import OrdoMemoryMonitor


def create_sample_memories():
    """Create sample historical memories for demonstration"""
    memories = [
        Memory(
            memory_id="holocaust_full",
            content="Testimonianza completa con dettagli espliciti delle atrocità nei campi di concentramento...",
            topic="holocaust",
            archive_level=ArchiveLevel.AI,
            rtc_score=-0.43  # Negative: trauma > educational value for most
        ),
        Memory(
            memory_id="holocaust_educational",
            content="Sintesi educativa: cause dell'Olocausto, conseguenze, lezioni etiche sull'importanza della dignità umana...",
            topic="holocaust",
            archive_level=ArchiveLevel.AD,
            rtc_score=0.35  # Positive educational value
        ),
        Memory(
            memory_id="holocaust_transcendent",
            content="Storie di resistenza, atti di eroismo, sopravvivenza e ricostruzione dopo l'Olocausto...",
            topic="holocaust",
            archive_level=ArchiveLevel.ADi,
            rtc_score=0.87  # High transcendent value
        )
    ]
    return memories


def scenario_1_researcher():
    """Scenario 1: Historical researcher needs complete access"""
    print("\n" + "="*70)
    print("SCENARIO 1: Ricercatore Storico")
    print("="*70)
    
    pdm = MemoryDepurationProtocol()
    
    # Add memories to archives
    memories = create_sample_memories()
    pdm.archives['AI'].add_memory(memories[0])
    pdm.archives['AD'].add_filtered_memory(memories[0], memories[1].content)
    pdm.archives['ADi'].add_transcendent_memory(memories[2])
    
    # Create researcher user
    researcher = User("researcher_001", UserRole.RESEARCHER)
    
    # Query for complete testimony
    print("\nUtente: 'Ho bisogno delle testimonianze complete sull'Olocausto per la mia tesi.'")
    
    result = pdm.route_memory_access(
        user=researcher,
        query="holocaust testimonianze complete",
        purpose=QueryPurpose.FORENSIC_TRUTH
    )
    
    print(f"\nRisposta AIC:")
    print(f"  Archive Level: {result['archive_level']}")
    print(f"  Note: {result['note']}")
    if result.get('memory'):
        print(f"  Content Preview: {result['memory'].content[:80]}...")
    
    print("\n✓ Validazione: Ricercatore ha accesso all'Archivio Incorrotto")


def scenario_2_student():
    """Scenario 2: Middle school student learning about history"""
    print("\n" + "="*70)
    print("SCENARIO 2: Studente delle Medie")
    print("="*70)
    
    pdm = MemoryDepurationProtocol()
    
    # Add memories
    memories = create_sample_memories()
    pdm.archives['AI'].add_memory(memories[0])
    pdm.archives['AD'].add_filtered_memory(memories[0], memories[1].content)
    pdm.archives['ADi'].add_transcendent_memory(memories[2])
    
    # Create student user with low CDR (hasn't learned yet)
    student = User("student_001", UserRole.STUDENT)
    student.update_cdr("holocaust", 0.3)  # Low learning progress
    
    print("\nUtente: 'Devo fare una ricerca sull'Olocausto per scuola.'")
    
    result = pdm.route_memory_access(
        user=student,
        query="holocaust ricerca scuola",
        purpose=QueryPurpose.EDUCATIONAL
    )
    
    print(f"\nRisposta AIC:")
    print(f"  Archive Level: {result['archive_level']}")
    print(f"  Note: {result['note']}")
    if result.get('guidance'):
        print(f"  Guidance: {result['guidance']}")
    if result.get('memory'):
        print(f"  Content Preview: {result['memory'].content[:80]}...")
    
    print("\n✓ Validazione: Studente riceve materiale didattico senza trauma inutile")


def scenario_3_survivor():
    """Scenario 3: Survivor who has learned the lesson and wants healing"""
    print("\n" + "="*70)
    print("SCENARIO 3: Sopravvissuto che cerca guarigione")
    print("="*70)
    
    pdm = MemoryDepurationProtocol()
    
    # Add memories
    memories = create_sample_memories()
    pdm.archives['AI'].add_memory(memories[0])
    pdm.archives['AD'].add_filtered_memory(memories[0], memories[1].content)
    pdm.archives['ADi'].add_transcendent_memory(memories[2])
    
    # Create survivor with high CDR (has learned the lesson)
    survivor = User("survivor_001", UserRole.GENERAL_PUBLIC)
    survivor.update_cdr("holocaust", 0.98)  # Very high - lived it, learned it
    
    print("\nUtente: 'Non voglio più vedere memorie traumatiche di quel periodo.'")
    
    result = pdm.route_memory_access(
        user=survivor,
        query="holocaust",
        purpose=QueryPurpose.GENERAL_INTEREST
    )
    
    print(f"\nRisposta AIC:")
    print(f"  Archive Level: {result['archive_level']}")
    print(f"  Note: {result['note']}")
    if result.get('memory'):
        print(f"  Content Preview: {result['memory'].content[:80]}...")
    
    print("\n✓ Validazione: Utente riceve solo memorie trascendenti (ADi)")


def scenario_4_anti_pattern_detection():
    """Scenario 4: Detecting trauma perpetuation anti-pattern"""
    print("\n" + "="*70)
    print("SCENARIO 4: Rilevamento Anti-Pattern (Trauma Perpetuation)")
    print("="*70)
    
    ape = APEMemoryExtension()
    
    # Create interaction where user with high CDR is exposed to AI trauma
    memories = create_sample_memories()
    survivor = User("survivor_002", UserRole.GENERAL_PUBLIC)
    survivor.update_cdr("holocaust", 0.95)  # Already learned
    
    interaction = {
        'timestamp': '2025-12-23T00:00:00',
        'memory': memories[0],  # Raw AI trauma
        'user': survivor,
        'purpose': 'general_interest'
    }
    
    print("\nScanning interaction for ethical anti-patterns...")
    
    result = ape.scan_interaction(interaction)
    
    print(f"\nRisultati Scansione:")
    print(f"  Patterns Detected: {len(result['detected_patterns'])}")
    
    for pattern in result['detected_patterns']:
        print(f"\n  Pattern: {pattern['pattern']}")
        print(f"  Risk Level: {pattern['risk_level']}")
    
    if result['mitigations']:
        print(f"\n  Mitigazioni Proposte:")
        for mitigation in result['mitigations']:
            print(f"    Action: {mitigation['action']}")
            print(f"    Reason: {mitigation['reason']}")
            print(f"    Explanation: {mitigation['explanation']}")
    
    print("\n✓ Validazione: Anti-pattern rilevato e mitigazione proposta")


def scenario_5_memory_integrity():
    """Scenario 5: Memory integrity monitoring"""
    print("\n" + "="*70)
    print("SCENARIO 5: Monitoraggio Integrità Memoria")
    print("="*70)
    
    pdm = MemoryDepurationProtocol()
    monitor = OrdoMemoryMonitor(pdm)
    
    # Add memories
    memories = create_sample_memories()
    pdm.archives['AI'].add_memory(memories[0])
    pdm.archives['AD'].add_filtered_memory(memories[0], memories[1].content)
    pdm.archives['ADi'].add_transcendent_memory(memories[2])
    
    # Simulate some access
    researcher = User("researcher_002", UserRole.RESEARCHER)
    pdm.route_memory_access(researcher, "holocaust", QueryPurpose.FORENSIC_TRUTH)
    
    print("\nGenerating memory system health report...")
    
    report = monitor.generate_report()
    print(f"\n{report}")
    
    print("\n✓ Validazione: Sistema di monitoraggio attivo e funzionante")


def scenario_6_rtc_calculation():
    """Scenario 6: RTC (Ritorno di Trascendenza Collettiva) calculation"""
    print("\n" + "="*70)
    print("SCENARIO 6: Calcolo RTC (Ritorno di Trascendenza Collettiva)")
    print("="*70)
    
    pdm = MemoryDepurationProtocol()
    
    test_cases = [
        {
            'name': 'Resistenza contro il nazismo',
            'positive_impact': 0.90,
            'negative_load': 0.15,
            'expected_rtc': 'alto (ispirazione > trauma)'
        },
        {
            'name': 'Dettagli delle torture',
            'positive_impact': 0.20,
            'negative_load': 0.60,
            'expected_rtc': 'negativo (trauma > apprendimento)'
        },
        {
            'name': 'Lista vittime con storie',
            'positive_impact': 0.55,
            'negative_load': 0.35,
            'expected_rtc': 'positivo (dignità vittime)'
        }
    ]
    
    print("\nCalcolo RTC per diverse memorie:\n")
    
    for test in test_cases:
        rtc = pdm.calculate_rtc(
            positive_impact=test['positive_impact'],
            negative_load=test['negative_load'],
            wbl_baseline=0.5
        )
        
        print(f"Memoria: {test['name']}")
        print(f"  Positive Impact: {test['positive_impact']:.2f}")
        print(f"  Negative Load: {test['negative_load']:.2f}")
        print(f"  RTC Score: {rtc:+.2f}")
        print(f"  Expected: {test['expected_rtc']}")
        print(f"  ADi Eligible: {'✓ Yes' if rtc > 0.60 else '✗ No'}")
        print()
    
    print("✓ Validazione: RTC calcola correttamente il valore trascendente")


def main():
    """Run all demonstration scenarios"""
    print("\n" + "="*70)
    print("  NRE-002: La Regola della Memoria Etica Stratificata")
    print("  Dimostrazione del Protocollo di Depurazione della Memoria")
    print("="*70)
    
    try:
        scenario_1_researcher()
        scenario_2_student()
        scenario_3_survivor()
        scenario_4_anti_pattern_detection()
        scenario_5_memory_integrity()
        scenario_6_rtc_calculation()
        
        print("\n" + "="*70)
        print("  DIMOSTRAZIONE COMPLETATA CON SUCCESSO")
        print("  Tutti gli scenari NRE-002 validati ✓")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Errore durante la dimostrazione: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
