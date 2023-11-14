# Code Structure for Portfolio Performance Calculator

# 1. **Main Modules**
# - Data Handling
# - Portfolio Calculations
# - Visualization (optional)
# - Execution Summary

# Strategies:
# - Use object-oriented programming (OOP) for scalability.
# - Ensure modularity: each class should handle one specific aspect of the system.
# - Use pandas for data manipulation and analysis.
# - Save intermediary results to avoid recalculating large datasets.

# Class Structure

from ExtraitReader import ReadMidas
import os

def list_files_in_midas_folder():
    folder_path = 'data/midas'
    files = os.listdir(folder_path)
    return files

# Example Usage
if __name__ == "__main__":

    all_transactions = list()
    file_list = list_files_in_midas_folder()

    midas_reader = ReadMidas()
    for item in file_list:
        if ".pdf" in item:
            trans_list = midas_reader.read_excrait_data("data/midas/" + item)

            for trans in trans_list:
                all_transactions.append(trans)
        
    for item in all_transactions:
        print(item)

        

