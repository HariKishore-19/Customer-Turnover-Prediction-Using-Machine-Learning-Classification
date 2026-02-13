import subprocess
import sys

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✓ Success")
        return True
    else:
        print(f"✗ Failed: {result.stderr}")
        return False

print("=" * 50)
print("Installing Telco Churn Predictor Dependencies")
print("=" * 50)

# Order matters for Windows
commands = [
    "python -m pip install --upgrade pip",
    "pip install wheel",
    "pip install numpy==1.23.5 --only-binary=:all:",
    "pip install pandas==1.5.3 --only-binary=:all:",
    "pip install scikit-learn==1.2.2 --only-binary=:all:",
    "pip install Flask==2.3.3"
]

all_success = True
for cmd in commands:
    if not run_command(cmd):
        all_success = False
        print(f"\nStopping at failed command: {cmd}")
        break

if all_success:
    print("\n" + "=" * 50)
    print("✅ ALL PACKAGES INSTALLED SUCCESSFULLY!")
    print("=" * 50)
    print("\nNow run: python app.py")
    print("Then open: http://localhost:5000")
else:
    print("\n" + "=" * 50)
    print("❌ INSTALLATION FAILED")
    print("=" * 50)
    print("\nTry Solution 4 (Anaconda) instead.")