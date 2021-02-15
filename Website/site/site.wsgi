import sys
import os
try:
    def add_to_path(directory):
        if directory not in sys.path:
            sys.path.append(directory)
    app_directory = os.path.dirname(os.path.abspath(__file__))
    from site import startup
    startup()
except ImportError as e:
    print("{0} Import Error: {1}".format(__file__,e))

