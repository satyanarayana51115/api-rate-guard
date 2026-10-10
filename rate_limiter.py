import time
from typing import Dict, Tuple

class TokenBucketRateLimiter:
    """
    In-memory Token Bucket rate limiting engine.
    Controls inbound request rates per client identifier.
    """
    def __init__(self, capacity: int = 5, refill_rate_per_second: float = 1.0):
        # Maximum burst capacity of the bucket
        self.capacity = capacity
        # Rate at which tokens are replenished per second
        self.refill_rate = refill_rate_per_second
        # In-memory storage mapping client_id -> (tokens_left, last_updated_timestamp)
        self.buckets: Dict[str, Tuple[float, float]] = {}

    def _refill(self, client_id: str) -> float:
        """Calculates token accrual based on elapsed time since last request."""
        current_time = time.time()
        
        if client_id not in self.buckets:
            # First request from this client: initialize with full capacity
            self.buckets[client_id] = (float(self.capacity), current_time)
            return float(self.capacity)

        tokens, last_time = self.buckets[client_id]
        elapsed = current_time - last_time

        # Calculate accrued tokens based on time passed
        new_tokens = min(float(self.capacity), tokens + (elapsed * self.refill_rate))
        self.buckets[client_id] = (new_tokens, current_time)
        return new_tokens

    def is_allowed(self, client_id: str, cost: int = 1) -> Tuple[bool, int]:
        """
        Evaluates whether a request can proceed.
        Returns:
            Tuple[bool, int]: (Allowed boolean, Remaining tokens)
        """
        available_tokens = self._refill(client_id)
        current_time = self.buckets[client_id][1]

        if available_tokens >= cost:
            # Deduct token and grant access
            remaining = available_tokens - cost
            self.buckets[client_id] = (remaining, current_time)
            return True, int(remaining)
        
        # Insufficient tokens: block request
        return False, int(available_tokens)