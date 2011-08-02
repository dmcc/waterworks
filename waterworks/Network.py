import os, socket

def get_hostname():
    """Returns the simple, unqualified version of a hostname."""
    try:
        name = socket.gethostbyaddr(socket.gethostname())[1][0]
    except: # some network errors can cause the above to fail
        fullname = os.uname()[1]
        name = fullname.split('.')[0]
    return name.lower()
