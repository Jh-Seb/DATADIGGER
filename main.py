import os
import sys
from gui.app_gui import APPGUI
from gui.app_gui import DKDE

def main():
    if os.path.exists(r"coco.jpeg"): 
        app = APPGUI()
    else:
        app = DKDE()
    
    app.mainloop()

if __name__ == "__main__":
    main()
