
## TrademarkPublicData
Utilities which support the processing of XML based USPTO trademark bulk download files

## Overview

The USPTO makes trademark data available to the public on both its own Bulk Data Download System Site as well as the external Reed Tech USPTO data portal.
The TM applications data is made available in XML format on a daily as well as annual basis. 
The collection of ZIP files on the Reed Tech site contains both the  daily  XML files(front files) as well as the annual XML files(back file). The  XML files are created and uploaded daily and contain pending and registered trademark text data including word mark, serial number, registration number, filing date, registration date, goods and services, classification number(s), status code(s), design search code(s), and pseudo mark(s).  
<ul>
<li><b><a href="http://patents.reedtech.com/tmappxml.php">Reed Tech IP Services, "USPTO Data Portal: Trademark Daily + Annual  XML Files - Applications"</a></b></li>
</ul>

The annual XML application files are available on both  the USPTO Bulk Data Storage System site as well as the Reed Tech site  and contain files with TM XML application data from April 7, 1884 to 2017:
<ul>
<li><b><a href="https://bulkdata.uspto.gov/data/trademark/dailyxml/applications/">USPTO Bulkdata Daily + Annual Trademark XML(Front + Back Files)</a></b></li>
</ul>
<ul>
<li><b><a href="https://patents.reedtech.com/tmappxml.php#1884-2017">Reed Tech Annual Trademark XML (Back files)</a></b></li>
</ul>
The TM assignments data is made available on the portal in XML format on a daily basis:
<ul>
<li><b><a href="http://patents.reedtech.com/tmassign.php">Reed Tech IP Services, "USPTO Data Portal: Trademark Daily XML Files - Assignments,"</a></b></li>
</ul>
The TM assignnents back file is made available on the portal in XML format:
<ul>
<li><b><a href="http://patents.reedtech.com/tmassign.php#1980-2017">Reed Tech IP Services, "USPTO Data Portal: Trademark  XML Files - Assignments: 1980-2017"</a></b></li>
</ul>
The collection of ZIP files consists of daily trademark assignments (front files) of text derived from trademark assignment recordations at the USPTO. The TM assignment annual XML data (backfiles) are available for download from either the  the USPTO Bulk Data Storage System (BDDS) or Reed Tech site and contain data created annually containing an aggregation of all trademark assignments from August 1980 to the 2017:
<ul>
<li><b><a href="https://bulkdata.uspto.gov/data3/trademark/dailyxml/assignments/">USPTO Bulk Data Storage System (BDSS) Trademark Annual XML Assignments</a></b></li>
</ul>
 
The TM annual bulk download files are available for download from either the USPTO Bulk Data Site or the Reed Tech site and consist of a series of ZIP files containing all trademark data from April 7, 1884  through the last day of the previous year. Once unzipped, the concatenated XML files range in size from roughly 400 MB to 3 GB and contain upwards of 80,000 trademark records per file. The files are too large to be opened with most standard text editors or IDEs for viewing.  Some commercial XML tools such as Oxygen XML Editor support viewing files of this size but these tools require a license.
There are currently 59 TM annual ZIP files in the series containing all trademark data through the end of 2017. The annual TM files can be distinguished from the daily TM XML ZIP files available on the site by the file names. Annual files are named using the last day of the year following by the series number (1-59):
<br>
<br>i.e.
<br>
apc171231-01.zip
<br>…
<br>apc171231-59.zip
<br>
<br>
Daily XML files are named using the date with no series number:
<br>
i.e.
<br>apc180101.zip

<br>
The trademark splitter is a Python based utility which separates out the trademarks contained within each bulk download file and then builds a corpus using a directory structure based on name and date of the ZIP file. The utility currently supports both the TM daily bulk download files(front files)  as well as the TM annual bulk download files (back files). The Python TM splitter tool uses a buffered reader to read and process the large XML input file in chunks so it won’t run out of memory.
<br>
For each individual trademark extracted from the bulk XML file, the TM splitter creates  2 files:
<ul>
<li><b>complete trademark containing all fields in USPTO standard trademark XML format</b></li>
<li><b>file containing a subset of fields in Solr ready XML format</b></li>
</ul>
The splitter uses regular expressions to match and extract the fields that are then exported to Solr ready XML format. Fields currently supported by the tool include  the following:
<ul>
<li><b>trademark serial number used as the unique document id in Solr</b></li>
<li><b>mark name</b></li>
<li><b>mark drawing code</b></li>
<li><b>design codes</b></li>
<li><b>goods and services codes and descriptions</b></li>

## Required software
The tool was built and tested using Python 3.6  which can be downloaded from <b><a href="http://www.python.org">http://www.python.org</a></b>.
<br>Install Python 3.6 and run the following command from a command/terminal/shell window in order to confirm the version :
<br>
C:\TrademarkPublicData\TMProcessing>python -V
<br>
Python 3.6.0

