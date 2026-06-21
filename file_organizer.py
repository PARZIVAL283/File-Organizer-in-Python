""" File Automation Project — "IEEE CIS IUBAT Student Branch"
Author  : Sourodip Das Gupta
Features: Level 1 (Date-wise sorting) 
+ Level 2 (Auto folder creation by year)
+ Level 3 (File count reporting)
"""

# Importing the modules required for the project
import os
import shutil
import datetime
import csv


# Change this to organize the folder.
SOURCE_DIR = "."

# Where organised files will be placed.
# A sub-folder called "Organised" is created inside SOURCE_DIR.
OUTPUT_DIR = os.path.join(SOURCE_DIR, "Organised")

# Files that the script itself creates — we must skip these.
SKIP_FILES = {"file_organizer.py", "file_report.txt", "file_report.csv"}


# HELPER: get modification date of a file

def get_file_date(filepath):
    
    """Returns a datetime object representing the last-modification
    date of the given file.
    os.path.getmtime() gives seconds since the Unix epoch;
    datetime.fromtimestamp() converts that to a human-readable date."""


    timestamp = os.path.getmtime(filepath)
    return datetime.datetime.fromtimestamp(timestamp)


# FEATURE 1 + 2: Sort files & create folders

def organise_files(source_dir, output_dir):
    """Scans every file in source_dir, determines its modification date,
    and moves it into:
        output_dir / YEAR / Mon-YEAR / filename

    Example paths:
        Organised/2024/Jan-2024/report.pdf
        Organised/2025/Jun-2025/photo.jpg

    Returns a dict  {folder_label: file_count}  for the report."""


    # This dict will track how many files land in each folder.
    folder_counts = {}

    # checking if output folder exists.
    os.makedirs(output_dir, exist_ok=True)

    print("\n📂  Scanning files …\n")

    for filename in os.listdir(source_dir):

        # Build the full path of the current item.
        filepath = os.path.join(source_dir, filename)

        # Skip directories, the output folder, and our own files 
        if os.path.isdir(filepath):
            continue
        if filename in SKIP_FILES:
            continue

        # Get the file's modification date 
        file_date   = get_file_date(filepath)
        year_str    = str(file_date.year)                          # e.g. "2024"
        month_str   = file_date.strftime("%b")                    # e.g. "Jan"
        month_label = f"{month_str}-{year_str}"                   # e.g. "Jan-2024"

        # Feature 2: create Year folder automatically 
        year_folder  = os.path.join(output_dir, year_str)
        os.makedirs(year_folder, exist_ok=True)

        # Feature 1: create Month-Year sub-folder 
        month_folder = os.path.join(year_folder, month_label)
        os.makedirs(month_folder, exist_ok=True)

        # Move the file
        destination = os.path.join(month_folder, filename)

        # If a file with the same name already exists in the destination, append a counter to avoid overwriting it.
        if os.path.exists(destination):
            base, ext   = os.path.splitext(filename)
            counter     = 1
            while os.path.exists(destination):
                destination = os.path.join(month_folder, f"{base}_{counter}{ext}")
                counter    += 1

        shutil.move(filepath, destination)
        print(f"  ✅  {filename:40s}  →  {year_str}/{month_label}/")

        # Update counts (keyed by "YEAR/Mon-YEAR")
        label = f"{year_str}/{month_label}"
        folder_counts[label] = folder_counts.get(label, 0) + 1

    return folder_counts

# FEATURE 3: File count report

def generate_report(folder_counts, output_dir):
    """Prints a summary table to the console and saves two report files:
    • file_report.txt //  human-readable
    • file_report.csv  //  machine-readable (opens in Excel)"""

    report_txt = os.path.join(output_dir, "file_report.txt")
    report_csv = os.path.join(output_dir, "file_report.csv")

    total = sum(folder_counts.values())

    # Console output
    print("\n" + "=" * 50)
    print("  📊  FILE ORGANISATION REPORT")
    print("=" * 50)

    if not folder_counts:
        print("  No files were moved.")
    else:
        # Sort entries chronologically (year first, then month).
        for label in sorted(folder_counts.keys()):
            count = folder_counts[label]
            bar   = "█" * count          # tiny ASCII bar chart
            print(f"  {label:25s}  →  {count:4d} file(s)  {bar}")

        print("-" * 50)
        print(f"  {'TOTAL':25s}  →  {total:4d} file(s)")

    print("=" * 50 + "\n")

    # Save .txt report
    with open(report_txt, "w", encoding="utf-8") as f:
        f.write("FILE ORGANISATION REPORT\n")
        f.write(f"Generated : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 45 + "\n")
        for label in sorted(folder_counts.keys()):
            f.write(f"{label:25s} → {folder_counts[label]:4d} file(s)\n")
        f.write("-" * 45 + "\n")
        f.write(f"{'TOTAL':25s} → {total:4d} file(s)\n")

    # Save .csv report
    with open(report_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Folder", "File Count"])
        for label in sorted(folder_counts.keys()):
            writer.writerow([label, folder_counts[label]])
        writer.writerow(["TOTAL", total])

    print(f"   Reports saved:")
    print(f"   {report_txt}")
    print(f"   {report_csv}\n")


# main function to run the script
def main():
    print("╔══════════════════════════════════════════╗")
    print("║   File Automation Project — IEEE CIS     ║")
    print("╚══════════════════════════════════════════╝")
    print(f"\n  Source folder : {os.path.abspath(SOURCE_DIR)}")
    print(f"  Output folder : {os.path.abspath(OUTPUT_DIR)}")

    # Run organiser (Features 1 & 2)
    folder_counts = organise_files(SOURCE_DIR, OUTPUT_DIR)

    # Generate report (Feature 3)
    generate_report(folder_counts, OUTPUT_DIR)

    print("Done!!!! All files have been organised.\n")


if __name__ == "__main__":
    main()