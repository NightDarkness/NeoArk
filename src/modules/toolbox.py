import subprocess, time, os

def read_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()
    
def write_file(file_path: str, data: str) -> None:
    with open(file_path, 'w') as file:
        file.write(data)

def get_drives() -> list:
    devices = subprocess.check_output("wmic logicaldisk get volumename", shell=True).decode("utf-8")
    devices = devices.replace("\r", "").replace("  ","").split("\n")
    data = []

    for i in devices:
        if i.endswith(" "):
            i = i[:-1]
        if i != "" and i != "VolumeName":
            data.append(i)
    
    return data
    
def get_drive_caption(drive_name: str) -> str:
    return subprocess.check_output(f"wmic logicaldisk where \"volumename='{drive_name}'\" get caption", shell=True).decode("utf-8").split("\n")[1][0:2]

def run_game(core: str, game: str) -> None:
    os.system(f"C:/NEO-ARK/RetroArch-Win64/retroarch.exe -L {core} -f {game} --verbose")