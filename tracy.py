import logging
import argparse
import time 

from opentelemetry import trace, context
from opentelemetry.trace import NonRecordingSpan, SpanContext, TraceFlags


parser = argparse.ArgumentParser("opentelemetry-exporter")
parser.add_argument("--serviceName", help="The name of the service", type=str)
parser.add_argument("--spanName", help="The name of the span", type=str)
parser.add_argument("--tags", help="(optional) A comma-delimited list of tag=value paris", type=str, required=False)
parser.add_argument("--parentTraceId", help="(optional) The id of the parent trace (hex)", type=str, required=False)
parser.add_argument("--parentSpanId", help="(optional) The id of the parent span (hex)", type=str, required=False)
parser.add_argument("--startTime", help="(optional) Start time (nanos)", type=int, required=False)
parser.add_argument("--endTime", help="(optional) End time (nanos)", type=int, required=False)

args = parser.parse_args()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
tracer = trace.get_tracer("filtest.tracer")

token = None

if args.parentTraceId:
    span = tracer.start_span(args.spanName)  

    span_context = SpanContext(
        trace_id=int(args.parentTraceId, 16),
        #trace_id=340282366920938463463374607431768211455,
        #trace_id=int(args.parentTraceId),
        span_id=span.get_span_context().span_id,
        is_remote=True,
        trace_flags=TraceFlags(0x01))
    
    ctx = trace.set_span_in_context(NonRecordingSpan(span_context))
    token = context.attach(ctx)

try:
    with tracer.start_as_current_span(args.spanName, 
                                      end_on_exit=False if args.endTime else True ,
                                      start_time=args.startTime if args.startTime else time.time_ns()) as span:
        if args.tags:
            tags = [ pair.split("=") for pair in args.tags.split(",") ] 
            for key, value in tags:
                span.set_attribute(key, value)
        if args.endTime:
            span.end(args.endTime)
finally:
    if token:
        context.detach(token)
        
