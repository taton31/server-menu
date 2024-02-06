from app import app
from uvicorn import run
# import unicorn
if __name__ == "__main__":
    # run("main:app", host="127.0.0.1", port=61854)
    run(app, host="192.168.3.39", port=61854)
