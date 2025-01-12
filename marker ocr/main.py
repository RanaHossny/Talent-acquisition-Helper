import os

def parse_pdf(input_folder, output_folder, workers=4, max_files=10):
    """
    Function to parse PDF files in the specified input folder using the marker tool.

    Args:
    - input_folder (str): Path to the folder containing PDF files to parse.
    - output_folder (str): Path to the folder where output should be saved.
    - workers (int): Number of workers to use (default: 4).
    - max_files (int): Maximum number of files to process (default: 10).
    """
    # Make sure the input and output folders are valid directories
    if not os.path.isdir(input_folder):
        raise ValueError(f"Input folder '{input_folder}' is not a valid directory.")
    if not os.path.isdir(output_folder):
        raise ValueError(f"Output folder '{output_folder}' is not a valid directory.")

    # Construct the marker command as a string with quoted paths
    command = (
        f"marker \"{input_folder}\" --output_dir \"{output_folder}\" "
        f"--workers {workers} --max_files {max_files}"
    )
    print(command)

    try:
        # Execute the command using os.system
        exit_code = os.system(command)
        if exit_code == 0:
            print("PDF parsing completed successfully.")
        else:
            print(f"Marker command failed with exit code: {exit_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Define input and output folder paths
    input_folder = r"D:\Users\rana.hosny\Downloads\gan task\ocr part\marker ocr\Team_CVs"
    output_folder = r"D:\Users\rana.hosny\Downloads\gan task\ocr part\marker ocr\output"
    
    # Call the function to parse PDFs
    parse_pdf(input_folder, output_folder, workers=4, max_files=30)
