"""
OpenTelemetry Configuration for GitHub Gists API
Enables distributed tracing with Tempo integration
"""
import os
from typing import Optional

# OpenTelemetry imports - graceful fallback if not installed
try:
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
    from opentelemetry.instrumentation.logging import LoggingInstrumentor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.propagate import set_global_textmap
    from opentelemetry.propagators.b3 import B3MultiFormat
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False

# Configuration from environment
OTEL_ENABLED = os.environ.get("OTEL_ENABLED", "true").lower() == "true"
OTEL_SERVICE_NAME = os.environ.get("OTEL_SERVICE_NAME", "github-gists-api")
OTEL_EXPORTER_OTLP_ENDPOINT = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://tempo.monitoring.svc.cluster.local:4317")
OTEL_EXPORTER_OTLP_INSECURE = os.environ.get("OTEL_EXPORTER_OTLP_INSECURE", "true").lower() == "true"


def setup_tracing(app=None) -> Optional[trace.Tracer]:
    """
    Configure OpenTelemetry tracing for the application.
    
    Returns:
        Tracer instance if successful, None otherwise
    """
    if not OTEL_AVAILABLE:
        print("⚠️  OpenTelemetry packages not installed. Tracing disabled.")
        print("   Install with: pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-grpc")
        print("                 pip install opentelemetry-instrumentation-fastapi opentelemetry-instrumentation-httpx")
        return None
    
    if not OTEL_ENABLED:
        print("ℹ️  OpenTelemetry disabled via OTEL_ENABLED=false")
        return None
    
    try:
        # Create resource with service info
        resource = Resource.create({
            "service.name": OTEL_SERVICE_NAME,
            "service.version": "1.0.0",
            "deployment.environment": os.environ.get("ENVIRONMENT", "production"),
            "service.namespace": os.environ.get("POD_NAMESPACE", "default"),
            "service.instance.id": os.environ.get("POD_NAME", "unknown"),
        })
        
        # Create tracer provider
        tracer_provider = TracerProvider(resource=resource)
        
        # Configure OTLP exporter (sends to Tempo)
        otlp_exporter = OTLPSpanExporter(
            endpoint=OTEL_EXPORTER_OTLP_ENDPOINT,
            insecure=OTEL_EXPORTER_OTLP_INSECURE,
        )
        
        # Add batch processor for efficiency
        span_processor = BatchSpanProcessor(otlp_exporter)
        tracer_provider.add_span_processor(span_processor)
        
        # Set global tracer provider
        trace.set_tracer_provider(tracer_provider)
        
        # Use B3 propagation format (compatible with Istio)
        set_global_textmap(B3MultiFormat())
        
        # Auto-instrument FastAPI
        if app is not None:
            FastAPIInstrumentor.instrument_app(app)
            print(f"✅ FastAPI instrumented for tracing")
        
        # Auto-instrument HTTPX (outgoing HTTP calls)
        HTTPXClientInstrumentor().instrument()
        print(f"✅ HTTPX instrumented for tracing")
        
        # Auto-instrument logging (adds trace context to logs)
        LoggingInstrumentor().instrument(set_logging_format=True)
        print(f"✅ Logging instrumented with trace context")
        
        print(f"🔍 OpenTelemetry tracing configured:")
        print(f"   Service: {OTEL_SERVICE_NAME}")
        print(f"   Exporter: {OTEL_EXPORTER_OTLP_ENDPOINT}")
        
        return trace.get_tracer(OTEL_SERVICE_NAME)
    
    except Exception as e:
        print(f"⚠️  Failed to configure OpenTelemetry: {e}")
        return None


def get_tracer() -> trace.Tracer:
    """Get the configured tracer instance."""
    if not OTEL_AVAILABLE:
        return None
    return trace.get_tracer(OTEL_SERVICE_NAME)


def create_span(name: str, attributes: dict = None):
    """
    Create a new span for custom instrumentation.
    
    Usage:
        with create_span("operation_name", {"key": "value"}) as span:
            # Your code here
            span.set_attribute("result", "success")
    """
    if not OTEL_AVAILABLE:
        from contextlib import nullcontext
        return nullcontext()
    
    tracer = get_tracer()
    if tracer is None:
        from contextlib import nullcontext
        return nullcontext()
    
    span = tracer.start_as_current_span(name)
    if attributes:
        for key, value in attributes.items():
            span.set_attribute(key, value)
    return span


# Decorator for tracing functions
def traced(name: str = None, attributes: dict = None):
    """
    Decorator to automatically trace a function.
    
    Usage:
        @traced("fetch_gists")
        async def fetch_gists(username: str):
            ...
    """
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            span_name = name or func.__name__
            with create_span(span_name, attributes):
                return await func(*args, **kwargs)
        
        def sync_wrapper(*args, **kwargs):
            span_name = name or func.__name__
            with create_span(span_name, attributes):
                return func(*args, **kwargs)
        
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator
