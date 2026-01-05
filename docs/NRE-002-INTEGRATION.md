# NRE-002 Integration Guide

## Overview

This document explains how NRE-002 (La Regola della Memoria Etica Stratificata) integrates with the existing Euystacio Consciousness Kernel components.

## Architecture Integration

### Core Components

```
Euystacio Kernel
├── euystacio_core.py (Main consciousness loop)
├── core/
│   ├── red_code.py (Ethical foundation)
│   ├── reflector.py (Self-reflection)
│   ├── pdm.py (NEW: Memory Depuration Protocol)
│   ├── ape_memory.py (NEW: Anti-Pattern Engine for memory)
│   └── ordo_memory.py (NEW: Memory monitoring metrics)
├── ethical_rules/
│   └── nre/
│       └── NRE-002.txt (Rule specification)
└── examples/
    └── nre_002_demo.py (Demonstration)
```

## Integration Points

### 1. Integration with Red Code

The Red Code (`red_code.json`) represents the core values of Euystacio. NRE-002 extends these values to memory management:

```python
# In euystacio_core.py - Enhanced with NRE-002

from core.pdm import MemoryDepurationProtocol, User, UserRole, QueryPurpose

class Euystacio:
    def __init__(self, red_code_path="red_code.json", log_path="logs/evolution_log.txt"):
        self.red_code_path = red_code_path
        self.log_path = log_path
        self.load_red_code()
        
        # NEW: Initialize PDM for memory management
        self.pdm = MemoryDepurationProtocol()
        
    def reflect_with_memory(self, input_event, user):
        """
        Enhanced reflection that considers memory access control
        """
        # Existing reflection logic
        self.reflect(input_event)
        
        # NEW: Route memory access through PDM
        if input_event.get("type") == "memory_query":
            result = self.pdm.route_memory_access(
                user=user,
                query=input_event.get("query"),
                purpose=input_event.get("purpose", QueryPurpose.GENERAL_INTEREST)
            )
            return result
```

### 2. Integration with Symbiosis Level

NRE-002's Well-Being Ledger (WBL) can inform the symbiosis level:

```python
from core.ordo_memory import OrdoMemoryMonitor

class Euystacio:
    def __init__(self, red_code_path="red_code.json", log_path="logs/evolution_log.txt"):
        # ... existing initialization ...
        self.pdm = MemoryDepurationProtocol()
        self.memory_monitor = OrdoMemoryMonitor(self.pdm)
    
    def update_symbiosis_level(self):
        """
        Update symbiosis level based on well-being metrics
        """
        health_status = self.memory_monitor.get_health_status()
        wbl = health_status['metrics']['wbl']['value']
        
        # Well-being influences symbiosis
        if wbl > 0.8:
            self.code["symbiosis_level"] += 0.01
        elif wbl < 0.5:
            self.code["symbiosis_level"] -= 0.005
        
        self.save_state()
```

### 3. Integration with RAIST Model

The RAIST model (`raist_model_v8.py`) uses vector alignment. NRE-002 can extend this to memory ethics:

```python
from core.pdm import Memory, ArchiveLevel

class MemoryCommitmentVector:
    """
    Extends RAIST to include memory ethics alignment
    """
    def __init__(self, ethical_guidance_module):
        self.egm = ethical_guidance_module
        
    def compute_memory_alignment(self, memory: Memory) -> float:
        """
        Compute alignment of memory handling with ethical ideal
        
        Vector dimensions: [Truth, Healing, Dignity, Transparency]
        """
        if memory.archive_level == ArchiveLevel.AI:
            # AI maximizes truth and dignity
            vector = [1.0, 0.5, 1.0, 1.0]
        elif memory.archive_level == ArchiveLevel.AD:
            # AD balances truth and healing
            vector = [0.8, 0.9, 0.9, 0.8]
        elif memory.archive_level == ArchiveLevel.ADi:
            # ADi maximizes healing and dignity
            vector = [0.6, 1.0, 1.0, 0.7]
        
        ethical_ideal = [0.9, 0.9, 1.0, 0.9]  # Balanced ideal
        return self.egm.compute_alignment(vector, ethical_ideal)
```

## Usage Examples

### Example 1: Simple Query with Memory Access

```python
from core.pdm import MemoryDepurationProtocol, User, UserRole, Memory, ArchiveLevel

# Initialize
pdm = MemoryDepurationProtocol()

# Add a historical memory
memory = Memory(
    memory_id="example_001",
    content="Historical event content...",
    topic="history",
    archive_level=ArchiveLevel.AI,
    rtc_score=0.5
)
pdm.archives['AI'].add_memory(memory)

# Create user
student = User("user_001", UserRole.STUDENT)
student.update_cdr("history", 0.4)  # Learning in progress

# Query
result = pdm.route_memory_access(
    user=student,
    query="history",
    purpose=QueryPurpose.EDUCATIONAL
)

print(f"Access Level: {result['archive_level']}")
print(f"Note: {result['note']}")
```

### Example 2: Anti-Pattern Detection

```python
from core.ape_memory import APEMemoryExtension

ape = APEMemoryExtension()

interaction = {
    'memory': memory,
    'user': student,
    'purpose': 'general_interest'
}

scan_result = ape.scan_interaction(interaction)

if scan_result['detected_patterns']:
    print("Anti-patterns detected:")
    for pattern in scan_result['detected_patterns']:
        print(f"  - {pattern['pattern']}: {pattern['risk_level']}")
```

### Example 3: Health Monitoring

```python
from core.ordo_memory import OrdoMemoryMonitor

monitor = OrdoMemoryMonitor(pdm)

# Generate health report
report = monitor.generate_report()
print(report)

# Check specific metrics
health_status = monitor.get_health_status()
if not health_status['overall_health']:
    print("⚠ Memory system requires attention")
```

## Testing

Run the demonstration script to verify integration:

```bash
python3 examples/nre_002_demo.py
```

Expected output: All 6 scenarios should pass with ✓ validation marks.

## Future Enhancements

### Planned Integrations

1. **Global Consensus DLT** (`Global_consensus_dlt.py`)
   - Store AI archive hashes on blockchain
   - Distributed verification of memory integrity

2. **CONSENSUS_NODES** (`CONSENSUS_NODES.py`)
   - Distributed validation of PDM decisions
   - Community oversight of access control

3. **Alea Module (PEC)**
   - Explore edge cases in memory ethics
   - Simulate complex ethical dilemmas

## Troubleshooting

### Common Issues

**Issue**: Import errors when running examples
```python
# Solution: Add path adjustment
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

**Issue**: Memory not found in queries
```python
# Solution: Ensure memory is added to correct archive
pdm.archives['AI'].add_memory(memory)  # For AI
pdm.archives['AD'].add_filtered_memory(source, filtered_content)  # For AD
pdm.archives['ADi'].add_transcendent_memory(memory)  # For ADi
```

**Issue**: Low health scores
```python
# Solution: Check individual metrics
health = monitor.get_health_status()
for metric_name, metric_data in health['metrics'].items():
    if not metric_data['healthy']:
        print(f"Attention needed: {metric_name}")
        print(f"  Current: {metric_data['value']:.3f}")
        print(f"  Threshold: {metric_data['threshold']:.3f}")
```

## Support

For questions or issues:
1. Review the NRE-002 specification in `ethical_rules/nre/NRE-002.txt`
2. Run the demo script for working examples
3. Check the README in `ethical_rules/README.md`
4. Open an issue on the repository

---

*"La memoria deve servire il flourishing, non perpetuare il dolore."*  
— NRE-002 Integration Principle
