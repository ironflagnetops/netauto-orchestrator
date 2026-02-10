import json,os,datetime
from csv import writer,DictReader

#------------------------------------------------------------------------------------------------------------------------#
#   DATA OUT - JSON                                                                                                      #
#------------------------------------------------------------------------------------------------------------------------#
# Write Python dict or list out to JSON
#
#   @param  data_output             Dict or list object to be output
#   @param  output_filename         Name of file to be created
#   @param  output_dir              Name of directory to store created file (will )

def write_json_out(data_output,output_filename,output_dir='data_out'):

    print('\n--> Serializing JSON')
    json_object = json.dumps(data_output, indent=4)

    # Writing to sample.json
    print('--> Writing JSON\n\n')
    with open(f"data_out/{output_filename}.json", "w") as outfile:
        outfile.write(json_object)

#------------------------------------------------------------------------------------------------------------------------#
#   DATA OUT - TEXT                                                                                                      #
#------------------------------------------------------------------------------------------------------------------------#
# Create and Write output to plain text file. Will create directory and file if not already existing.
#
#   @param  output_dir              Name of directory to store created file (will )
#   @param  output_filename         Name of file to be created
#   @bool   timestamp               Will add a timestamp to the filename in order not to overwrite prior output files
#
#   TODO: Rewrite function so you have more control over the output directory

def output_gen_text(output_dir='',output_filename='',timestamp=True):
    
    # Defines the current working directory file path  
    current_dir = os.getcwd()

    # Asks user to name of output directory
    if output_dir == '':
        output_dir = input("\nOutput Folder Name: ")
    output_folder_name = "{}/{}/".format(current_dir,output_dir)
    
    # If output directory does NOT exist, it is created
    if not os.path.exists(output_folder_name):
        os.makedirs(output_folder_name)

    # Asks user to name of output file (e.g., 'routerACL')
    if output_filename == '':
        output_filename = input("Output File Name: ")
    print()

    if timestamp == True:
        # Calculates the current time at runtime and formats to yyyymmdd_hhmmss
        x = datetime.datetime.now()
        fileTime = x.strftime("%Y%m%d_%H%M%S")

        # Compiles the output string from the folder creation code block, the variable 'output_filename',
        #   and the generated 'fileTime' variable
        txt_out = ("{}{}_{}.txt".format(output_folder_name,output_filename,fileTime))
    else:
        txt_out = ("{}{}.txt".format(output_folder_name,output_filename))
    
    # Opens the output file using variable 'txt_out' and is ready to write lines
    #   Example: write_output = bse_output_gen_text()
    #            write_output.write('')
    txt_output = open(txt_out, "a")

    return(txt_output)

#------------------------------------------------------------------------------------------------------------------------#
#   DATA OUT - TEXT                                                                                                      #
#------------------------------------------------------------------------------------------------------------------------#
# Create and Write output to plain text file. Will create directory and file if not already existing.
#
#   @param  output_dir              Name of directory to store created file (will )
#   @param  output_filename         Name of file to be created
#   @bool   timestamp               Will add a timestamp to the filename in order not to overwrite prior output files
#
#   TODO: Rewrite function so you have more control over the output directory

def output_gen_csv_lin(output_dir='',output_filename='',headings='',timestamp=True):
    
    # Defines the current working directory file path  
    current_dir = os.getcwd()

    # Asks user to input the name of output directory
    if output_dir == '':
        output_dir = input("\nOutput Folder Name: ")
    output_folder_name = "{}/{}/".format(current_dir,output_dir)
    
    # If output directory does NOT exist, it is created
    if not os.path.exists(output_folder_name):
        os.makedirs(output_folder_name)

    # Asks user to input the output filename (e.g., 'routerACL')
    if output_filename == '':
        output_filename = input("Output File Name: ")
    print("")

    if timestamp == True:
        # Calculates the current time at runtime and formats to yyyymmdd_hhmmss
        x = datetime.datetime.now()
        fileTime = x.strftime("%Y%m%d_%H%M%S")

        # Compiles the output string from the folder creation code block, the variable 'output_filename',
        #   and the generated 'fileTime' variable
        csv_out = ("{}{}_{}.csv".format(output_folder_name,output_filename,fileTime))
    else:
        csv_out = ("{}{}.csv".format(output_folder_name,output_filename))
    
    # Opens the output file using variable 'csv_out' and is ready to write lines
    #   Example: write_output = bse_output_gen_csv()
    #            write_output.writerow('')
    csvOpen = open(csv_out, "w", newline="", encoding='utf-8')
    csv_output = writer(csvOpen)

    # Prompt user if they want column headings for CSV output file
    if headings == '':
        headings_decision = input("Would you like to add headings to your CSV? (y/n): ")
        print("")

        # If yes, this is the process of adding headings to the CSV
        if headings_decision == "y":
            headings = []
            headings_data = input("Enter the column headings separated by a comma.\n(Example --> heading1,heading2,heading3,...)\n\nHeadings: ")
            headings_data = headings_data.split(",")
            for ele in headings_data:
                ele = ele.strip()
                headings.append(ele)
            # Write headings in CSV file
            csv_output.writerow(headings)
    else:
        csv_output.writerow(headings)

    return(csv_output)


#------------------------------------------------------------------------------------------------------------------------#
#   DATA IN - CSV to Dict                                                                                                #
#------------------------------------------------------------------------------------------------------------------------#
# Import a CSV file into a Python dictionary object
#
#   @param  filename              Name/path of CSV file to be imported

def csv_to_dict(filename):

    with open(filename, 'r', encoding='utf-8-sig') as f:  
        dict_reader = DictReader(f)        
        list_of_dict = list(dict_reader)   

    return(list_of_dict)