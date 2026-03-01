import subprocess
import sys

def run_loop():
    for i in range(1, 6):
        print(f"\\n{'='*20} RUN {i} {'='*20}\\n")
        
        result = subprocess.run(["python3", "main.py"])
        
        if result.returncode != 0:
            print(f"\\n❌ Run {i} FAILED. Stopping execution.")
            sys.exit(1)
            
        print(f"\\n✅ Run {i} SUCCESSFUL.\\n")
        
    print(f"\\n🎉 ALL 5 RUNS COMPLETED SUCCESSFULLY WITHOUT ERRORS! 🎉\\n")

if __name__ == "__main__":
    run_loop()
