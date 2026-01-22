#!/usr/bin/env python3
"""
ST Anchor CLI - Command-line interface for Lantana OS Anchoring & Triplesign
"""

import argparse
import json
import sys
from lantana_os import LantanaOS


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="ST Anchor - Lantana OS Anchoring & Triplesign Command",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run complete anchoring procedure with default PeaceBonds
  python st_anchor.py anchor
  
  # Add custom PeaceBonds and run anchoring
  python st_anchor.py anchor --peace-bond "003:TERRA:Earth Resources"
  
  # Verify an existing bundle
  python st_anchor.py verify triple_signature_bundle.json
  
  # Show current node status
  python st_anchor.py status
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Anchor command
    anchor_parser = subparsers.add_parser('anchor', help='Execute anchoring procedure')
    anchor_parser.add_argument(
        '--peace-bond',
        action='append',
        help='Add PeaceBond in format ID:NAME:TYPE (can be used multiple times)'
    )
    anchor_parser.add_argument(
        '--output',
        default='triple_signature_bundle.json',
        help='Output file for the bundle (default: triple_signature_bundle.json)'
    )
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify a Triple Signature Bundle')
    verify_parser.add_argument('bundle_file', help='Path to bundle JSON file')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show node synchronization status')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    if args.command == 'anchor':
        return execute_anchor(args)
    elif args.command == 'verify':
        return verify_bundle(args)
    elif args.command == 'status':
        return show_status(args)
    
    return 0


def execute_anchor(args):
    """Execute the anchoring procedure."""
    # Initialize Lantana OS
    lantana = LantanaOS()
    
    # Add default PeaceBonds if none specified
    if not args.peace_bond:
        lantana.add_peace_bond(
            "001",
            "IDRO",
            {
                "type": "Water Resources",
                "region": "Mediterranean Basin",
                "commitment": "Sustainable water management and equitable distribution"
            }
        )
        
        lantana.add_peace_bond(
            "002",
            "HELIOS",
            {
                "type": "Solar Energy",
                "region": "Global",
                "commitment": "Renewable energy transition and solar infrastructure"
            }
        )
    else:
        # Parse custom PeaceBonds
        for pb in args.peace_bond:
            try:
                # Use rsplit to split from the right, limiting to 2 splits
                # This handles colons in the TYPE field
                parts = pb.split(':', 2)
                if len(parts) != 3:
                    print(f"Error: Invalid PeaceBond format: {pb}")
                    print("Expected format: ID:NAME:TYPE")
                    print("Note: TYPE can contain colons, but ID and NAME cannot")
                    return 1
                
                bond_id, name, bond_type = parts
                lantana.add_peace_bond(
                    bond_id.strip(),
                    name.strip(),
                    {"type": bond_type.strip(), "custom": True}
                )
            except Exception as e:
                print(f"Error parsing PeaceBond {pb}: {e}")
                return 1
    
    # Execute the complete anchoring procedure
    try:
        bundle = lantana.execute_anchoring_procedure()
        
        # Save the bundle to a JSON file
        bundle_json = lantana.get_bundle_json(bundle)
        with open(args.output, "w") as f:
            f.write(bundle_json)
        
        print(f"\n✓ Triple Signature Bundle saved to: {args.output}")
        return 0
        
    except Exception as e:
        print(f"\n✗ Error during anchoring procedure: {e}")
        import traceback
        traceback.print_exc()
        return 1


