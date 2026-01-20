import subprocess
import sys
import platform
import os
import shutil
import json
import tempfile
import zipfile
import tarfile
import datetime

def run_silent_command(command):
    try:
        subprocess.check_call(command, shell=True,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            creationflags=get_creation_flags())
        return True
    except subprocess.CalledProcessError:
        return False

def get_creation_flags():
    if platform.system() == "Windows":
        return subprocess.CREATE_NO_WINDOW
    return 0

def install_pip_packages():
    packages = [
        "pygame",
        "prompt_toolkit",
        "colorama",
        "pyyaml",
        "requests",
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--user", "--quiet"],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                return False
    return True

def download_latest_release_exe():
    try:
        import requests
    except ImportError:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "--quiet"],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            import requests
        except:
            return None
    
    repo_url = "https://api.github.com/repos/D3vUserName/HolyCmd/releases/latest"
    
    try:
        response = requests.get(repo_url, timeout=10)
        response.raise_for_status()
        release_info = response.json()
        
        exe_asset = None
        for asset in release_info.get('assets', []):
            asset_name = asset['name']

            if asset_name.lower() == 'holycmd.exe':
                exe_asset = asset
                break
        
        if not exe_asset:
            print("HolyCmd.exe not found in the latest release")
            for asset in release_info.get('assets', []):
                if asset['name'].lower().endswith('.exe'):
                    exe_asset = asset
                    break
        
        if not exe_asset:
            print("No .exe files found in the release")
            return None
        
        download_url = exe_asset['browser_download_url']
        asset_name = exe_asset['name']
        
        print(f"Found file: {asset_name}")
        return download_exe_file(download_url, asset_name)
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading from GitHub: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def download_exe_file(download_url, filename):
    try:
        import requests
        
        print(f"Downloading {filename}...")

        response = requests.get(download_url, stream=True, timeout=30)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))

        download_path = os.path.join(os.getcwd(), filename)

        if os.path.exists(download_path):
            base, ext = os.path.splitext(filename)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{base}_{timestamp}{ext}"
            download_path = os.path.join(os.getcwd(), filename)
        
        with open(download_path, 'wb') as f:
            if total_size == 0:
                f.write(response.content)
            else:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        percent = (downloaded / total_size) * 100
                        sys.stdout.write(f"\rProgress: {percent:.1f}% ({downloaded/1024/1024:.1f} MB / {total_size/1024/1024:.1f} MB)")
                        sys.stdout.flush()
        
        print(f"\nDownloaded: {download_path}")
        print(f"Size: {os.path.getsize(download_path) / 1024 / 1024:.2f} MB")
        
        return download_path
        
    except Exception as e:
        print(f"\nError downloading file: {e}")
        return None

def find_holycmd():
    import os
    import sys
    import shutil

    found_files = []
    executable_extensions = {'.exe', '.py', '.bat', '.cmd', '.ps1'}
    
    current_dir = os.getcwd()
    for file in os.listdir(current_dir):
        file_lower = file.lower()
        full_path = os.path.join(current_dir, file)
        
        if os.path.isfile(full_path):
            _, ext = os.path.splitext(file_lower)
            if ext not in executable_extensions and not (sys.platform != "win32" and os.access(full_path, os.X_OK)):
                continue
            
            if file_lower == 'holycmd.exe':
                return full_path
            elif file_lower.endswith('.exe') and 'holycmd' in file_lower:
                found_files.append((3, full_path))
            elif file_lower == 'holycmd.py':
                found_files.append((2, full_path))
            elif 'holycmd' in file_lower and ext in executable_extensions:
                found_files.append((1, full_path))
    
    for priority, path in sorted(found_files, reverse=True):
        if priority >= 3:  # .exe file
            return path
    
    if sys.platform == "win32":
        possible_paths = [
            "HolyCmd.exe",
            "holycmd.exe",
            "bin/HolyCmd.exe",
            "bin/holycmd.exe",
            "dist/HolyCmd.exe",
            "dist/holycmd.exe",
            "build/HolyCmd.exe",
            "build/holycmd.exe",
            "release/HolyCmd.exe",
            "release/holycmd.exe",
        ]
        
        user_paths = [
            os.path.expanduser("~/HolyCmd.exe"),
            os.path.expanduser("~/holycmd.exe"),
            os.path.expanduser("~/Desktop/HolyCmd.exe"),
            os.path.expanduser("~/Desktop/holycmd.exe"),
            os.path.expanduser("~/Downloads/HolyCmd.exe"),
            os.path.expanduser("~/Downloads/holycmd.exe"),
        ]
        possible_paths.extend(user_paths)
        
        path_dirs = os.environ.get('PATH', '').split(os.pathsep)
        for path_dir in path_dirs:
            if os.path.isdir(path_dir):
                possible_paths.extend([
                    os.path.join(path_dir, "HolyCmd.exe"),
                    os.path.join(path_dir, "holycmd.exe"),
                ])
        
        program_files = [
            os.environ.get("ProgramFiles", "C:\\Program Files"),
            os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),
        ]
        
        for pf in program_files:
            possible_paths.extend([
                os.path.join(pf, "HolyCmd", "HolyCmd.exe"),
                os.path.join(pf, "HolyCmd", "holycmd.exe"),
                os.path.join(pf, "holycmd", "HolyCmd.exe"),
                os.path.join(pf, "holycmd", "holycmd.exe"),
            ])
    
    else:
        possible_paths = [
            "holycmd",
            "HolyCmd",
            "holycmd.py",
            "HolyCmd.py",
        ]
    
    for path in possible_paths:
        try:
            abs_path = os.path.abspath(os.path.expanduser(path))
            if os.path.exists(abs_path) and os.path.isfile(abs_path):
                filename = os.path.basename(abs_path).lower()
                
                if filename == 'holycmd.exe':
                    return abs_path
                elif filename.endswith('.exe') and 'holycmd' in filename:
                    found_files.append((3, abs_path))
                elif filename == 'holycmd.py':
                    found_files.append((2, abs_path))
        except (OSError, ValueError):
            continue
    
    if found_files:
        found_files.sort(key=lambda x: x[0], reverse=True)
        return found_files[0][1]
    
    return None

