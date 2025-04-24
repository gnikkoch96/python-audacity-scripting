import os
import subprocess
import time
from pathlib import Path

try:
    import pyaudacity
except ImportError:
    print("PyAudacity module not found. Please install it with 'pip install pyaudacity'")
    exit(1)


# Define paths
INPUT_FOLDER = Path("./input")
OUTPUT_FOLDER = Path("./output")

# Create output folder if it doesn't exist
OUTPUT_FOLDER.mkdir(exist_ok=True)

# Constants for noise reduction and compression
NOISE_SAMPLE_DURATION = 5  # seconds to sample for noise profile
NOISE_REDUCTION = 10  # dB
NOISE_SENSITIVITY = 2.0
NOISE_FREQUENCY_SMOOTHING = 4
NOISE_ATTACK_DECAY_TIME = 0.15

# Compression settings
THRESHOLD = -30
NOISE_FLOOR = -40
RATIO = 2.5 
ATTACK_TIME = 0.1
RELEASE_TIME = 1.0
MAKEUP_GAIN = 0

def launch_audacity(file_path):
    """
    Launch Audacity with a specific file and return the process handle
    """
    print(f"Opening {file_path} in Audacity...")
    
    # Path to Audacity executable - adjust for your system
    audacity_path = r"C:\Program Files\Audacity\audacity.exe"
    if not Path(audacity_path).exists():
        print(f"Audacity not found at {audacity_path}. Please update the path.")
        return None
    
    # Launch Audacity with the file
    process = subprocess.Popen([audacity_path, str(file_path)])
    
    # Wait for Audacity to start up
    time.sleep(5)
    return process

def close_audacity(process):
    """
    Close the specific Audacity process
    """
    if process:
        print("Closing Audacity...")
        process.terminate()  # Gracefully terminate the process
        process.wait()       # Wait for the process to exit
        print("Audacity closed.")
    else:
        print("No Audacity process to close.")

def process_file(file_path):
    """
    Process the audio file: apply noise reduction and compression
    """

    process = launch_audacity(file_path)

    # Step 3: Select a portion of the audio for the noise profile
    noise_sample_start = 0  # Start time in seconds
    noise_sample_end = NOISE_SAMPLE_DURATION  # End time in seconds
    print(f"Selecting noise sample from {noise_sample_start}s to {noise_sample_end}s...")
    pyaudacity.do(f'SelectTime: Start="{noise_sample_start}" End="{noise_sample_end}"')
    time.sleep(2)

    # Step 4: Get the noise profile
    print("Getting noise profile...")
    pyaudacity.do('NoiseReduction: GetProfile="1"')
    time.sleep(2)

    # Step 5: Select the entire track
    print("Selecting the entire track...")
    pyaudacity.do('SelectAll')
    time.sleep(2)

    # Run Macro
    print("Applying Noise Reduction...")
    pyaudacity.do("Macro_NoiseReductionPython")
    time.sleep(2)

    print("Applying Compression...")
    pyaudacity.do("Macro_CompressorPython")    
    time.sleep(2)

    # Step 8: Export the processed file as WAV
    output_file_path = OUTPUT_FOLDER / file_path.name.replace('.aup3', '_processed.wav')
    print(f"Exporting processed file to {output_file_path}...")

    # Ensure the path is properly formatted
    output_file_path_str = str(output_file_path).replace("\\", "/")  # Use forward slashes for compatibility

    # Check if the file already exists
    if output_file_path.exists():
        print(f"File {output_file_path} already exists. Deleting it...")
        output_file_path.unlink()  # Delete the existing file

    # Send the export command with NumChannels set to 2 (stereo)
    print(f'Sending command: Export2: Filename="{output_file_path_str}" NumChannels=2')
    pyaudacity.do(f'Export2: Filename="{output_file_path_str}" NumChannels=2')
    time.sleep(2)

    print(f"Processed file saved as {output_file_path}.")
    time.sleep(2)

    # Step 9: Close the current project without saving
    close_audacity(process)

def main():
    """
    Main function to process all Audacity files in the input folder
    """
    # Check if input folder exists
    if not INPUT_FOLDER.exists():
        print(f"Input folder '{INPUT_FOLDER}' does not exist.")
        return
        
    # Get all .aup3 files in the input folder
    aup3_files = list(INPUT_FOLDER.glob('*.aup3'))
    
    if not aup3_files:
        print(f"No .aup3 files found in '{INPUT_FOLDER}'")
        return
        
    print(f"Found {len(aup3_files)} files to process.")
    
    for file_path in aup3_files:
        print(f"\nProcessing {file_path.name}...")
        process_file(file_path)
        
        # Wait before processing next file
        time.sleep(5)
        
    print("\nAll files processed.")

if __name__ == "__main__":
    main()