def verify_bundle(args):
    """Verify a Triple Signature Bundle."""
    try:
        with open(args.bundle_file, 'r') as f:
            bundle = json.load(f)
        
        print("\n" + "="*80)
        print("TRIPLE SIGNATURE BUNDLE VERIFICATION")
        print("="*80)
        
        # Check bundle structure
        print("\n[Structure Check]")
        required_fields = ["bundle_type", "version", "timestamp", "ipfs", "signatures", 
                          "synchronization", "arweave", "peace_bonds", "status", "verification"]
        
        missing = [f for f in required_fields if f not in bundle]
        if missing:
            print(f"  ✗ Missing required fields: {', '.join(missing)}")
            return 1
        print("  ✓ All required fields present")
        
        # Check bundle type
        print("\n[Bundle Type]")
        if bundle.get("bundle_type") != "Lantana OS Triple Signature Bundle":
            print(f"  ✗ Invalid bundle type: {bundle.get('bundle_type')}")
            return 1
        print(f"  ✓ {bundle['bundle_type']}")
        
        # Check signatures
        print("\n[Signatures]")
        sigs = bundle.get("signatures", {})
        required_nodes = ["Africa", "North_Pole", "Nexus_Central"]
        for node in required_nodes:
            if node in sigs:
                sig_data = sigs[node]
                print(f"  ✓ {node}: {sig_data['signature'][:16]}...{sig_data['signature'][-16:]}")
            else:
                print(f"  ✗ Missing signature from {node}")
                return 1
        
        # Check synchronization
        print("\n[Node Synchronization]")
        sync = bundle.get("synchronization", {})
        coherence = sync.get("overall_coherence", 0.0)
        print(f"  Overall Coherence: {coherence}")
        
        for sync_pair in sync.get("synchronizations", []):
            status = "✓" if sync_pair.get("synchronized") else "✗"
            print(f"  {status} {sync_pair['nodes']}: {sync_pair['coherence']}")
        
        if coherence < 0.94:
            print(f"  ✗ Coherence {coherence} below minimum 0.94")
            return 1
        
        # Check Arweave
        print("\n[Arweave Anchoring]")
        arweave = bundle.get("arweave", {})
        print(f"  TX ID: {arweave.get('arweave_tx_id', 'N/A')}")
        print(f"  Status: {arweave.get('status', 'N/A')}")
        print(f"  Permanence: {arweave.get('permanence', 'N/A')}")
        
        # Check IPFS
        print("\n[IPFS]")
        ipfs = bundle.get("ipfs", {})
        print(f"  CID: {ipfs.get('cid', 'N/A')}")
        
        # Check PeaceBonds
        print("\n[PeaceBonds]")
        peace_bonds = bundle.get("peace_bonds", [])
        for pb in peace_bonds:
            status = "✓" if pb.get("anchored") else "✗"
            print(f"  {status} {pb['bond_id']}: {pb['name']} - {pb.get('timestamp', 'N/A')}")
        
        # Overall verification
        print("\n[Overall Verification]")
        verification = bundle.get("verification", {})
        all_valid = all([
            verification.get("all_signatures_valid"),
            verification.get("synchronization_verified"),
            verification.get("arweave_anchored"),
            verification.get("ipfs_broadcasted")
        ])
        
        for key, value in verification.items():
            status = "✓" if value else "✗"
            print(f"  {status} {key}: {value}")
        
        print("\n" + "="*80)
        if all_valid:
            print("BUNDLE VERIFICATION: ✓ PASSED")
            print("="*80)
            return 0
        else:
            print("BUNDLE VERIFICATION: ✗ FAILED")
            print("="*80)
            return 1
            
    except FileNotFoundError:
        print(f"Error: Bundle file not found: {args.bundle_file}")
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in bundle file: {e}")
        return 1
    except Exception as e:
        print(f"Error during verification: {e}")
        import traceback
        traceback.print_exc()
        return 1


def show_status(args):
    """Show current node synchronization status."""
    lantana = LantanaOS()
    
    print("\n" + "="*80)
    print("LANTANA OS - NODE STATUS")
    print("="*80)
    
    sync_report = lantana.synchronizer.verify_all_nodes()
    
    print("\n[Node Status]")
    for name, status in sync_report["nodes"].items():
        print(f"  • {name}:")
        print(f"    Location: {status['location']}")
        print(f"    Coherence: {status['coherence']}")
        print(f"    Status: {status['status']}")
    
    print("\n[Synchronizations]")
    for sync in sync_report["synchronizations"]:
        status_icon = "✓" if sync["synchronized"] else "✗"
        print(f"  {status_icon} {sync['nodes']}: {sync['coherence']}")
    
    print(f"\n[Overall System Coherence]")
    coherence = sync_report["overall_coherence"]
    if coherence >= 0.94:
        print(f"  ✓ {coherence} (Sufficient)")
    else:
        print(f"  ✗ {coherence} (Below minimum 0.94)")
    
    print("\n" + "="*80)
    return 0


if __name__ == "__main__":
    sys.exit(main())
