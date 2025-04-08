import logging
import sys

proc_name = "droncast"


def post_fork(server, worker):
    """Configure logging after Gunicorn forks worker processes."""

    # Configure Gunicorn's error logger
    error_logger = logging.getLogger("gunicorn.error")
    error_logger.handlers = []  # Remove default handlers
    handler = logging.StreamHandler(sys.stderr)
    error_logger.addHandler(handler)

    # Configure Gunicorn's access logger
    access_logger = logging.getLogger("gunicorn.access")
    access_logger.handlers = []  # Remove default handlers
    handler = logging.StreamHandler(sys.stdout)
    access_logger.addHandler(handler)


# Use JSON format for access logs
accesslog = "-"  # Log to stdout
errorlog = "-"  # Log to stderr
access_log_format = (
    '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
)
