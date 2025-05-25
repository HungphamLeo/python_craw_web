# cmd/main.py
from Deploy import Run

if __name__ == "__main__":
    deploy = Run()
    deploy.run_etl()
