# run_kira.py
import sys
import os

# Force current directory to be the script path
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.getcwd())

print("--- SYSTEM BOOT SEQUENCE STARTED ---", flush=True)

try:
    print("[1/4] Importing Modules...", flush=True)
    from src.main import KiraController
    print("[2/4] Modules Imported Successfully.", flush=True)

    if __name__ == "__main__":
        print("[3/4] Initializing Controller...", flush=True)
        controller = KiraController()
        
        print("[4/4] Starting Engine... (Window should appear now)", flush=True)
        controller.run()

except KeyboardInterrupt:
    print("\nSystem Shutdown.", flush=True)
except Exception as e:
    # Print the full error
    import traceback
    traceback.print_exc()
    print(f"CRITICAL FAILURE: {e}", flush=True)