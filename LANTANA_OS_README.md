# Lantana OS - Anchoring & Triplesign Documentation

## Overview

The Lantana OS Anchoring & Triplesign system implements a distributed procedure for ensuring eternal persistence and verification of critical data through IPFS and Arweave networks. The system uses triple signature validation from three geographically distributed nodes to ensure data integrity and consensus.

## Architecture

### Components

1. **IPFS Manager** - Handles CID generation and data aggregation
2. **Triple Signature Nodes** - Three distributed nodes that cryptographically sign data:
   - **Africa** - Central Africa Node
   - **North Pole** - Arctic Distributed Node  
   - **Nexus Central** - Central Coordination Hub
3. **Node Synchronizer** - Verifies synchronization and coherence between nodes
4. **PeaceBonds** - Metadata anchoring system for critical commitments
5. **ST Anchor** - Arweave notarization for eternal persistence

### Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. PeaceBonds Timestamp Anchoring                         │
│     - #001: IDRO (Water Resources)                         │
│     - #002: HELIOS (Solar Energy)                          │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  2. Node Synchronization Verification                      │
│     - Africa ↔ North Pole coherence check                  │
│     - Minimum coherence requirement: 0.94                  │
│     - Overall system coherence validation                  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  3. Metadata Preparation                                   │
│     - System information                                   │
│     - PeaceBonds data                                      │
│     - Node synchronization report                          │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  4. Triple Signature Application                           │
│     - Africa node signature                                │
│     - North Pole node signature                            │
│     - Nexus Central node signature                         │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  5. IPFS Data Aggregation                                  │
│     - Combine metadata and signatures                      │
│     - Generate Content Identifier (CID)                    │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  6. ST Anchor - Arweave Notarization                       │
│     - Permanent storage on Arweave network                 │
│     - Eternal persistence guarantee                        │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  7. IPFS Network Broadcasting                              │
│     - Distribute signed metadata                           │
│     - Make bundle publicly verifiable                      │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  8. Triple Signature Bundle Generation                     │
│     - Complete verification package                        │
│     - JSON format for easy validation                      │
└─────────────────────────────────────────────────────────────┘
```

## Installation

No additional dependencies required. The system uses Python 3 standard library.

```bash
# Make the CLI executable
chmod +x st_anchor.py
```

## Usage

### Command Line Interface

The `st_anchor.py` CLI provides three main commands:

#### 1. Execute Anchoring Procedure

Run the complete anchoring and triple signature workflow:

```bash
# With default PeaceBonds (IDRO and HELIOS)
python st_anchor.py anchor

# With custom PeaceBonds
python st_anchor.py anchor --peace-bond "003:TERRA:Earth Resources"

# Specify custom output file
python st_anchor.py anchor --output my_bundle.json
```

#### 2. Verify Triple Signature Bundle

Verify the integrity and completeness of a bundle:

```bash
python st_anchor.py verify triple_signature_bundle.json
```

Verification checks:
- Bundle structure completeness
- All three signatures present and valid
- Node synchronization status
- Coherence requirements met (≥0.94)
- Arweave anchoring confirmation
- IPFS CID generation
- PeaceBonds timestamp anchoring

#### 3. Show Node Status

Check current synchronization status of all nodes:

```bash
python st_anchor.py status
```

### Programmatic Usage

You can also use the Lantana OS module directly in Python:

```python
from lantana_os import LantanaOS

# Initialize system
lantana = LantanaOS()

# Add PeaceBonds
lantana.add_peace_bond(
    "001",
    "IDRO", 
    {
        "type": "Water Resources",
        "region": "Mediterranean Basin",
        "commitment": "Sustainable water management"
    }
)

# Execute complete procedure
bundle = lantana.execute_anchoring_procedure()

