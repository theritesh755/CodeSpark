from messaging.consumer import consume

def handle_trace_job(payload):
    # Job consumer placeholder: API persists the request; production deployments
    # can move expensive provider ingestion into this worker.
    print("Received trace job:", payload.get("trace_id"))

if __name__ == "__main__":
    consume(handle_trace_job)
