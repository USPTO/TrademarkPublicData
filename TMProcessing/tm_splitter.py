#!/usr/bin/python3

# tm_splitter.py by Michael Henderson 
# Split individual TM files from a  bulk downloaded XML file containing an aggregation of TMs
# Write out a separate XML files and Solr ready XML file for each TM

import os
import re
import sys
import getopt
import xml.dom.minidom

def main(argv):
    
    #defaults for optional command line arguments    
    bulk_tm_file = 'apc161231-56-test.xml'
    output_directory = 'tm_corpus'
    
    # regular expressions for tm bibdata extraction
    xml_tag ='<?xml version=\"1.0\" encoding=\"UTF-8\"?>'
    start_xml_pattern = re.compile("(?P<xml_tag><\?xml[^>]+\?>[\s]*?)", re.IGNORECASE)
    doctype_tag = ''
    start_doctype_pattern = re.compile("(?P<doctype_tag><!DOCTYPE trademark-applications-daily \[[^]]+\]>[\s]*)", re.IGNORECASE)
    start_tm_file = '(?P<start_tm_file_tags><trademark-applications-daily>[^<]+<version>[^<]+<version-no>[^<]+</version-no>[^<]+<version-date>[^<]+</version-date>[^<]+</version>[^<]+<creation-datetime>(?P<creation_datetime>[^<]+)</creation-datetime>[^<]+<application-information>[^<]+<file-segments>[^<]+<file-segment>[^<]+</file-segment>[^<]+<action-keys>[^<]+<action-key>[^<]+</action-key>)'
    start_tm_file_pattern = re.compile(start_tm_file, re.IGNORECASE)
    creation_datetime_tag = '<creation-datetime>(?P<creation_datetime>[^<]+)</creation-datetime>'
    creation_datetime_pattern = re.compile(creation_datetime_tag, re.IGNORECASE)
    creation_datetime = ''
    tm_start_tag = ''
    start_tm_file_tags = ''
    eof_tags = ''
    start_tm_pattern = re.compile("(?P<tm_start_tag><case-file>)", re.IGNORECASE)
    end_tm_pattern = re.compile("<\/case-file>", re.IGNORECASE)
    tm_pattern=re.compile("(?P<case_file><case-file>([\w\W]+?</case-file>))", re.IGNORECASE)
    INTL_pattern=re.compile("(<international-code>(?P<intl_code>[\w\W]+?)</international-code>)",re.IGNORECASE)
    main_class_pattern=re.compile("(?P<main_class_1>[\w])[\s](?P<main_class_2>[\w])")
    patent_file_pattern = re.compile("<us-patent-grant([^>]+?file\=\")(?=(?P<patent_file>[^>]+?)\")([^>]+?>)", re.IGNORECASE)
    record_separator = "</case-file>\n"
    end_of_file = '(?P<eof_tags></action-keys>[^<]+</file-segments>[^<]+</application-information>[^<]+</trademark-applications-daily>)'
    patent_file_base_pattern = re.compile("(?P<file_base>[\w\-]+?)[\.][xX][mM][lL]", re.IGNORECASE)
    serial_number_pattern = re.compile("(<serial-number>(?P<serial_number>[\w\W]+?)</serial-number>)", re.IGNORECASE)
    
    eof_pattern = re.compile(end_of_file, re.IGNORECASE)
    mark_id_pattern = re.compile("(<mark-identification>(?P<mark_id>[\w\W]+?)</mark-identification>)", re.IGNORECASE)
    gs_pattern = re.compile("(<case-file-statement>[^<]+<type-code>(?P<gs_type_code>GS[\w\W]+?)</type-code>[^<]+<text>(?P<gs_text>[\w\W]+?)</text>)", re.IGNORECASE)
    cf_stmts_pattern = re.compile("(?P<cf_stmts><case-file-statements>([\w\W]+?</case-file-statements>))", re.IGNORECASE)


    tm_drawing_code_pattern = re.compile ("(<mark-drawing-code>(?P<mark_drawing_code>[\w\W]+?)</mark-drawing-code>)", re.IGNORECASE)
    tm_design_code_pattern = re.compile ("(<design-search>[^<]+<code>(?P<design_search_code>[\w\W]+?)</code>)", re.IGNORECASE)
    tm_design_searches_pattern = re.compile("(?P<design_searches><design-searches>([\w\W]+?</design-searches>))", re.IGNORECASE)
    
    # counters for tracking frequencies of XML tags
    line_count_readfile = 0
    start_xml_count = 0
    start_doctype_count = 0
    start_patent_count = 0  
    end_patent_count = 0
    patent_count = 0
    USPC_count = 0
    tm_list_length = 0
    # list that will hold records read from the input file
    records = []
    # list that will hold TM records
    tm_list = []
    # list that will hold TM design codes
    tm_design_codes_list = []
    # list that will hold the TM GS codes + text
    tm_gs_codes_list = []
    # parse the optional command line arguments; use default values if no cmd line args provided by user
    print('Number of arguments: ', len(sys.argv), 'arguments')
    print('Argument List:', str(sys.argv))
    print('Argv: ', argv)
    numargs = len(sys.argv)
    if numargs < 2: raise TypeError('requires at least one argument: tm_splitter.py [-i <inputfile> | --ifile <inputfile>]')
    
    try:
        opts, args = getopt.getopt(argv, "hi:d:",["ifile=", "odir"])
        
    except getopt.GetoptError:
        print ('tm_splitter.py [-i <inputfile> | --ifile <inputfile>] [-d <outdir> | --odir <outdir>]')
        sys.exit(2) 
        
    for opt, arg in opts:
        if opt == '-h':
            print('tm_splitter.py [-i <inputfile> | --ifile <inputfile>][-d <outdir>|--odir <outdir>]') 
            sys.exit()
        elif opt in ("-i", "--ifile"):
            bulk_patents_file = arg
            
        elif opt in ("-d", "--odir"):
            output_directory = arg
    

    try: 
      # use buffered reader to read records from in input file; build a list of strings representing TM records
      records = readrecords(bulk_patents_file, record_separator)
     
      record_list = list(records)
      
      for record in record_list:
        match_start_tm_file_pattern = re.search(start_tm_file_pattern, record)
        if match_start_tm_file_pattern:
            start_tm_file_dict = match_start_tm_file_pattern.groupdict()
            start_tm_file_tags = start_tm_file_dict['start_tm_file_tags']
            print("start_tm_file_tags:", start_tm_file_tags)
        match_creation_datetime = re.search(creation_datetime_pattern, record)
        if match_creation_datetime:
            creation_datetime_dict = match_creation_datetime.groupdict()
            creation_datetime = creation_datetime_dict['creation_datetime']
            print("creation datetime: ", creation_datetime)
            
        match_eof = re.search(eof_pattern, record)
        if match_eof:
            print("matched eof: ", record)
            match_eof_dict = match_eof.groupdict()
            eof_tags = match_eof_dict['eof_tags']
            
        # match open + closing tags i.e. <case-file ...> ...</case-file>
        match_tm = re.search(tm_pattern, record)
        if match_tm:
            match_tm_dict = match_tm.groupdict()
            tm_case_file = match_tm_dict['case_file']
            tm_list.append(tm_case_file)
            
        else:
            print("didn't match TM record:", record)
            next
            
     
      tm_list_length = len(tm_list)
      print ("finished reading TMs") 
      print("number of TMs read:")
      print(tm_list_length)
      print("")
      
      
            
           
    except IOError as e:
        print("could not open file: ", e) 
    except ValueError as e:
        print('bad filename', e)  
        
    
    
    # extract bibdata from each record
    print("processing tms:")
    for record in tm_list:
        tm_design_codes_list = []
        
        # extract opening xml elements i.e.<?xml version="1.0" encoding="UTF-8"?>
        match_xml_start = re.search(start_xml_pattern, record)
        if match_xml_start:
           start_xml_count += 1
           match_xml_start_dict = match_xml_start.groupdict()
           xml_tag = match_xml_start_dict['xml_tag'] 
           # remove trailing white space including newline
           xml_tag.rstrip() 
                         
        #count doctype elements i.e. <!DOCTYPE us-patent-grant SYSTEM "us-patent-grant-v42-2006-08-23.dtd" [ ]>
        match_doctype_start = re.search(start_doctype_pattern, record)
        if match_doctype_start:
           start_doctype_count += 1
           match_doctype_dict = match_doctype_start.groupdict()
           doctype_tag = match_doctype_dict['doctype_tag']
           # remove trailing white space including newline
           doctype_tag.rstrip()
           
        # match open + closing tags i.e. <case-file ...> ...</case-file>
        match_tm = re.search(tm_pattern, record)
        if match_tm:
            patent_count +=1    
            print ("processing tm number: ", patent_count, " / ", tm_list_length)
            print(tm_list_length) 
        else:
            print("didn't match TM record:", record)
            next
                   
        # extract us tm opening elements i.e. <us-patent-grant ... file="USD0595476-20090707.XML" ...>
        match_tm_start = re.search(start_tm_pattern, record)
        if match_tm_start:
            start_patent_count +=1 
            match_tm_start_dict= match_tm_start.groupdict()
            tm_start_tag = match_tm_start_dict['tm_start_tag']
            tm_start_tag.rstrip()
            
        # count tm closing elements i.e. </us-patent-grant>        
        match_tm_end = re.search(end_tm_pattern, record)
        if match_tm_end:
            end_patent_count += 1
                    
        
        
        # extract the patent XML file name i.e.<us-patent-grant ... file="USD0595476-20090707.XML" ...>
        match_patent_file = re.search(patent_file_pattern, record)
        
        
        # assign default file names in case serial number  is missing
        tm_file = 'tm_123.xml'
        tm_file_base = 'tm123'
        tm_file_solr = 'solr_' + tm_file
        
        # extract the TM serial number
        match_tm_serial = re.search(serial_number_pattern, record)
        if match_tm_serial:
            match_tm_serial_dict = match_tm_serial.groupdict()
            tm_serial_number = match_tm_serial_dict['serial_number']
            tm_file = tm_serial_number + ".xml"
            
            tm_file_solr = "solr_" + tm_file
            
        print("tm_file: ", tm_file) 
        print("tm_file_solr:", tm_file_solr)
          
        # extract the TM mark id
        tm_mark_id = "empty"
        match_tm_mark_id = re.search(mark_id_pattern, record)
        if match_tm_mark_id:
            match_tm_mark_id_dict = match_tm_mark_id.groupdict()
            tm_mark_id = match_tm_mark_id_dict['mark_id']
            
        print("tm_mark_id: ", tm_mark_id)   
        
        # extract TM goods and services embedded under case-file-statements:
        cf_stmts = "empty"
        tm_gs_code = "empty"
        tm_gs_text = "empty"
        tm_gs_codes_list = []
        
        # match & extract <case-file-statements>...</>
        match_cf_stmts = re.search(cf_stmts_pattern, record)
        if match_cf_stmts:
            match_cf_stmts_dict = match_cf_stmts.groupdict()
            cf_stmts = match_cf_stmts_dict['cf_stmts']
        print("cf_stmts: ", cf_stmts.encode("utf-8"))
        
        # split the individual GS codes
        lines = cf_stmts.split("</case-file-statement>")
        gs_cnt = 0
        for line in lines[:-1]:
            tm_gs_code = "empty"
            tm_gs_text = "empty"
            match_tm_gs = re.search(gs_pattern, line)
            if match_tm_gs:
                gs_cnt += 1
                print("line: ", gs_cnt)
                print(line.encode("utf-8"))
                match_tm_gs_dict = match_tm_gs.groupdict()
                tm_gs_code = match_tm_gs_dict['gs_type_code']
                tm_gs_text = match_tm_gs_dict['gs_text']
                
                tm_gs_codes_list.append(tm_gs_code + ":" + tm_gs_text)
                print("appended to tm_gs_codes_list: ")
                print(tm_gs_code + ":" + tm_gs_text)  
        
        # extract TM mark drawing code pattern
        tm_drawing_code = "empty"
        match_tm_drawing_code = re.search(tm_drawing_code_pattern, record)
        if match_tm_drawing_code:
            match_tm_drawing_code_dict = match_tm_drawing_code.groupdict()
            tm_drawing_code = match_tm_drawing_code_dict['mark_drawing_code']
        print("tm_drawing_code: ", tm_drawing_code.encode("utf-8"))    
        
        
        
        #extract TM design searches
        tm_design_searches = "empty"
        match_tm_design_searches = re.search(tm_design_searches_pattern, record)
        if match_tm_design_searches:
            match_tm_design_searches_dict = match_tm_design_searches.groupdict()
            tm_design_searches = match_tm_design_searches_dict['design_searches']
        print("tm_design_searches: ", tm_design_searches.encode("utf-8"))
        lines = tm_design_searches.split("</design-search>")
        for line in lines[:-1]:
            print("line: ")
            print(line.encode("utf-8"))
            
            # extract TM design codes: <code> </code> elements
            match_design_code = re.search(tm_design_code_pattern, line)
            if match_design_code:
                match_design_code_dict = match_design_code.groupdict()
                tm_design_code = match_design_code_dict['design_search_code']
                tm_design_codes_list.append(tm_design_code)
                print("appended to tm_design_codes_list: ")
                print(tm_design_code.encode("utf-8"))
                
            # extract the match and append to tm_design_codes_list
            
        # extract the XML file name of the patent
        if match_patent_file:
            patent_file_dict = match_patent_file.groupdict()
            tm_file = patent_file_dict['patent_file']
            
           
        
        # extract the base name of input file to create directory name
        match_patent_file_base = re.search(patent_file_base_pattern, bulk_patents_file)
        if match_patent_file_base:
            patent_file_base_dict = match_patent_file_base.groupdict()
            tm_file_base = patent_file_base_dict['file_base']   
            print("tm_file_base:", tm_file_base.encode("utf-8"))
            
        
        
        
        # extract the TM intl code
        int_code = "no_intl_code"
        if (re.search(INTL_pattern, record)):
            
            INTL_pattern_match = re.search(INTL_pattern, record).groupdict()
            print ("INTL_pattern_match:", INTL_pattern_match)
            USPC_count += 1
            # get rid of leading and trailing white space
            int_code = INTL_pattern_match['intl_code'].strip()
        
        
        
               
        
       
       
        # get rid of internal white space in main class
        # i.e. D 1 =>D1, D 2=>D2, D 9=>D9
        is_intern_space = re.search(main_class_pattern, int_code)
        if (is_intern_space):
           main_class_dict = is_intern_space.groupdict()
           int_code = main_class_dict['main_class_1'] + main_class_dict['main_class_2']
        
        # build the patents corpus under the output directory using the international code 
        #directory = output_directory + "/" + int_code 
        #path_tm = output_directory + "/" + int_code  + "/" + tm_file
        
        # build the TM corpus under the output directory using the base name of the XML input file 
        directory = output_directory + "/" + tm_file_base + "/solr"
        # complete TM record XML file
        path_tm = output_directory + "/" + tm_file_base  + "/" + tm_file
        # solr ready XML
        path_tm_solr = output_directory + "/" + tm_file_base + "/solr/" + tm_file_solr
        
        #this call to os.path.dirname significantly impacts the performance
        #directory = os.path.dirname(path)
                
        # in Python 3: os.makdirs() supports exist_ok=True to ignore directory already exists errors
        print("creating directory: ")
        print(directory.encode("utf-8"))
        os.makedirs(directory, exist_ok=True)
        
        # write the complete TM XML file under directory named after TM annual XML file 
        print("creating tm file:")
        print(path_tm.encode("utf-8"))
        outfile = open(path_tm,'w', encoding="utf8")
        outfile.write(xml_tag)
        outfile.write("\n")
        outfile.write(start_tm_file_tags)
        
        outfile.write("\n")
        outfile.write(record)
        outfile.write("\n")
        outfile.write(eof_tags)
        outfile.close()
        print("tm file creation complete\n")
       
        # write the Solr ready XML file
        print("creating Solr ready XML file:")
        print(path_tm_solr.encode("utf-8"))
        outfile = open(path_tm_solr,'w', encoding="utf8")
        outfile.write(xml_tag)
        outfile.write("\n")
        outfile.write("<add>\n")
        outfile.write("<doc>\n")
        
        # set id to serial number
        outfile.write("<field name=\"id\">")
        outfile.write(tm_serial_number)
        outfile.write("</field>\n")
        
        # creation-datetime
        outfile.write("<field name=\"creation-datetime\">")
        outfile.write(creation_datetime)
        outfile.write("</field>\n")
        
        # parent document type is tm-bibdata
        outfile.write("<field name=\"type\">")
        outfile.write("tm-bibdata")
        outfile.write("</field>\n")
        
        # serial number
        outfile.write("<field name=\"serial-number\">")
        outfile.write(tm_serial_number)
        outfile.write("</field>\n")
        
        # mark-identification
        outfile.write("<field name=\"mark-identification\">")
        outfile.write(tm_mark_id)
        outfile.write("</field>\n")
        
        # mark-drawing-code
        outfile.write("<field name=\"mark-drawing-code\">")
        outfile.write(tm_drawing_code)
        outfile.write("</field>\n")
        
        # design codes:
        for design_code in tm_design_codes_list:
           outfile.write("<field name=\"design-code\">")
           outfile.write(design_code)
           outfile.write("</field>\n")
           
        # good-services
        for gs_code_text_pair in tm_gs_codes_list:
           print ("gs_code_text_pair:")
           print(gs_code_text_pair.encode("utf-8"))
           lines = re.split(":", gs_code_text_pair)
           gs_code = lines[0]
           gs_text = lines[1]
           
           # add the gs code and text as nested document w/unique id 
           gs_serial_number = tm_serial_number + "_" + gs_code
           outfile.write("<doc>\n")
           outfile.write("<field name =\"id\">")
           outfile.write(gs_serial_number)
           outfile.write("</field>\n")
           outfile.write("<field name=\"type\">")
           outfile.write("goods-services")
           outfile.write("</field>\n")
           outfile.write("<field name=\"gs-code\">")
           outfile.write(gs_code)
           outfile.write("</field>\n")
           outfile.write("<field name=\"gs-text\">")
           outfile.write(gs_text)
           outfile.write("</field>\n")
           outfile.write("</doc>\n")
        
        
        
                
                
        outfile.write("</doc>\n")
        outfile.write("</add>\n")
        outfile.close()
        print("tm Solr file creation complete\n")        
        
    # print summary of tags matched during tm processing
    print("\ntm processing summary:")
    
    print("Number of lines processed from input file:")
    #print(len(readfile(bulk_patents_file)))
    
    
    print("Number of tm classifications extracted:")
    print(USPC_count)
    
    print("Number of opening xml elements matched:")
    print(start_xml_count)
    
    print("Number of doctype elements matched:")
    print(start_doctype_count)
    
    print("Number of start tm elements matched:")
    print(start_patent_count)
    
    print("Number of end tm elements matched: ")
    print(end_patent_count)   
    
    print ("Number of complete tms matched:")  
    print(patent_count)
    
    print("Corpus created under output directory:")
    print(os.path.abspath(output_directory))
    
    print("tm processing complete") 
    
 
 # read input file one line at a time       
def readfile(filename):
    if filename.endswith('.xml'):
        fh = open(filename, encoding="utf8")
        return fh.readlines()
    else: raise ValueError('Filename must end with .xml')
    
# read from input file using a buffered reader and record separator to demarcate end of record   
def readrecords(filename, record_separator='\n',  bufsize=4096):
      print("reading input file:")
      print(filename)
      print("using record separator:")
      print(record_separator)
      print("read buffer size in bytes:")
      print(bufsize)
      
      record_separator_pattern = re.compile(record_separator, re.IGNORECASE)
      
      
      input = open(filename, encoding="utf8")
      buf = ''
      print("reading TMs...please wait...")
      while True:
         newbuf = input.read(bufsize)
         #print ("newbuf: ", newbuf)
         if not newbuf:
            if buf != '': 
                yield buf
            return
         buf += newbuf
        
             
         lines = buf.split(record_separator)
                  
         for line in lines[:-1]:
             
             yield line + record_separator
         buf = lines[-1]
         
         
       

     
if __name__ == "__main__": main(sys.argv[1:])
