import argparse
import os
import sys

parser = argparse.ArgumentParser("opentelemetry-exporter")
parser.add_argument("--serviceName", help="The name of the service", type=str)
parser.add_argument("--spanName", help="The name of the span", type=str)
parser.add_argument("--tags", help="(optional) A comma-delimited list of tag=value paris", type=str, required=False)
parser.add_argument("--parentTraceId", help="(optional) The id of the parent trace (hex)", type=str, required=False)
parser.add_argument("--parentSpanId", help="(optional) The id of the parent span (hex)", type=str, required=False)
parser.add_argument("--startTime", help="(optional) Start time (nanos)", type=int, required=False)
parser.add_argument("--endTime", help="(optional) End time (nanos)", type=int, required=False)

args = parser.parse_args()

http_otel_collector = "http://localhost:4318"

args_string = " ".join(sys.argv[1:])
command = f"opentelemetry-instrument \
    --exporter_otlp_protocol http/protobuf  \
    --exporter_otlp_endpoint {http_otel_collector} \
    --traces_exporter otlp \
    --metrics_exporter console \
    --logs_exporter console \
    --service_name {args.serviceName} python tracy.py {args_string}"
print(command)
os.system(command)
