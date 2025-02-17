import json
import subprocess, time, os

def read_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()
    
def write_file(file_path: str, data: str) -> None:
    with open(file_path, 'w') as file:
        file.write(data)

def get_drives() -> list:

    drives = subprocess.run(
        args=[
            "powershell",
            "-noprofile",
            "-command",
            "Get-WmiObject -Class Win32_LogicalDisk | Select-Object volumename,caption,drivetype | ConvertTo-Json"
        ],
        text=True,
        stdout=subprocess.PIPE
    )

    if drives.returncode != 0 or not drives.stdout.strip():
        print('Failed to enumerate drives')
        return []
    drives = json.loads(drives.stdout)

    data = []

    for i in drives:
        if i["volumename"] == "NEOARK":
            data = i
    
    return data

def run_game(core: str, game: str) -> None:
    os.system(f"C:/NEO-ARK/RetroArch-Win64/retroarch.exe -L {core} -f {game} --verbose")