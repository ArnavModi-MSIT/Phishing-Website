import multiprocessing

# Gunicorn config
bind = "0.0.0.0:$PORT"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 2

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Memory
max_requests = 1000
max_requests_jitter = 50