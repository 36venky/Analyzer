import subprocess
import glob
import os

def run_all_analyzers():
    # Find all scripts that start with "Analyzer_" in the current folder
    scripts = glob.glob("mod_*.py")

    if not scripts:
        print("⚠️ No Analyzer_*.py files found!")
        return

    processes = []
    for script in scripts:
        p = subprocess.Popen(["python", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes.append(p)

    print("✅ All analyzers are now running concurrently!")

    # Keep the master script alive
    for p in processes:
        p.wait()

if __name__ == "__main__":
    run_all_analyzers()
