import h5py
import os
import numpy as np
import warnings

def encode_attr(val):
    if isinstance(val, str):
        return np.bytes_(val)   # explicit, PyCBC-safe
    return val

def combine_hdf5_samples(base_directory, output_filename="combined_results.hdf"):
    """
    Combines the 'samples' datasets and copies all relevant metadata
    from result.hdf files in subdirectories into a single master file.

    Args:
        base_directory (str): The path to the directory containing the 'acc_e_0p*' subdirectories.
        output_filename (str): The name of the new HDF5 file to create.
    """
    combined_samples_data = {}
    # Store attributes and other non-sample data from the *last* processed file,
    # as per your request, assuming they are consistent.
    root_attributes_to_copy = {}
    config_file_content = None # Stores content of /config_file/0
    sampler_info_root_attributes = {}
    sampler_info_datasets = {} # Stores datasets like random_state
    sampler_info_saved_state_content = None # Content of /sampler_info/saved_state/state
    samples_group_attributes = {} # Attributes directly on the /samples group (e.g., lognl)

    # Get a sorted list of directories
    #subdirectories = sorted([d for d in os.listdir(base_directory)
    #                         if os.path.isdir(os.path.join(base_directory, d)) and d.startswith('acc_e_0p')])
    subdirectories = sorted([
    d for d in os.listdir(base_directory)
    if (
        os.path.isdir(os.path.join(base_directory, d)) and
        d.startswith('acc_e_0p') and
        d <= 'acc_e_0p355'
    )
    ])

    if not subdirectories:
        print(f"No subdirectories starting with 'acc_e_0p' found in {base_directory}")
        return

    print(f"Found {len(subdirectories)} subdirectories to process.")

    # First pass: Collect all samples data, and the metadata from the *last* file.
    for i, sub_dir in enumerate(subdirectories):
        full_path = os.path.join(base_directory, sub_dir, "result.hdf")
        if not os.path.exists(full_path):
            print(f"Warning: {full_path} not found. Skipping.")
            continue

        try:
            with h5py.File(full_path, 'r') as f:
                print(f"Processing {full_path}...")

                # Collect root attributes and other groups/datasets from the *last* file
                if i == len(subdirectories) - 1: # Only from the last file
                    # Root attributes
                    for attr_name, attr_value in f.attrs.items():
                        root_attributes_to_copy[attr_name] = attr_value

                    # /config_file/0
                    if 'config_file' in f and '0' in f['config_file']:
                        config_file_content = f['config_file']['0'][()]

                    # /sampler_info and its contents
                    if 'sampler_info' in f:
                        for attr_name, attr_value in f['sampler_info'].attrs.items():
                            sampler_info_root_attributes[attr_name] = attr_value
                        for item_name in f['sampler_info'].keys():
                            item = f['sampler_info'][item_name]
                            if isinstance(item, h5py.Dataset):
                                sampler_info_datasets[item_name] = item[()]
                            elif isinstance(item, h5py.Group) and item_name == 'saved_state':
                                if 'state' in item:
                                    sampler_info_saved_state_content = item['state'][()]

                # Collect samples data from all files
                if 'samples' in f:
                    # Get attributes from the samples group (e.g., 'lognl', 'L1_lognl')
                    if i == len(subdirectories) - 1: # Only from the last file
                        for attr_name, attr_value in f['samples'].attrs.items():
                            samples_group_attributes[attr_name] = attr_value

                    for key in f['samples'].keys():
                        if key not in combined_samples_data:
                            combined_samples_data[key] = []
                        data = f['samples'][key][()] # Read all data into memory
                        combined_samples_data[key].append(data)
                else:
                    print(f"Warning: 'samples' group not found in {full_path}. Skipping.")
        except Exception as e:
            print(f"Error reading {full_path}: {e}. Skipping.")
            continue

    if not combined_samples_data:
        print("No sample data found to combine. Exiting.")
        return

    # Concatenate all lists of arrays into single numpy arrays
    final_combined_samples_data = {key: np.concatenate(value) for key, value in combined_samples_data.items()}

    # Write to the new master HDF5 file
    try:
        with h5py.File(output_filename, 'w') as out_f:
            # Copy root attributes
            for attr_name, attr_value in root_attributes_to_copy.items():
                # Handle numpy strings for older PyCBC versions if necessary
                if isinstance(attr_value, str):
                    out_f.attrs[attr_name] = encode_attr(attr_value)
                else:
                    out_f.attrs[attr_name] = attr_value

            # Explicitly set 'filetype' if it wasn't copied or is incorrect
            if 'filetype' not in out_f.attrs:
                out_f.attrs['filetype'] = np.string_("posterior") # Default to posterior

            # Create and populate /config_file group
            if config_file_content is not None:
                config_group = out_f.create_group('config_file')
                config_group.create_dataset('0', data=config_file_content, compression="gzip")

            # Create and populate /data/L1 group (assuming only L1 based on your h5ls)
            # This part assumes a consistent data structure and only one detector.
            # If you have multiple detectors (H1, V1 etc), this section needs to be expanded
            # to iterate through detectors and their psds/stilde.
            # For simplicity, based on the provided `h5ls`, we'll try to copy L1 from the last file.
            last_file_path = os.path.join(base_directory, subdirectories[-1], "result.hdf")
            with h5py.File(last_file_path, 'r') as f_last:
                if 'data' in f_last and 'L1' in f_last['data']:
                    data_group = out_f.create_group('data')
                    l1_group = data_group.create_group('L1')

                    # Copy stilde
                    if 'stilde' in f_last['data']['L1']:
                        stilde_dset = f_last['data']['L1']['stilde']
                        new_stilde = l1_group.create_dataset('stilde', data=stilde_dset[()],
                                                              dtype=stilde_dset.dtype,
                                                              compression="gzip")
                        for attr_name, attr_value in stilde_dset.attrs.items():
                            if isinstance(attr_value, str):
                                new_stilde.attrs[attr_name] = np.string_(attr_value)
                            else:
                                new_stilde.attrs[attr_name] = attr_value

                    # Copy psds/0
                    if 'psds' in f_last['data']['L1'] and '0' in f_last['data']['L1']['psds']:
                        psds_group = l1_group.create_group('psds')
                        psd0_dset = f_last['data']['L1']['psds']['0']
                        new_psd0 = psds_group.create_dataset('0', data=psd0_dset[()],
                                                              dtype=psd0_dset.dtype,
                                                              compression="gzip")
                        for attr_name, attr_value in psd0_dset.attrs.items():
                            if isinstance(attr_value, str):
                                new_psd0.attrs[attr_name] = np.string_(attr_value)
                            else:
                                new_psd0.attrs[attr_name] = attr_value
                else:
                    warnings.warn("Could not find '/data/L1' in the last HDF5 file. Plotting might fail without data.")


            # Create and populate /sampler_info group
            if sampler_info_root_attributes or sampler_info_datasets or sampler_info_saved_state_content is not None:
                sampler_group = out_f.create_group('sampler_info')
                for attr_name, attr_value in sampler_info_root_attributes.items():
                    if isinstance(attr_value, str):
                        sampler_group.attrs[attr_name] = np.string_(attr_value)
                    else:
                        sampler_group.attrs[attr_name] = attr_value

                for ds_name, ds_data in sampler_info_datasets.items():
                    sampler_group.create_dataset(ds_name, data=ds_data, compression="gzip")

                if sampler_info_saved_state_content is not None:
                    saved_state_group = sampler_group.create_group('saved_state')
                    saved_state_group.create_dataset('state', data=sampler_info_saved_state_content, compression="gzip")


            # Create /samples group and add datasets
            samples_group = out_f.create_group('samples')
            # Add attributes to the /samples group (lognl, L1_lognl)
            for attr_name, attr_value in samples_group_attributes.items():
                if isinstance(attr_value, str):
                    samples_group.attrs[attr_name] = np.string_(attr_value)
                else:
                    samples_group.attrs[attr_name] = attr_value

            for key, data_array in final_combined_samples_data.items():
                samples_group.create_dataset(key, data=data_array, compression="gzip")

        print(f"\nSuccessfully combined samples into {output_filename}")
        print("Combined file structure and dataset sizes:")
        with h5py.File(output_filename, 'r') as check_f:
            def print_attrs(name, obj):
                print(name)
                for key, val in obj.attrs.items():
                    print(f"    - {key}: {val}")
            check_f.visititems(print_attrs)

            print("\nCombined dataset shapes in /samples:")
            for key in check_f['samples'].keys():
                print(f"  /{check_f['samples'][key].name}: {check_f['samples'][key].shape}")

    except Exception as e:
        print(f"Error writing to output file {output_filename}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    base_dir = "/home/lroy02/acceleration_runs/GW200105_runs/runs/"
    combine_hdf5_samples(base_dir, "combined_acc_ecc_samples_pycbc_format_0p355.hdf")

