OVERVIEW

These scripts are currently supported on Windows only. They allow you to run Pro API queries based on input CSV files, pull down the raw JSON, and then parse result data points out of that JSON to generate an output CSV file.

HOW TO USE THE SCRIPTS

1. Initial one-time setup: copy the WPPBatch folder to your own machine wherever you like. Open WPPBatch/wppbatch.ini and edit it as needed to your preferences.

2. Generate an input CSV file that has columns containing input parameters that you want to submit to the search, e.g. phones, names, addresses, etc. You can also include any other internal identifiers or any other extra data columns that you want, and these will be passed through to the output file. The CSV file requires a header.

3. Drag and drop your CSV file onto the appropriate Search*.bat script. For example, if you want to search on phone numbers, then drag a CSV file containing phones onto SearchPhone.bat.

4. Follow the instructions on screen to map input columns from your CSV file to the search input parameters.

5. The script will run and generate a new raw results file in the same directory as your source file. The raw results file is basically a copy of your input file, with "_rawresults" appended to the filename, and two new columns appended to the content of the file: one column defines the API URL that was loaded, and another column contains raw JSON response.

6. The last step is to drag the raw results file onto the appropriate Extract*.bat script. Most search types just have one  Extract script, e.g. ExtractFindPerson.bat is associated with SearchPerson.bat. However, for phone solutions there are several options based on whether you want to extract a Phone Reputation result, Phone Intelligence, etc.

