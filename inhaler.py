#!/bin/python

from pprint import pprint
from filter import alexa_filter

def parse_list(filename):
    """
    Parse the list and chop it up into sections
    """
    lines = open(filename, "r").readlines()
    # lines = lines[:50]

    print "Parsing File: ", filename.split("/")[-1]
    print "# lines: ", len(lines)
    print

    sections = []
    section = []
    header = None

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line[0] == '[':
            continue
        if line[:2].strip() == '!' and (len(line) > 2 and line[2] != "*"):
            continue
        if line.startswith("! ***"):
            if header:
                sections.append((header, section))
            section = []
            header = (line.strip("!")
                         .strip("-")
                         .strip()
                         .strip("*"))
            header = header.split(".")[0].split("/")[-1]
            continue

        section.append(line)

    if header:
        sections.append((header, section))
    
    return sections


def print_sections(sections):
    print "%-50s%10s%10s" % ("Section", "# of Rules", "Dropped")
    print_separator()
    for section in sections:
        print_section(section)


def print_section(section):
    print "%-50s%10d%10d" % (section[0], len(section[1]), len(section[2]))

def print_separator():
    print "-" * 80


def filter_section(section):
    name, rules = section
    filtered_rules, dropped_rules = alexa_filter(rules)
    return (name, filtered_rules, dropped_rules)

def is_ascii(string):
    try:
        string.encode('ascii')
    except UnicodeDecodeError:
        return False
    return True

def is_rule_ok(rule):
    if (rule.startswith("|http://") or
        rule.startswith("|https://") or
        rule.startswith("@@|http://") or
        rule.startswith("@@|https://")):
        return False

    if "{" in rule:
        return False

    if not is_ascii(rule):
        return False

    return True

def sanitize_section(section):
    name, rules, dropped = section

    sanitized_rules = []
    for rule in rules:
        if is_rule_ok(rule):
            sanitized_rules.append(rule)
        else:
            dropped.append(rule)
    return (name, sanitized_rules, dropped)



def write_rules(output_file, section_name, rules):
    output_file.write("!" + 40 * "-" + "\n")
    output_file.write("! *** " + section_name + " ***\n")
    for rule in rules:
        output_file.write(rule + "\n")

def write_data(filename, sections):

    output_dir = "processed"
    drop_dir = "dropped"

    # sections = sections[:1]
    output_filename = filename.split("/")[-1]

    output_file = open(output_dir + "/" + output_filename, "w")
    drop_file = open(drop_dir + "/" + output_filename, "w")

    for section in sections:
        name, rules, dropped = section

        if rules:
            write_rules(output_file, name, rules)

        if dropped:
            write_rules(drop_file, name, dropped)

    output_file.close()
    drop_file.close()


def process_file(filename):
    sections_to_filter = [
        "easylist_general_block",
        "easylist_general_block_dimensions",
        "easylist_general_hide",
        "easylist_whitelist_general_hide",
        "easylist_specific_block",
        "easylist_specific_hide",
        "easylist_whitelist",
        "easylist_whitelist_dimensions",

        "easyprivacy_specific",

        "fanboy_social_specific_block",
        "fanboy_social_specific_hide",
        "fanboy_social_thirdparty",
    ]

    sections_to_drop = [
        "easylist_adservers_popup",
        "adult_adservers",
        "adult_adservers_popup",
        "easylist_thirdparty_popup",
        "adult_thirdparty_popup",
        "easylist_specific_block_popup",
        "adult_specific_block",
        "adult_specific_block_popup",
        "adult_specific_hide",
        "easylist_whitelist_popup",
        "adult_whitelist",
        "adult_whitelist_popup",

        "easyprivacy_specific_international",
        "easyprivacy_thirdparty_international",
        "easyprivacy_whitelist_international",

        "fanboy_social_international",
    ]

    def process_section(section):
        name, rules = section
        if name in sections_to_filter:
            return filter_section(section)
        elif name in sections_to_drop:
            return (name, [], rules)
        else:
            return (name, rules, [])

    sections = parse_list(filename)
    sections = [process_section(section) for section in sections]
    sections = [sanitize_section(section) for section in sections]

    write_data(filename, sections)

    total_count = sum([len(section[1]) for section in sections])
    drop_count = sum([len(section[2]) for section in sections])
    
    print_sections(sections)
    print_separator()
    print "%-50s%10d%10d" % ("Total", total_count, drop_count)


    return total_count, drop_count


files = [
    "update/easylist.txt",
    "update/easyprivacy.txt",
    "update/antisocial.txt",
]

total_count = 0
dropped_count = 0
for filename in files:
    total, dropped = process_file(filename)
    total_count += total
    dropped_count += dropped
    print

print_separator()
print "%-50s%10d%10d" % ("Grand Total", total_count, dropped_count)


