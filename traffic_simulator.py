import httpx
import time
from typing import List, Dict, Any

class TrafficSimulator:
    def __init__(self, target_url: str = "http://127.0.0.1:8000/api/v1/resource"):
        self.target_url = target_url

    def send_burst_traffic(self, total_requests: int = 10, delay_between_requests: float = 0.1) -> List[Dict[str, Any]]:
        """
        Simulates high-frequency incoming API traffic.
        """
        logs = []
        with httpx.Client(timeout=5.0) as client:
            for seq in range(1, total_requests + 1):
                timestamp = time.strftime("%H:%M:%S")
                try:
                    response = client.get(self.target_url)
                    remaining = response.headers.get("X-RateLimit-Remaining", "0")
                    logs.append({
                        "request_seq": seq,
                        "time": timestamp,
                        "status_code": response.status_code,
                        "remaining_tokens": remaining,
                        "outcome": "PASSED" if response.status_code == 200 else "BLOCKED (429)"
                    })
                except Exception as ex:
                    logs.append({
                        "request_seq": seq,
                        "time": timestamp,
                        "status_code": 0,
                        "remaining_tokens": "N/A",
                        "outcome": f"ERROR: {str(ex)}"
                    })
                
                time.sleep(delay_between_requests)
        return logs