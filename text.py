import traceback

# skipcq: PYL-W0621
def find_nth_occurrence(ini_str, sub_str, n):
    # Finding nth occurrence of substring
    val = -1
    # skipcq: PYL-W0612
    for i in range(0, n):
        val = ini_str.find(sub_str, val + 1)
    return val

def dob1_algo3_2_name_check(name):
    if name == "":
        return False

    if not name.startswith("Beneficiary:"):
        return False

    return True

"""
Beneficiary: John Doe

Phone: N/A

DOB: xx/xx/xxxx
"""

def dob1_algo3_2(lines, index):
    dob = lines[index]
    space_index = 4

    name = False

    # extract the dob
    dob = dob[space_index + 1:]
    # get rid of the 19 (like from 1933)
    correct_dob = dob[:len(dob)-4]
    correct_dob += dob[len(dob)-2:]

    for i in range(1, 11):
        new_name = lines[index - i]
        if not dob1_algo3_2_name_check(new_name):
            continue
        name = new_name
        name = name[name.find(":") + 1:]
        name = name.strip() 

        # swap first name and last name 
        # should be lastname firstname
        name_list = name.split(" ")
        name = name_list[1] + " " + name_list[0]
        break
    # if name:
    #     NOTE: this doesnt get rid of a middle name, idk if this occurence actually uses the middle name or not...
    #     # get rid of a middle name, if any
    #     if name.count(" ") > 1:
    #         # first_space = name.find(" ")
    #         # second_space = name.find(" ", first_space + 1)
    #         # name = name[:second_space]
    #         name = name.replace(",", "")

    return [name, correct_dob]

def dob1_algo3_name_check(name):
    if name == "":
        return False

    if not name.startswith("RE:"):
        return False

    return True

"""
RE: Doe John
DOB: xx/xx/xxxx
"""
def dob1_algo3(lines, index):
    dob = lines[index]
    space_index = 4

    name = False

    # extract the dob
    dob = dob[space_index + 1:]
    # get rid of the 19 (like from 1933)
    correct_dob = dob[:len(dob)-4]
    correct_dob += dob[len(dob)-2:]

    for i in range(1, 11):
        new_name = lines[index - i]
        if not dob1_algo3_name_check(new_name):
            continue
        name = new_name
        name = name[name.find(":") + 1:]
        name = name.strip()
    
    if name:
        # get rid of a middle name, if any
        if name.count(" ") > 1:
            first_space = name.find(" ")
            second_space = name.find(" ", first_space + 1)
            name = name[:second_space]

    return [name, correct_dob]

def dob1_algo2_name_check(name):
    if name == "":
        return False

    if not name.isupper():
        return False

    if not ", " in name:
        return False

    if name.startswith("PHS"):
        return False

    if name.count(",") != 1:
        return False

    return True

"""
DOE, MIDDLENAME JOHN
Current Meds MRN: 12345678901
DOB: X/X/XXXX, Sex: X
"""
def dob1_algo2(lines, index):
    dob = lines[index]
    space_index = 4

    name = False

    # extract the dob
    dob = dob[space_index + 1 : dob.find(",")]
    # get rid of the 19 (like from 1933)
    correct_dob = dob[:len(dob)-4]
    correct_dob += dob[len(dob)-2:]

    for i in range(1, 11):
        new_name = lines[index - i]
        if not dob1_algo2_name_check(new_name):
            continue
        name = new_name
        break

    if name:
        # get rid of a middle name, if any
        if name.count(" ") > 1:
            first_space = name.find(" ")
            second_space = name.find(" ", first_space + 1)
            name = name[:second_space]
            name = name.replace(",", "")

    return [name, correct_dob]

def dob1_algo1_name_check(name):
    if name == "":
        return False

    if not name.isupper():
        return False

    if not "," in name:
        return False

    return True

