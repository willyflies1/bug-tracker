from src import create_app

"""---How-to-run---"""
# 1. C:/.../bug-tracker/src> set FLASK_APP=run.py
# 2. C:/.../bug-tracker/src> flask run -h localhost -p 4995
#       * Currently Twitter Callback function takes site back on port=4995

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=4995)