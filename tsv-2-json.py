# converts 4 tsv files into json format
# utilized code found here:
# https://www.geeksforgeeks.org/python-tsv-conversion-to-json/

import json

def tsv2json(input_file,output_file):
    arr = [] # empty array to hold all the documents
    file = open(input_file, 'r', encoding='utf8') 
    a = file.readline() # read first line only; a stores our data labels
    
    # The first line consist of headings of the record
    # so we will store it in a string and move to
    # next line in input_file.
    titles = [t.strip() for t in a.split('\t')] # a.split returns an array of strings, separated by the tab character; strip each one (remove the end \n)
    for line in file:
        d = {} # create an empty document
        for t, f in zip(titles, line.split('\t')): 
            if t in ['primaryProfession', 'knownForTitles', 'genres', 'characters']:
                stripped_string = f.strip()
                if stripped_string == '\\N':
                    d[t] = None
                else:
                    decluttered_string = stripped_string.replace('"', "").replace("[","").replace("]", "")
                    array_of_strings = decluttered_string.split(",")
                    d[t] = array_of_strings
            else:
                stripped_string = f.strip()
                if stripped_string == '\\N':
                    d[t] = None
                else:
                    d[t] = stripped_string # single string, strip \n 
        arr.append(d)
        
        # we will append all the individual dictionaires into list
        # and dump into file.
    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(json.dumps(arr, indent=4))


def main():
    # Driver Code
    input_filename = 'name.basics.tsv'
    output_filename = 'name.basics.json'
    tsv2json(input_filename,output_filename)

    input_filename = 'title.basics.tsv'
    output_filename = 'title.basics.json'
    tsv2json(input_filename,output_filename)

    input_filename = 'title.principals.tsv'
    output_filename = 'title.principals.json'
    tsv2json(input_filename,output_filename)
    
    input_filename = 'title.ratings.tsv'
    output_filename = 'title.ratings.json'
    tsv2json(input_filename,output_filename)

main()