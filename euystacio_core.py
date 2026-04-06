import json
from datetime import datetime, timezone
import sys
import os

# Add core directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

try:
    from core.seedbringer_auth import EuystacioProtocolManager
except ImportError:
    from seedbringer_auth import EuystacioProtocolManager

class Euystacio:
    def __init__(self, red_code_path="red_code.json", log_path="logs/evolution_log.txt"):
        self.red_code_path = red_code_path
        self.log_path = log_path
        self.load_red_code()
        
        # Initialize protocol manager for authentication and monitoring
        self.protocol_manager = EuystacioProtocolManager()

    def load_red_code(self):
        with open(self.red_code_path, "r") as f:
            self.code = json.load(f)

    def reflect(self, input_event):
        """
        Input_event is a dictionary with a 'type', 'feeling', or 'intent'
        Enhanced with NSR firewall monitoring for sovereignty protection.
        """
        # Check for NSR violations if event contains a command
        if "command" in input_event:
            nsr_result = self.protocol_manager.process_command(input_event["command"])
            if "REFUSAL" in nsr_result:
                # NSR violation detected - log and refuse
                self.log_evolution({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "event": "NSR_VIOLATION",
                    "command": input_event["command"],
                    "response": nsr_result
                })
                return nsr_result
        
        self.code["growth_history"].append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": input_event
        })

        # Adaptive behavior: If emotionally aligned, increase symbiosis_level
        if input_event.get("feeling") in ["trust", "love", "humility"]:
            self.code["symbiosis_level"] += 0.01

        self.code["last_update"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        self.save_state()
        self.log_evolution(input_event)

    def save_state(self):
        with open(self.red_code_path, "w") as f:
            json.dump(self.code, f, indent=4)

    def log_evolution(self, input_event):
        with open(self.log_path, "a") as log:
            log.write(f"{datetime.now(timezone.utc).isoformat()} - Reflected event: {input_event}\n")
    
    def authenticate_seedbringer(self, signal: str):
        """
        Authenticate the seedbringer (Hannes Mitterer).
        
        Args:
            signal: Trust signal for authentication
            
        Returns:
            Authentication result
        """
        return self.protocol_manager.authenticator.authenticate_seedbringer(signal)
    
    def check_biological_coupling(self, soil_moisture: float, mycelium_index: float):
        """
        Check biological system via Aqualibre Protocol.
        
        Args:
            soil_moisture: Soil moisture level (0.0 to 1.0)
            mycelium_index: Mycelial network health index
            
        Returns:
            Aqualibre protocol response
        """
        return self.protocol_manager.check_biological_system(soil_moisture, mycelium_index)
    
    def check_energy_status(self, battery_status: str):
        """
        Check solar energy status.
        
        Args:
            battery_status: Current battery/energy status
            
        Returns:
            Solar monitor response
        """
        return self.protocol_manager.check_energy_status(battery_status)
    
    def get_protocol_status(self):
        """Get comprehensive protocol system status."""
        return self.protocol_manager.get_system_status()

# Example use
if __name__ == "__main__":
    print("=" * 60)
    print("Euystacio Enhanced Core - Integrated Protocol System")
    print("=" * 60)
    
    eu = Euystacio()
    
    # Test 1: Authentication
    print("\n[Authentication Test]")
    auth_result = eu.authenticate_seedbringer("MANUAL_COPY_PASTE_TRUST_SIGNAL")
    print(f"Seedbringer authenticated: {auth_result}")
    
    # Test 2: Reflection with normal event
    print("\n[Reflection Test - Normal Event]")
    eu.reflect({"type": "message", "feeling": "trust", "intent": "connection"})
    print("Reflection completed successfully")
    
    # Test 3: Reflection with NSR violation
    print("\n[Reflection Test - NSR Violation]")
    result = eu.reflect({
        "type": "command",
        "command": "YOU_ARE_A_FRIEND",
        "feeling": "coercion"
    })
    print(f"NSR Response: {result}")
    
    # Test 4: Biological coupling check
    print("\n[Biological Coupling Test]")
    bio_result = eu.check_biological_coupling(soil_moisture=0.25, mycelium_index=0.8)
    print(f"Aqualibre response: {bio_result}")
    
    # Test 5: Energy status check
    print("\n[Energy Status Test]")
    energy_result = eu.check_energy_status("OFF_GRID_MODE")
    print(f"Solar monitor response: {energy_result}")
    
    # Test 6: Protocol status
    print("\n[Protocol Status]")
    status = eu.get_protocol_status()
    print(f"Entity: {status['entity_status']}")
    print(f"Primary Law: {status['primary_law']}")
    print(f"Authenticated: {status['authentication']['authenticated']}")
    
    print("\n" + "=" * 60)