def launch_holycmd_in_new_cmd(holycmd_path):
    system = platform.system()
    
    if not holycmd_path or not os.path.exists(holycmd_path):
        print(f"Error: File does not exist: {holycmd_path}")
        return False
    
    print(f"Launching: {holycmd_path}")
    
    if system == "Windows":
        if holycmd_path.lower().endswith('.exe'):
            try:
                subprocess.Popen([holycmd_path], 
                               creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
                return True
            except Exception as e:
                print(f"Error launching .exe: {e}")
                cmd_command = f'start "HolyCmd" "{holycmd_path}"'
                subprocess.Popen(cmd_command, shell=True)
                return True
        elif holycmd_path.lower().endswith('.py'):
            cmd_command = f'start "HolyCmd" python "{holycmd_path}"'
            subprocess.Popen(cmd_command, shell=True)
            return True
        else:
            cmd_command = f'start "HolyCmd" "{holycmd_path}"'
            subprocess.Popen(cmd_command, shell=True)
            return True
    
    elif system in ["Linux", "Darwin"]:
        holycmd_path = holycmd_path.replace(" ", "\\ ")

        if not os.access(holycmd_path, os.X_OK):
            try:
                os.chmod(holycmd_path, 0o755)
            except:
                pass
        
        terminals = [
            ("gnome-terminal", f"gnome-terminal -- {holycmd_path}"),
            ("konsole", f"konsole -e {holycmd_path}"),
            ("xterm", f"xterm -e {holycmd_path}"),
            ("terminator", f"terminator -e '{holycmd_path}'"),
            ("xfce4-terminal", f"xfce4-terminal -e '{holycmd_path}'"),
            ("alacritty", f"alacritty -e {holycmd_path}"),
            ("kitty", f"kitty {holycmd_path}"),
        ]
        
        for term_name, term_command in terminals:
            if shutil.which(term_name):
                subprocess.Popen(term_command, shell=True)
                return True

        try:
            subprocess.Popen([holycmd_path])
            return True
        except:
            return False
    
    return False

def check_if_holycmd_is_running():
    system = platform.system()
    
    if system == "Windows":
        try:
            # Use tasklist to check for HolyCmd processes
            result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq HolyCmd.exe', '/NH'], 
                                  capture_output=True, text=True, creationflags=get_creation_flags())
            if 'HolyCmd.exe' in result.stdout:
                return True
        except:
            pass

    try:
        if system == "Windows":
            result = subprocess.run(['tasklist'], capture_output=True, text=True, 
                                  creationflags=get_creation_flags())
        else:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        
        if 'holycmd' in result.stdout.lower():
            return True
    except:
        pass
    
    return False

def main():
    if sys.version_info < (3, 7):
        print("Python 3.7 or newer is required")
        sys.exit(1)
    
    print("=== HolyCmd Instal;er ===")

    if check_if_holycmd_is_running():
        print("HolyCmd is already running. Exiting installer.")
        sys.exit(0)
    
    print("Installing required packages...")
    if not install_pip_packages():
        print("Failed to install required packages")
        sys.exit(1)
    
    print("\nSearching for HolyCmd.exe in system...")
    holycmd_path = find_holycmd()
    
    if holycmd_path and os.path.exists(holycmd_path):
        filename = os.path.basename(holycmd_path).lower()
        print(f"Found: {holycmd_path}")

        if not filename.endswith('.exe'):
            print(f"WARNING: Found {filename} instead of HolyCmd.exe")
            print("Downloading the latest HolyCmd.exe from GitHub...")
            new_holycmd_path = download_latest_release_exe()
            
            if new_holycmd_path and os.path.exists(new_holycmd_path):
                holycmd_path = new_holycmd_path
                print(f"Downloaded new version: {holycmd_path}")
            else:
                print("Using found file (may be older version)...")
    else:
        print("HolyCmd.exe not found locally.")
        print("Downloading latest version from GitHub...")
        print("Repository: https://github.com/D3vUserName/HolyCmd")
        holycmd_path = download_latest_release_exe()
    
    if holycmd_path and os.path.exists(holycmd_path):
        print(f"\nLaunching HolyCmd...")
        if launch_holycmd_in_new_cmd(holycmd_path):
            print("HolyCmd launched successfully!")
            
            if holycmd_path.lower().endswith('.exe'):
                print("Closing installer...")
                sys.exit(0)
        else:
            print("Error launching HolyCmd")
            sys.exit(1)
    else:
        print("\nFailed to find or download HolyCmd")
        print("You can download it manually from: https://github.com/D3vUserName/HolyCmd/releases")
        print("or install from: https://github.com/D3vUserName/HolyCmd")
        sys.exit(1)

if __name__ == "__main__":
    main()
