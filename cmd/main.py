# cmd/main.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Deploy import Run

if __name__ == "__main__":
    deploy = Run()
    deploy.run_etl()
    #any application, service,...
