"""
First script which should be used to read the input file created by download_reuters.py 
script and create a CSV output file. If script is runned multiple times with different
input files, CSV output should be appended, not re-created.

"""


import re
import csv
import time
import datetime
import os
import hashlib

DELAY = 300   

f_output = open('output.csv', 'w')
csv_writer = csv.writer(f_output, delimiter=',', quotechar="'", quoting=csv.QUOTE_NONE, escapechar="\\")
csv_writer.writerow(['Date', 'Time', 'Title', 'Text'])
list_of_hashed_titles = []

print("Andrej")

while True:
    now = datetime.datetime.now()
    print(now.strftime("%Y%m%d-%H%M%S"))
    now = now - datetime.timedelta(seconds=DELAY)
    file_name = "REUT_" + now.strftime("%Y%m%d-%H%M%S") + ".txt"
    print(type(file_name))

    list_of_files = []
    for subdir, dirs, files in os.walk('./'):
        for file_name in files:
            if file_name.startswith("REUT_"):
                file_date_time = datetime.datetime.strptime(re.split("_|\.",file_name)[1], "%Y%m%d-%H%M%S")
                if file_date_time > now:
                    list_of_files.append(file_name)


    for file_name in list_of_files:
        print("Reading file " + file_name)
        f_input = open(file_name, 'r')

        data = f_input.read()

        if "------------------------" in data:
            split_sections = re.split("------------------------", data)
            if "\n" in split_sections:
                split_sections.remove("\n")

                for section in split_sections:
                    data_columns = re.split("URL: |\nDATE: |\nTITLE: |TEXT:", section)
                    data_columns = data_columns[2].split() + [re.sub('[\n,\"]', '', data_columns[3]), re.sub('[\n,\"]', '', data_columns[4])]

                    if len(data_columns) == 4:
                        if data_columns[3] != '' and hashlib.md5(data_columns[3].encode()).hexdigest() not in list_of_hashed_titles:
                            list_of_hashed_titles.append(hashlib.md5(data_columns[3].encode()).hexdigest())
                            csv_writer.writerow(data_columns)

        print("Closing files")
        f_input.close()

    time.sleep(DELAY)


