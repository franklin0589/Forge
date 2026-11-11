import math
import numpy as np
import os
import subprocess

def find_bezier_control_points(p0, p3, s1, s2, t1, t2):
    """
    Finds cubic Bézier control points P1 and P2 given endpoints and intermediate samples.
    
    Parameters:
    p0, p3 : Tuples/Lists of (x, y) for the start and end coordinates of the curve.
    s1, s2 : Tuples/Lists of (x, y) for the target path sample points.
    t1, t2 : Floats (0 < t < 1) representing the parameter values at s1 and s2.
    """
    # 1. Build the 2x2 coefficient matrix M
    M = np.array([
        [3 * (1 - t1)**2 * t1, 3 * (1 - t1) * t1**2],
        [3 * (1 - t2)**2 * t2, 3 * (1 - t2) * t2**2]
    ])
    
    # 2. Build the constants vector Y for the X dimension
    Y_x = np.array([
        s1[0] - (1 - t1)**3 * p0[0] - t1**3 * p3[0],
        s2[0] - (1 - t2)**3 * p0[0] - t2**3 * p3[0]
    ])
    
    # 3. Build the constants vector Y for the Y dimension
    Y_y = np.array([
        s1[1] - (1 - t1)**3 * p0[1] - t1**3 * p3[1],
        s2[1] - (1 - t2)**3 * p0[1] - t2**3 * p3[1]
    ])
    
    # 4. Solve the linear matrix equations M * P = Y
    p1_x, p2_x = np.linalg.solve(M, Y_x)
    p1_y, p2_y = np.linalg.solve(M, Y_y)
    
    # Return the control points as discrete coordinate tuples
    return (p1_x, p1_y), (p2_x, p2_y)




def ffmpeg_stitch_videos(video_folder, output_filename):
    # Find and sort all MP4 files
    video_files = sorted([f for f in os.listdir(video_folder) if f.endswith('.mp4')])
    
    if not video_files:
        print("No MP4 files found.")
        return

    list_file_path = os.path.join(video_folder, "files_to_merge.txt")
    
    # Create the text file that FFmpeg expects
    with open(list_file_path, "w", encoding="utf-8") as f:
        for video in video_files:
            # Escape single quotes in filenames if any exist
            safe_name = video.replace("'", "'\\''")
            f.write(f"file '{safe_name}'\n")
            
    # Run the FFmpeg concat command
    # -c copy tells FFmpeg to stream-copy instead of re-encoding
    try:
        command = [
            "ffmpeg", "-f", "concat", "-safe", "0", 
            "-i", list_file_path, "-c", "copy", output_filename
        ]
        subprocess.run(command, check=True)
        print(f"Successfully created {output_filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error during FFmpeg merging: {e}")
    finally:
        # Clean up the temporary text file
        if os.path.exists(list_file_path):
            os.remove(list_file_path)
