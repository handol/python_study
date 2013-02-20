import re

# common variables

rawstr = r"""([ ,]+)(\w+)(\.vlrNum)(\s*[)])"""
embedded_rawstr = r"""([ ,]+)(\w+)(\.vlrNum)(\s*[)])"""
matchstr = """strcpy(dbDataCamelSysData.vlrNum, dbDataSub.vlrNum);"""

# method 1: using a compile object
compile_obj = re.compile(rawstr)
match_obj = compile_obj.search(matchstr)

# method 2: using search function (w/ external flags)
match_obj = re.search(rawstr, matchstr)

# method 3: using search function (w/ embedded flags)
match_obj = re.search(embedded_rawstr, matchstr)

# Retrieve group(s) from match_obj
all_groups = match_obj.groups()

# Retrieve group(s) by index
group_1 = match_obj.group(1)
group_2 = match_obj.group(2)
group_3 = match_obj.group(3)
group_4 = match_obj.group(4)

# Replace string
newstr = compile_obj.subn('1\12\23\3, OSZ_MSISDN \4', 0)

print newstr