## Data download
The tool can be tested with the following trademark annual XML input file:
<br>
<br>
<b><a href="https://bulkdata.uspto.gov/data/trademark/dailyxml/applications/apc171231-56.zip">apc171231-56.zip</a></b>
<br>
<br>
Unzip the file to a location with plenty of storage and confirm that there is an XML file of the same name:
<br>
i.e. e:\TMData\Applications_XML\apc171231-56.zip

<br>
The annual XML ZIP files are named using the last day of the previous year and the sequence number. For example, the file “acp171231-56.zip” is one of 59 files that together represent a snapshot of all USPTO registered trademarks as of Dec. 31, 2017. This sample file contains 82,652 trademark records. It is 106 MB zipped and 1.72 GB unzipped.

<br>
The tool can be tested with the following trademark daily XML input file:
<br>
<b><a href="https://bulkdata.uspto.gov/data/trademark/dailyxml/applications/apc180329.zip">apc180329.zip</a></b>
<br>
Unzip the file and confirm that there is an XML file with the same name:
<br>
i.e. apc180329.xml
<br>
Daily XML files are named using the date with no series number and only contain trademark records for a single day. This file contains 28575 records for all trademark transactions for March 29th, 2017.

<br>
The complete set of annual XML files form a snapshot of the USPTO public trademark data as of the last day of the previous year. In order to build an up to date trademark corpus representing all publicly available trademark data, the splitter must first process all annual XML files.  The splitter can then process all daily XML files up to the previous day which includes all changes since the snapshot was published on the last day of the previous year.

## Running the tool
Copy the Python script to the same directory at the XML test data:
<br>
i.e. C:\TrademarkPublicData\TMProcessing\tm_splitter.py

<br>
Launch a command line tool such as the Windows command prompt, Cygwin or other shell window.
<br>
Navigate to the installation directory:
<br>
$ cd C:\TrademarkPublicData\TMProcessing

<br>
Run the utility by providing the name of the input XML file and location of output directory as command line arguments:

<br>
$python tm_splitter.py -i e:\TMData\Applications_XML\apc161231-56.xml -d c:\tm_corpus

<br>
The utility will echo status messages to standard output as it builds a trademark corpus under the directory specified on the command line using the input file:
<br>
Number of arguments:  5 arguments
<br>
Argument List: ['D:\\TrademarkPublicData\\TMProcessing\\tm_splitter.py', '-i', 'e:\\TMData\\Applications_XML\\apc161231-56-87275954.xml', '-d', 'c:\\tm_corpus']
<br>
Argv:  ['-i', 'e:\\TMData\\Applications_XML\\apc161231-56-87275954.xml', '-d', 'c:\\tm_corpus']
<br>
reading input file:
<br>
e:\TMData\Applications_XML\apc161231-56-87275954.xml
<br>
using record separator:
</case-file>

<br>
read buffer size in bytes:
4096
<br>
reading TMs...please wait...
<br>
processing tms:
<br>
processing tm number:  1  /  1
<br>
1
<br>
tm_file:  87275954.xml
<br>
tm_file_solr: solr_87275954.xml

<br>
c:\\tm_corpus/apc161231-56-87275954/87275954.xml'
<br>
tm file creation complete

<br>
creating Solr ready XML file:
<br>
c:\\tm_corpus/apc161231-56-87275954/solr/solr_87275954.xml'

<br>
tm Solr file creation complete

<br>
tm processing summary:
<br>
Number of lines processed from input file:
<br>
Number of tm classifications extracted:
1
<br>Number of opening xml elements matched:
0
<br>Number of doctype elements matched:
0
<br>Number of start tm elements matched:
1
<br>Number of end tm elements matched: 
1
<br>Number of complete tms matched:
1
<br>Corpus created under output directory:
<br>c:\tm_corpus
<br>tm processing complete


<br>After the tool has completed processing, confirm that files were created for each trademark under the directory specified on the command line.
<br>The utility will create a corpus structure using the input file name for directory name and trademark serial number for file name:
<br>i.e. 
<ul>
<li><b>c:\tm_corpus\apc161231-56-87275954\87275954.xml</b></li>
<li><b>c:\tm_corpus\apc161231-56-87275954\solr\solr_87275954.xml</b></li>
</ul>

## Setting up PyDev with Eclipse
The following versions of PyDev are compatible with Eclipse:
<ul>
<li><b>Eclipse 4.6 (Nyon), Java 8: PyDev 5.5</b></li>
<li><b>Eclipse 4.5, Java 8: PyDev 5.2.0</b></li>
<li><b>Eclipse 3.8, Java 7: PyDev 4.5.5</b></li>
<li><b>Eclipse 3.x, Java 6: PyDev 2.8.2</b></li>
</ul>

<br>i.e. MyEclipse version 2016 CI 7 uses Eclipse 4.5
<br>Configure Eclipse 4.5 with PyDev 5.2 

