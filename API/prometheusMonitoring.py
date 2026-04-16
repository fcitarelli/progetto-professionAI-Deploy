from fastapi import Request
from prometheus_client import Counter, Histogram
import time


REQUEST_COUNT = Counter(
    'api_requests_total',
    'Total API Requests',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'api_latency_seconds',
    'API Latency'
)

async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    latency = time.time() - start_time
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        http_status=response.status_code
    ).inc()
    
    REQUEST_LATENCY.observe(latency)
    
    return response

