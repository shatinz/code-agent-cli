import subprocess

def execute_shell_command(command: str) -> str:
    """
    Executes a shell command directly on the host (Windows PowerShell).
    Use this to run system commands, pip installs, or file system operations.
    """
    try:
        # Run command using powershell
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, timeout=120)
        output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}\nRETURN_CODE: {result.returncode}"
        return output
    except Exception as e:
        return f"Error executing command: {str(e)}"

def execute_python_code(code: str) -> str:
    """
    Executes Python code safely by saving it to a temporary file and running it.
    The code should be a full valid python script.
    """
    import tempfile
    import os
    try:
        tmp_fd, tmp_path = tempfile.mkstemp(suffix=".py")
        with os.fdopen(tmp_fd, 'w') as f:
            f.write(code)
            
        result = subprocess.run(["python", tmp_path], capture_output=True, text=True, timeout=120)
        os.remove(tmp_path)
        output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}\nRETURN_CODE: {result.returncode}"
        return output
    except Exception as e:
        return f"Error executing python code: {str(e)}"