<br>Read the notes on the manual installation of PyDev with Eclipse:
<b><a href="http://www.pydev.org/manual_101_install.html">PyDev Install Manual 101</a></b>

<br>Download the PyDev zip file:
<br>i.e. To download the PyDev 5.2 zip use the following link:
<br><b><a href= "https://superb-dca2.dl.sourceforge.net/project/pydev/pydev/PyDev%205.2.0/PyDev%205.2.0.zip">PyDev 5.2</a></b>
<br>C:\Users\mdhen_000\Downloads\PyDev_5.2.0.zip

<br>Copy the PyDev 5.2 zip to the Eclipse dropins directory and unzip:
<br>i.e.
<br>C:\MyEclipse2016CI\dropins\PyDev5.2.0.zip
<br>C:\MyEclipse2016CI\dropins\org.python.pydev.mylyn.feature_0.3.0.zip

<br>Restart MyEclipse

##Creating Python project in Eclipse:
Create Eclipse project for tm_splitter.py

<br>Navigate to  Package Explorer tab in Eclipse:
<br>Right mouse click:
<br>Select New->Project->Other->Pydev->PyDev Project
<br>Name: Python_TM_Splitter
<br>Grammar:  3.0-3.5
<br>Interpreter: C:\Python3.6\python.exe

##Link to source code from Python project:
<br>Right mouse from Package Explorer
<br>New->Folder->Advanced
<br>Select: Link to alternate location (Linked folder) ->Browse
<br>Select: C drive:
<br>C:\TrademarkPublicData\TMProcessing\
<br>This will link to the external files and not create them in the workspace itself.

##Configuring Preferences in Eclipse:
<br>Windows->Preferences->PyDev->Interpreters:
<br>Python 3.6:
<br>C:\Python3.6\python.exe
<br>Windows->Preferences->PyDev->Editor:
<br>Hover->PyDevDocstring Hover->Unchecked

##Open PyDev Perspective:
<br>Right mouse click Open Perspective icon with plus symbol in right hand corner of tool bar
<br>Open Perspective-> PyDev

## Notice
This source code is a work in progress and has not been fully vetted for a production environment. 


## Other Information
The United States Department of Commerce (DOC)and the United States Patent and Trademark Office (USPTO) GitHub project code is provided on an ‘as is’ basis without any warranty of any kind, either expressed, implied or statutory, including but not limited to any warranty that the subject software will conform to specifications, any implied warranties of merchantability, fitness for a particular purpose, or freedom from infringement, or any warranty that the documentation, if provided, will conform to the subject software.  DOC and USPTO disclaim all warranties and liabilities regarding third party software, if present in the original software, and distribute it as is.  The user or recipient assumes responsibility for its use. DOC and USPTO have relinquished control of the information and no longer have responsibility to protect the integrity, confidentiality, or availability of the information. 

User and recipient agree to waive any and all claims against the United States Government, its contractors and subcontractors as well as any prior recipient, if any.  If user or recipient’s use of the subject software results in any liabilities, demands, damages, expenses or losses arising from such use, including any damages from products based on, or resulting from recipient’s use of the subject software, user or recipient shall indemnify and hold harmless the United States government, its contractors and subcontractors as well as any prior recipient, if any, to the extent permitted by law.  User or recipient’s sole remedy for any such matter shall be immediate termination of the agreement.  This agreement shall be subject to United States federal law for all purposes including but not limited to the validity of the readme or license files, the meaning of the provisions and rights and the obligations and remedies of the parties. Any claims against DOC or USPTO stemming from the use of its GitHub project will be governed by all applicable Federal law. “User” or “Recipient” means anyone who acquires or utilizes the subject code, including all contributors. “Contributors” means any entity that makes a modification. 

This agreement or any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not in any manner constitute or imply their endorsement, recommendation or favoring by DOC or the USPTO, nor does it constitute an endorsement by DOC or USPTO or any prior recipient of any results, resulting designs, hardware, software products or any other applications resulting from the use of the subject software.  The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, including USPTO, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC, USPTO  or the United States Government.

<br />
<br />
<p xmlns:dct="http://purl.org/dc/terms/" xmlns:vcard="http://www.w3.org/2001/vcard-rdf/3.0#">
  <a rel="license"
     href="http://creativecommons.org/publicdomain/zero/1.0/">
    <img src="http://i.creativecommons.org/p/zero/1.0/88x31.png" style="border-style: none;" alt="CC0" />
  </a>
  <br />
  To the extent possible under law,
  <a rel="dct:publisher"
     href="https://github.com/USPTO/PatentPublicData">https://github.com/USPTO/PatentPublicData</a>
  has waived all copyright and related or neighboring rights to
  <span property="dct:title">Patent Public Data</span>.
This work is published from:
<span property="vcard:Country" datatype="dct:ISO3166"
      content="US" about="https://github.com/USPTO/PatentPublicData">
  United States</span>.
</p>
