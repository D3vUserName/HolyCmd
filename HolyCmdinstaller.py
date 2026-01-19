import subprocess
import sys
import platform
import os
import shutil

def run_silent_command(command):
    try:
        subprocess.check_call(command, shell=True,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            creationflags=get_creationflags())
        return True
    except subprocess.CalledProcessError:
        return False

def get_creationflags():
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

def find_holycmd():
    import os
    import sys
    import shutil
    
    if sys.platform == "win32":
        valid_extensions = ['.exe', '.py', '.bat', '.cmd']
        target_names = ['holycmd', 'HolyCmd']
    else:
        valid_extensions = ['', '.py', '.sh', '.out']
        target_names = ['holycmd', 'HolyCmd', 'holycmd.py']
    
    possible_paths = [
        "HolyCmd.exe",
        "holycmd.exe",
        "holycmd",
        "HolyCmd",
        "holycmd.py",
        "HolyCmd.py",
        "./HolyCmd.exe",
        "./holycmd.exe",
        "./holycmd",
        "./HolyCmd",
        "bin/HolyCmd.exe",
        "bin/holycmd.exe",
        "bin/holycmd",
        "bin/HolyCmd",
        "src/HolyCmd.exe",
        "src/holycmd.exe",
        "src/holycmd",
        "src/HolyCmd",
        "app/HolyCmd.exe",
        "app/holycmd.exe",
        "app/holycmd",
        "app/HolyCmd",
        "dist/HolyCmd.exe",
        "dist/holycmd.exe",
        "dist/holycmd",
        "dist/HolyCmd",
        "build/HolyCmd.exe",
        "build/holycmd.exe",
        "build/holycmd",
        "build/HolyCmd",
        "release/HolyCmd.exe",
        "release/holycmd.exe",
        "release/holycmd",
        "release/HolyCmd",
        "../HolyCmd.exe",
        "../holycmd.exe",
        "../holycmd",
        "../HolyCmd",
        "../holycmd.py",
        "../../HolyCmd.exe",
        "../../holycmd.exe",
        "../../holycmd",
        "../../HolyCmd",
        
        os.path.expanduser("~/HolyCmd.exe"),
        os.path.expanduser("~/holycmd.exe"),
        os.path.expanduser("~/holycmd"),
        os.path.expanduser("~/HolyCmd"),
        os.path.expanduser("~/Desktop/HolyCmd.exe"),
        os.path.expanduser("~/Desktop/holycmd.exe"),
        os.path.expanduser("~/Desktop/holycmd"),
        os.path.expanduser("~/Desktop/HolyCmd"),
        os.path.expanduser("~/Documents/HolyCmd.exe"),
        os.path.expanduser("~/Documents/holycmd.exe"),
        os.path.expanduser("~/Documents/holycmd"),
        os.path.expanduser("~/Documents/HolyCmd"),
        os.path.expanduser("~/Downloads/HolyCmd.exe"),
        os.path.expanduser("~/Downloads/holycmd.exe"),
        os.path.expanduser("~/Downloads/holycmd"),
        os.path.expanduser("~/Downloads/HolyCmd"),
    ]
    
    path_dirs = os.environ.get('PATH', '').split(os.pathsep)
    for path_dir in path_dirs:
        if os.path.isdir(path_dir):
            for target in target_names:
                for ext in valid_extensions:
                    possible_paths.append(os.path.join(path_dir, target + ext))
    
    if sys.platform == "win32":
        program_files = [
            os.environ.get("ProgramFiles", "C:\\Program Files"),
            os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),
            os.environ.get("LocalAppData", os.path.expanduser("~\\AppData\\Local")),
        ]
        
        for pf in program_files:
            for target in target_names:
                possible_paths.extend([
                    os.path.join(pf, target, "HolyCmd.exe"),
                    os.path.join(pf, target, "holycmd.exe"),
                    os.path.join(pf, target, target + ".exe"),
                    os.path.join(pf, target, "bin", "HolyCmd.exe"),
                    os.path.join(pf, target, "bin", "holycmd.exe"),
                ])
    else:
        unix_paths = [
            "/usr/local/bin",
            "/usr/bin",
            "/bin",
            "/opt",
            "/opt/holycmd",
            "/usr/local/share",
            "/usr/share",
        ]
        
        for upath in unix_paths:
            for target in target_names:
                possible_paths.append(os.path.join(upath, target))
    
    checked_paths = set()
    
    for path in possible_paths:
        try:
            abs_path = os.path.abspath(os.path.expanduser(path))
            
            if abs_path in checked_paths:
                continue
            checked_paths.add(abs_path)
            
            if os.path.exists(abs_path):
                if os.path.isfile(abs_path):
                    filename = os.path.basename(abs_path).lower()

                    if any(target in filename for target in ['holycmd', 'holy-cmd']):
                        return abs_path
                    
                    name_without_ext, ext = os.path.splitext(filename)
                    if name_without_ext in ['holycmd', 'holy-cmd']:
                        return abs_path
                    
                    if ext == '.exe':
                        exe_name = name_without_ext.replace('-', '').replace('_', '').lower()
                        if exe_name == 'holycmd':
                            return abs_path
                
                elif os.path.isdir(abs_path):
                    try:
                        files = os.listdir(abs_path)
                        for file in files:
                            file_lower = file.lower()
                            if any(name in file_lower for name in ['holycmd.exe', 'holycmd', 'holy-cmd']):
                                candidate = os.path.join(abs_path, file)
                                if os.path.isfile(candidate):
                                    return os.path.abspath(candidate)
                    except (PermissionError, OSError):
                        continue
        
        except (OSError, ValueError):
            continue
    
    search_roots = [
        os.getcwd(),
        os.path.dirname(os.getcwd()),
        os.path.expanduser("~"),
    ]

    excluded_dirs = {'.git', '__pycache__', 'node_modules', 'venv', '.venv', 'env'}
    max_depth = 3
    
    def recursive_search(current_path, depth=0):
        if depth >= max_depth:
            return None
        
        try:
            for item in os.listdir(current_path):
                item_path = os.path.join(current_path, item)

                if item.startswith('.') or item in excluded_dirs:
                    continue
                
                if os.path.isfile(item_path):
                    item_lower = item.lower()
                    if (item_lower in ['holycmd.exe', 'holycmd', 'holy-cmd.exe', 'holy-cmd'] or
                        item_lower.endswith(('.exe', '.py', '.sh')) and 
                        'holycmd' in item_lower.replace('-', '').replace('_', '')):
                        return os.path.abspath(item_path)
                
                elif os.path.isdir(item_path):
                    result = recursive_search(item_path, depth + 1)
                    if result:
                        return result
        
        except (PermissionError, OSError):
            pass
        
        return None
    
    for root in search_roots:
        if os.path.exists(root):
            result = recursive_search(root)
            if result:
                return result

    for target in target_names:
        try:
            which_path = shutil.which(target)
            if which_path and os.path.exists(which_path):
                return os.path.abspath(which_path)
        except Exception:
            continue
    
    return None

def launch_holycmd_in_new_cmd(holycmd_path):
    system = platform.system()
    
    if system == "Windows":
        cmd_command = f'start "HolyCmd" cmd /k "{holycmd_path}"'
        subprocess.Popen(cmd_command, shell=True)
        return True
        
    elif system == "Linux" or system == "Darwin":
        holycmd_path = holycmd_path.replace(" ", "\\ ")
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
            os.chmod(holycmd_path, 0o755)
            subprocess.Popen([holycmd_path])
            return True
        except:
            return False
    
    return False

def main():
    if sys.version_info < (3, 7):
        sys.exit(1)
    
    if not install_pip_packages():
        sys.exit(1)
    
    holycmd_path = find_holycmd()
    
    if holycmd_path and os.path.exists(holycmd_path):
        launch_holycmd_in_new_cmd(holycmd_path)
        
        sys.exit(0)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
