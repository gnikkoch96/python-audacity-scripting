import subprocess

# Replace with the actual path to Audacity and the .aup3 file
audacity_path = "C:\\Program Files\\Audacity\\audacity.exe"
file_path = "D:\\Github\\python-audacity-scripting\\input\\test.aup3"

subprocess.Popen([audacity_path, file_path])
