from threading import Lock


log_lock = Lock()


def log(*args):

    with log_lock:
        print(*args)