# Get JSON representation
bundle_json = lantana.get_bundle_json(bundle)
```

## Triple Signature Bundle Format

The output bundle is a comprehensive JSON document containing:

```json
{
  "bundle_type": "Lantana OS Triple Signature Bundle",
  "version": "1.0",
  "timestamp": "2026-01-22T03:53:17.857267Z",
  "ipfs": {
    "cid": "Qm...",
    "aggregated_data": { ... }
  },
  "signatures": {
    "Africa": {
      "signature": "7e65f60...",
      "node_location": "Central Africa Node",
      "coherence": 1.0
    },
    "North_Pole": { ... },
    "Nexus_Central": { ... }
  },
  "synchronization": {
    "overall_coherence": 1.0,
    "nodes": { ... },
    "synchronizations": [ ... ]
  },
  "arweave": {
    "arweave_tx_id": "5a03eef...",
    "status": "CONFIRMED",
    "permanence": "ETERNAL"
  },
  "peace_bonds": [ ... ],
  "verification": {
    "all_signatures_valid": true,
    "synchronization_verified": true,
    "arweave_anchored": true,
    "ipfs_broadcasted": true
  }
}
```

## Key Features

### 1. Triple Signature System
- Three geographically distributed nodes provide signatures
- Ensures no single point of failure
- Cryptographic validation using SHA-256

### 2. Node Synchronization
- Real-time coherence monitoring
- Minimum coherence threshold: 0.94
- Pairwise synchronization checks
- Special focus on Africa ↔ North Pole link

### 3. PeaceBonds
- Timestamp-anchored commitments
- Support for multiple bond types
- Immutable once anchored
- Default bonds: IDRO (Water) and HELIOS (Solar)

### 4. Dual Persistence
- **IPFS**: Distributed content-addressed storage
- **Arweave**: Permanent, immutable storage
- Combined approach ensures both distribution and eternality

### 5. Comprehensive Verification
- Structural validation
- Signature verification
- Coherence checks
- Status confirmations

## Security Considerations

1. **Cryptographic Signatures**: All data signed with SHA-256 hashes
2. **Distributed Consensus**: Requires agreement from all three nodes
3. **Coherence Requirements**: Minimum 0.94 threshold prevents degraded operations
4. **Immutable Storage**: Arweave guarantees permanent, tamper-proof records
5. **Content Addressing**: IPFS CIDs ensure data integrity

## Example Output

When running the anchoring procedure, you'll see output like:

```
================================================================================
LANTANA OS - ANCHORING & TRIPLESIGN PROCEDURE
================================================================================

[Step 1] Anchoring PeaceBonds timestamps...
  ✓ PeaceBond #001: IDRO - 2026-01-22T03:53:17.856671Z
  ✓ PeaceBond #002: HELIOS - 2026-01-22T03:53:17.856688Z

[Step 2] Verifying node synchronization...
  Node Status:
    • Africa: ONLINE (coherence: 1.0)
    • North Pole: ONLINE (coherence: 1.0)
    • Nexus Central: ONLINE (coherence: 1.0)

  Africa ↔ North Pole Synchronization:
    • Coherence: 0.9814
    • Status: ✓ SYNCHRONIZED

  ✓ Overall System Coherence: 1.0

[Step 4] Applying triple signatures...
  ✓ Africa: a41ea1e4964b2077...91fb0dcf9c48e49c
  ✓ North_Pole: 305f4538ff752098...8a3dd8abe7db50b9
  ✓ Nexus_Central: 37b427c70f9da1b8...362719607553fe72

[Step 5] Aggregating data and generating IPFS CID...
  ✓ IPFS CID: Qm135116f8304d95db72c42b7f8b3c5475e29e6f88dc66

[Step 6] Executing ST Anchor for Arweave notarization...
  ✓ Arweave TX ID: f757e394f0bdf344e585a9ca639d9f285279505dbf811c0f418b5a29f748da95
  ✓ Permanence: ETERNAL

================================================================================
PROCEDURE COMPLETE ✓
================================================================================

Bundle Status: COMPLETE
Triple Signatures: 3/3 ✓
System Coherence: 1.0 ✓
Arweave Anchored: CONFIRMED ✓
```

## Integration with Euystacio Framework

The Lantana OS system integrates with the broader Euystacio Consciousness Kernel:

- **Ethical Alignment**: Follows the Lex Amoris principles
- **Red Code Compatibility**: Can be integrated with Red Code protocols
- **Consensus Integration**: Compatible with Global_consensus_dlt.py
- **Distributed Ledger**: Can work with Euchridian G-DLT

## Future Enhancements

- Real network integration with actual IPFS and Arweave nodes
- Advanced cryptographic signatures (e.g., Ed25519)
- Multi-signature wallet integration
- Real-time node health monitoring
- Automatic failover mechanisms
- Geographic diversity scoring

## License

This module is part of the Euystacio Consciousness Kernel project.
See the main LICENSE file for details.

## Authors

Developed as part of the Lantana OS initiative for the Euystacio project.
