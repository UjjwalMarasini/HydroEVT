# This code extract the data extreme values.
# The data should in the format of DHM.

import os
import csv
import re

results = []

for filename in os.listdir():
    if filename.lower().endswith(".txt"):

        year = None

        # AQ420_64.TXT → 1964–1995
        match = re.search(r'_(\d{2})\.txt', filename.lower())
        if match and filename.upper().startswith("AQ420"):
            yy = int(match.group(1))
            year = 1900 + yy

        # AQ_2007.txt
        elif filename.startswith("AQ_"):
            match = re.search(r'(\d{4})', filename)
            if match:
                year = int(match.group(1))

        # 2000.txt
        elif re.fullmatch(r'\d{4}\.txt', filename.lower()):
            year = int(filename[:4])

        # 01.txt or 96.txt
        elif re.fullmatch(r'\d{2}\.txt', filename.lower()):
            yy = int(filename[:2])
            if yy <= 6:
                year = 2000 + yy
            else:
                year = 1900 + yy

        if year:
            with open(filename, "r") as file:
                for line in file:
                    if line.strip().startswith("Max"):
                        values = line.split()
                        last_value = values[-1]

                        # Skip NA values
                        if last_value.upper() == "NA":
                            print(f"Skipped NA in {filename}")
                            break

                        results.append([year, float(last_value)])
                        break

# Sort by year
results.sort(key=lambda x: x[0])

# Save formatted.csv
with open("formatted.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Year", "Annual Peak"])
    writer.writerows(results)

print("Done! formatted.csv created successfully.")