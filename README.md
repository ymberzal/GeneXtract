# GeneXtract
GeneXtract is an easy to use Python GUI tool to parse through GFF or GTF files from NCBI and extract gene symbols. 
GeneXtract extracts the gene symbols from either GTF or GFF file uploaded by the user.
Window size specifies base pair positions on either side of the chromosome position as mentioned in the BED file. If the BED file contains, for example, NC_037330.1 113368116 113368116 and the provided window size is 20000, the GeneXtract script parses through the GTF or GFF file and extracts out genes from: 113348116 to 113388116 
The chromosome numbers provided in the BED file must match with the chromosome numbers in the GFF or GTF file. If the BED file contains chromosomes as 1,2,3..and so on, the chromosomes on GTF/GFF file must be renamed accordingly. This can be achieved with the awk command. 
Install python3 
Install Tkinter package: sudo apt install python3-tk
If working directly with the sccript, open the terminal and type python3 GeneXtract.py
To compile the script in executable file:
Install pyinstaller: pip install pyinstaller
Run pyinstaller with the command: pyinstaller --onefile GeneXtract.py 
Double click the executable to run it
