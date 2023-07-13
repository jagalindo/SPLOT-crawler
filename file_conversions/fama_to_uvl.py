import argparse
import os
from flamapy.core.discover import DiscoverMetamodels

def process_file(input_file_path, output_file_path):
    # Check if the file exists
    if os.path.isfile(input_file_path):
        # Open the file
        with open(input_file_path, 'r') as file:
            dm = DiscoverMetamodels() # Instantiate the class
            #print(dm.get_plugins())
            # Read the content of the input file
            model=dm.use_transformation_t2m(input_file_path,"fm") # Use the transformation to translate the model

            # Open the output file and write the content to it
            dm.use_transformation_m2t(model, output_file_path)
    else:
        print(f"The file {input_file_path} does not exist.")

def main():
    # Create the parser
    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument('input_file_path', help='The path to the input file to process')
    parser.add_argument('output_file_path', help='The path to the output file')

    # Parse the arguments
    args = parser.parse_args()

    # Call the function with the file path
    process_file(args.input_file_path, args.output_file_path)

if __name__ == '__main__':
    main()
