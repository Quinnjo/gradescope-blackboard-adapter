import csv
import os

READ_CSV_FILEPATH = 'old.csv'
WRITE_CSV_FILEPATH = 'new.csv'

"""
Open a Blackboard (HuskyCT) generated csv file
return a Dictionary with key:value pairs as
{'First Last' : {'Field' : Value}}
d['Student Name']['hw5'] should be this student's hw5 grade
"""
def blackboard_grades_as_dict(filename):
    fieldnames = []

    # Open and convert field names to assignment
    with open(filename, mode='r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for fn in reader.fieldnames:
            fieldnames.append(extract_assignment_name(fn))

    # Open same file with processed fieldnames
    res = dict()
    with open(filename, mode='r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            # These keys are from HuskyCT csv format
            full_name = row['first name'] + ' ' + row['last name']

            # Add the name:dict pair to our result
            res[full_name] = row

    return res

        
def is_assignment_name(fieldname):
    return '[' in fieldname

# Extract the blackboard assignment name, convert to lowercase
def extract_assignment_name(fieldname):
    if is_assignment_name(fieldname):
        return fieldname[:fieldname.find('[')-1].lower()
    return fieldname.lower()

def gradescope_grades_as_dict(filename):
    fieldnames = []
    with open(filename, mode='r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for fn in reader.fieldnames:
            fieldnames.append(fn.lower())
    
    res = dict()
    with open(filename, mode='r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            # These keys are from HuskyCT csv format
            full_name = row['name']

            # Add the name:dict pair to our result
            res[full_name] = row

    return res

def gs_assignment_name(filename):
    if '_' in filename:
        return filename[:filename.find('_')].lower()
    return filename.lower()

def transfer_assignment(filepath, asgn_name, bb):
    gs = gradescope_grades_as_dict(filepath)
    print('Transferring assignment: ' + asgn_name)
    for name, d in gs.items():

        if name in bb.keys():
            if d['status'] == 'Graded':
                bb[name][asgn_name] = d['total score']
            else:
                bb[name][asgn_name] = '0.0'
                # Zero for no submission

def write_blackboard_csv(src_file, dst_file, bb):
    with open(dst_file, mode='w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = list(bb.values())[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #print(fieldnames)
        #print(bb)
        writer.writerows(bb.values())

def transfer_grades(src_file, dst_file, scores_dir):
    bb = blackboard_grades_as_dict(src_file)
    #print(list(bb.values())[0])
    
    # Look for all gradescope csv files and transfer their grades
    with os.scandir(scores_dir) as obj:
        for entry in obj:
            if entry.is_file():
                transfer_assignment(entry.path, gs_assignment_name(entry.name), bb)
    
    # Write to new csv
    write_blackboard_csv(src_file, dst_file, bb)

    # TODO: Format the written csv in a way that blackboard will accept

    

def main():
    transfer_grades(READ_CSV_FILEPATH, WRITE_CSV_FILEPATH, 'src_grades')

if __name__ == '__main__':
    main()