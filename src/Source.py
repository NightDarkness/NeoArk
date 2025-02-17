import subprocess, os, pystray, threading, time
from PIL import Image
from modules import toolbox as tb
class NeoArk:
    def __init__(self):
        self.app_name = "NeoArk"
        self.info = {"Device": None, "Console": None, "Game": None, "Core": None, "Status": "No cartdrige"}
        self.icon = Image.open("res/Images/Icon.png")
        self.menu = pystray.Menu(
            pystray.MenuItem(f"{self.app_name}", lambda: None),
            pystray.MenuItem(f"Status: {self.info['Status']}", lambda: None),
            pystray.MenuItem(f"{self.info['Console']} : {self.info['Game']}", lambda: None),
            pystray.MenuItem(f"Core : {self.info['Core']}", lambda: None),
            pystray.MenuItem("Exit", self.exit)
        )
        self.tray = pystray.Icon(self.app_name, self.icon, "NeoArk", menu=self.menu)

    def cartdrige_listener(self):

        cache = []
        
        while True:

            drives = tb.get_drives()

            if len(drives) > 0 and len(cache) == 0:
                #os.system("cls")
                cache = drives
                print(f"Drives updated\n\n{drives}")

                try:
                    
                    file_data = tb.read_file(drives["caption"] + "DATA.ark")

                    data_lines = file_data.split("\n")

                    self.info["Status"] = "Cartdrige detected"
                    self.info["Device"] = drives["caption"] + "/"
                    self.info["Game"] = data_lines[2].split("=")[1]
                    self.info["Core"] = data_lines[3].split("=")[1]
                    self.info["Console"] = data_lines[4].split("=")[1]

                    #tb.write_file("C:\NEO-ARK\DATA.ark", self.info)

                    tb.run_game(self.info["Core"], self.info["Game"])
                except:
                    print("Error al leer la informacion del cartucho")

            else:
                if len(drives) == 0:
                    cache = []
                self.info["Status"] = "No cartdrige"

            time.sleep(1)


    def run(self):
        threading.Thread(target=self.cartdrige_listener, daemon=True).start()
        self.tray.run()

    def exit(self):
        self.info = {"Device": None, "Console": None, "Game": None, "Core": None, "Status": "No cartdrige"}
        #tb.write_file("C:\NEO-ARK\DATA.ark", self.info)
        self.tray.stop()
        os._exit(0)


if __name__ == "__main__":
    app = NeoArk()
    app.run()