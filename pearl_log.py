from datetime import datetime

def pearlize(event):
    with open("PEARL_LOG.md", "a") as log:
        log.write(f"- {datetime.now()} :: {event}\n")

