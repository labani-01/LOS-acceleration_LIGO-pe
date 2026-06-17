import os
import subprocess
import time

base_dir = os.path.expanduser(
    '/home/lroy02/acceleration_runs/GW200105_runs/runs'
)

for dirname in sorted(os.listdir(base_dir)):
    dirpath = os.path.join(base_dir, dirname)
    run_file = os.path.join(dirpath, 'run.sh')

    if os.path.isdir(dirpath) and os.path.isfile(run_file):
        print(f"[INFO] Submitting job in: {dirname}")
        try:
            result = subprocess.run(
                ['sbatch', 'run.sh'],
                cwd=dirpath,
                check=True,
                capture_output=True,
                text=True
            )
            print(result.stdout.strip())

            time.sleep(0.1)

        except subprocess.CalledProcessError as e:
            print(f"[ERROR]-Failed to submit job in {dirname}")
            print(e.stderr.strip())

            time.sleep(0.1)

    else:
        print(f"[SKIP]-No run.sh in {dirname}")