"""
DOE, JOHN
DOB:XX/XX/XX
"""
def dob1_algo1(lines, index):
    dob = lines[index]
    name = lines[index - 1]

    # get rid of a middle name, if any
    if name.count(" ") > 1:
        first_space = name.find(" ")
        second_space = name.find(" ", first_space + 1)
        name = name[:second_space]

    if not dob1_algo1_name_check(name):
        name = lines[index - 2]
    if not dob1_algo1_name_check(name):
        name = False

    if name:
        name = name.replace(",", "")

    correct_dob = dob[4:]
    return [name, correct_dob]

# dob1 -> DOB:
def dob1_algo_chooser(lines):
    dob_indexes = [n for (n, e) in enumerate(lines) if e.startswith("DOB:")]

    for dob_index in dob_indexes:
        dob = lines[dob_index]
        # sometimes, it's just: "DOB:" so we need to check for that
        if len(dob) <= 5:
            continue

        algo1_result = None
        algo2_result = None
        algo3_result = None

        # if there's not a space, it's algo1
        if dob[4] != " ":
            algo1_result = dob1_algo1(lines, dob_index)
        
        if dob[4] == " ":
            if dob[-8] == ",":
                algo2_result = dob1_algo2(lines, dob_index)
            algo3_result= dob1_algo3(lines, dob_index)
            if False in algo3_result:
                algo3_result = dob1_algo3_2(lines, dob_index)

        if algo1_result:
            if not False in algo1_result:
                return algo1_result
        if algo2_result:
            if not False in algo2_result:
                return algo2_result
        if algo3_result:
            if not False in algo3_result:
                return algo3_result
        continue
    return False


def dob2_name_check(name):
    if name == "":
        return False

    if not " , " in name:
        return False

    if not name.startswith("Patient:"):
        return False

    if name.count(",") != 1:
        return False

    return True

# dob2 -> "DOB/"
"""
Patient: DOE , JOE MIDDLENAME Location: Spc Procedure
MRN: 12345678 Copy to: DoctorLastName, DoctorFirstName
FIN: 123456789

 

DOB/Age/Sex: XX/XX/XXXX XX years Gender
"""

def dob2_algo(lines, index):
    dob = lines[index]

    name = False
    correct_name = False

    # extract the dob
    dob = dob[13:23]
    # get rid of the 19 (like from 1933)
    correct_dob = dob[:len(dob)-4]
    correct_dob += dob[len(dob)-2:]

    for i in range(1, 11):
        new_name = lines[index - i]
        if not dob2_name_check(new_name):
            continue
        name = new_name
        break
    
    if name:
        first_start = find_nth_occurrence(name, " ", 1)
        second_end = find_nth_occurrence(name, " ", 4)

        # extract the name
        correct_name = name[first_start + 1 : second_end]
        correct_name = correct_name.replace(", ", "")

    return [correct_name, correct_dob]

def dob2_algo_chooser(lines):
    dob_indexes = [n for (n, e) in enumerate(lines) if e.startswith("DOB/Age/")]

    for dob_index in dob_indexes:
        result = None

        result = dob2_algo(lines, dob_index)

        if result:
            if not False in result:
                return result
        continue
    return False

def dob3_name_check(name):
    if name == "":
        return False

    if not name.startswith("Patient Name:"):
        return False

    return True

# dob3 -> "Date of Birth:"
"""
Report ID: 12345678 End of Service Summary Report Y/Y/YYYY
Patient Name: John Doe Prescribing Physician: DoctorFirstName DoctorLastName, MD

Date of Birth: X/XX/XXXX Gender: F <Office Location>
"""

