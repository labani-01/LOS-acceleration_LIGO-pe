import os
import shutil

step = 0.005
ecc_min = 0.0
ecc_max = 0.200

base_config_path = "base/common_config.ini"
base_run_path = "base/run.sh"
output_parent_dir = "runs"

base_abs_dir = "/home/lroy02/acceleration_runs/GW200105_runs/runs"
logs_dir = "/home/lroy02/acceleration_runs/GW200105_runs/logs"

num_bins = int((ecc_max - ecc_min) / step)

for i in range(num_bins):
    current = round(ecc_min + i * step, 5)
    next_val = round(current + step, 5)

    folder_name = f"acc_e_{current:.3f}".replace(".", "p")
    new_dir = os.path.join(output_parent_dir, folder_name)
    os.makedirs(new_dir, exist_ok=True)

    # -------- CONFIG FILE --------
    new_config_path = os.path.join(new_dir, "config.ini")
    shutil.copy(base_config_path, new_config_path)

    with open(new_config_path, "r") as f:
        lines = f.readlines()

    with open(new_config_path, "w") as f:
        in_ecc_block = False
        for line in lines:
            if line.strip().startswith("[prior-eccentricity]"):
                in_ecc_block = True
                f.write(line)
                continue
            if in_ecc_block:
                if line.strip().startswith("min-eccentricity"):
                    f.write(f"min-eccentricity = {current:.5f}\n")
                elif line.strip().startswith("max-eccentricity"):
                    f.write(f"max-eccentricity = {next_val:.5f}\n")
                elif line.strip().startswith("[") and line.strip().endswith("]"):
                    in_ecc_block = False
                    f.write(line)
                else:
                    f.write(line)
            else:
                f.write(line)

    # RUN.SH
    run_dst = os.path.join(new_dir, "run.sh")
    with open(base_run_path, "r") as f:
        run_lines = f.readlines()

    config_abs = os.path.join(base_abs_dir, folder_name, "config.ini")
    result_abs = os.path.join(base_abs_dir, folder_name, "result.hdf")

    job_name = folder_name
    log_file = f"{folder_name}.out"

    with open(run_dst, "w") as f:
        for line in run_lines:

        # SBATCH replacements
            if line.startswith("#SBATCH --job-name"):
                f.write(f"#SBATCH --job-name={job_name}\n")

            elif line.startswith("#SBATCH --output"):
                log_path = os.path.join(logs_dir, log_file)
                f.write(f"#SBATCH --output={log_path}\n")

        # PyCBC replacements
            elif "--config-file" in line:
                f.write(f"\t--config-file {config_abs} \\\n")

            elif "--output-file" in line:
                f.write(f"\t--output-file {result_abs} \\\n")

            else:
                f.write(line)


print("All config, run, and submit files generated in 'runs/'")
