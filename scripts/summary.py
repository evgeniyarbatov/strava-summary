import sys
import os
import concurrent

import pandas as pd

from concurrent.futures import ThreadPoolExecutor

from utils import (
    get_gpx_info,
)

def process_file(file_path):
    start_time, activity_type, duration, distance, elevation_gain = get_gpx_info(file_path)
    print(f"{start_time} {activity_type} {duration} {distance} {elevation_gain}")
    return {
        'start': start_time,
        'type': activity_type,
        'duration': duration,
        'distance': distance,
        'elevation': elevation_gain
    }

def main(data_dir, summary_file):
    data = []
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.gpx')]
        
        # Map the process_file function to all files
        future_to_file = {executor.submit(process_file, file): file for file in files}
        
        for future in concurrent.futures.as_completed(future_to_file):
            try:
                file_data = future.result()
                if file_data:
                    data.append(file_data)
            except Exception as e:
                print(f"An error occurred processing {future_to_file[future]}: {e}")
                continue

    df = pd.DataFrame(data)
    df.to_csv(summary_file, index=False)

if __name__ == "__main__":
    main(*sys.argv[1:])