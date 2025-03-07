import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from gui.app_gui_start import start_app
from gui.DKDE import DKDE

def main():
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    reports_path = os.path.join(downloads, "reports")
    
    if not os.path.exists(reports_path):
        os.makedirs(reports_path)
    
    if os.path.exists(r"assets\coconut.jpeg"):
        start_app()
    else:
        app = DKDE()
        app.mainloop()
    
    

if __name__ == "__main__":
    main()
