def _red_code_protocol(self, reason: str):
    """ Red-Code-Log-Detailierung vor Shutdown """
    log_data = {
        "timestamp": time.time(),
        "reason": reason,
        "current_vectors": list(self.vs.vectors.items())
    }
    with open("red_code_log.json", "w") as log_file:
        import json
        json.dump(log_data, log_file)

    print("\n[RED CODE LOGGING]: Systemzustand gesichert.")
    raise SystemExit(0)
