from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from rate_limiter import TokenBucketRateLimiter

app = FastAPI(title="API Rate Guard Gateway", version="1.0.0")

# Initialize limiter: 5 tokens max burst, refills 1 token every second
limiter = TokenBucketRateLimiter(capacity=5, refill_rate_per_second=1.0)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Identify client by IP or fallback to client host
    client_ip = request.client.host if request.client else "unknown"
    
    # Check if request has an available token
    allowed, remaining_tokens = limiter.is_allowed(client_id=client_ip, cost=1)
    
    if not allowed:
        # Standard HTTP 429 Too Many Requests response
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "error": "Rate limit exceeded",
                "message": "Too many requests. Please throttle your traffic.",
                "retry_after_seconds": 1
            },
            headers={"Retry-After": "1"}
        )
    
    # If allowed, process request and attach rate-limit telemetry headers
    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(limiter.capacity)
    response.headers["X-RateLimit-Remaining"] = str(remaining_tokens)
    return response

@app.get("/api/v1/resource")
async def get_protected_resource():
    """Sample protected business endpoint."""
    return {
        "status": "success",
        "data": "Operation successful. Protected resource accessed."
    }