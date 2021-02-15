import sys
import os
def startup():
    try:
        global application
        def add_to_path(directory):
            if directory not in sys.path:
                sys.path.append(directory)
        app_directory = os.path.dirname(os.path.abspath(__file__))
        add_to_path(app_directory)       
        from common import app as application
    except Exception as e:
        import traceback
        print("{0} Import Error: {1}".format(__file__,e))
        print(traceback.format_exc())
        print("path:{0}".format("\n".join(sys.path)))
        raise(Exception("Import Error"))

if __name__ == '__main__':
    startup()
    application.run(host="0.0.0.0",port=5000,debug=True)
    