def dob3_algo(lines, index):
    dob = lines[index]

    name = False
    correct_name = False

    # extract the dob
    dob = dob[15 : dob.find(" ", 15)]
    # get rid of the 19 (like from 1933)
    correct_dob = dob[:len(dob)-4]
    correct_dob += dob[len(dob)-2:]

    for i in range(1, 11):
        new_name = lines[index - i]
        if not dob3_name_check(new_name):
            continue
        name = new_name
        break

    if name:
        name_start_index = find_nth_occurrence(name, " ", 2) + 1
        name_mid_index = find_nth_occurrence(name, " ", 3)
        name_end_index = find_nth_occurrence(name, " ", 4)

        first_name = name[name_start_index : name_mid_index]
        last_name = name[name_mid_index + 1 : name_end_index]

        correct_name = last_name + " " + first_name

    return [correct_name, correct_dob]

def dob3_algo_chooser(lines):
    dob_indexes = [n for (n, e) in enumerate(lines) if e.startswith("Date of Birth: ")]

    for dob_index in dob_indexes:
        result = None

        result = dob3_algo(lines, dob_index)

        if result:
            if not False in result:
                return result
        continue
    return False

def dob4_name_check(name):
    if name == "":
        return False

    if not name.startswith("Patient Name:"):
        return False

    return True

"""
Doe, John Y/Y/YYYY CardioNet Summary Report Page 1 of 2
Copyright � 2002-2011 CardioNet Inc. All Rights Reserved.ardionet, Inc

Doe, John Y/Y/YYYY CardioNet Summary Report
"""
# doesn't work??
# name only
# idek
def dob4_algo(lines, index):
    name = lines[index]

    end_space = find_nth_occurrence(name, " ", 2)
    correct_name = name[:end_space]
    correct_name = correct_name.replace(",", "")

    return [correct_name, False]

def dob4_algo_chooser(lines):
    name_indexes = [n for (n, e) in enumerate(lines) if "CardioNet Summary Report" in e]

    for name_index in name_indexes:
        result = None

        result = dob4_algo(lines, name_index)

        if result:
            if result[0]:
                return result
        continue
    return False

def master_algo_chooser(lines):
    dob1_result = dob1_algo_chooser(lines)
    if dob1_result:
        if not False in dob1_result:
            return dob1_result

    dob2_result = dob2_algo_chooser(lines)
    if dob2_result:
        if not False in dob2_result:
            return dob2_result

    dob3_result = dob3_algo_chooser(lines)
    if dob3_result:
        if not False in dob3_result:
            return dob3_result

    dob4_result = dob4_algo_chooser(lines)
    if dob4_result:
        if dob4_result[0]:
            return dob4_result

    # We couldn't find anything :(
    return [False, False]

def get_data_from_list(data_list):
    name = data_list[0]
    if name:
        name_list = name.split(" ")
        last_name = name_list[0].title()
        first_name = name_list[1].title()
    else:
        last_name = "ERROR"
        first_name = "ERROR"

    dob = data_list[1]
    if dob:
        dob_list = dob.split("/")

        year = dob_list[2]
        year = "19" + year

        month = dob_list[0]
        if len(month) == 1:
            month = "0" + month

        date = dob_list[1]
        if len(date) == 1:
            date = "0" + date
    else:
        year = "YYYY"
        month = "MM"
        date = "DD"
    
    return [last_name, first_name, year, month, date]

# skipcq: PYL-W0621
def find_info(file_int, test = False):
    # Note: test mode depends on the .txt file (from OCR) already existing\
    file_int = str(file_int)
    file = "./text/out_text" + file_int + ".txt"
    lines = []

    with open(file) as f:
        lines = [line.rstrip() for line in f]

    try:
        result = master_algo_chooser(lines)
    except:
        print("TEXT ERROR OCCURED WITH: " + str(file_int))
        traceback.print_exc()
        return [False, False]

    if test:
        data = get_data_from_list(result)
        new_file_name = f"./combined/{data[0]}_{data[1]}_DOB-{data[2]}-{data[3]}-{data[4]}_File-{file_int}.pdf"

        print(result)
        print(new_file_name)
        
        if data[0] != "ERROR":
            return True
        return False

    return result

if __name__ == "__main__":
    import cProfile

    file_int = "5800"
    cProfile.run('find_info(file_int, True)')