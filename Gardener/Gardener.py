#Gardener - phylogenetic trees trimmer

# imports :)

import argparse
import os
import re

def nexus_search(nexusfile):
    """
    Reads data from .nexus file, checks for taxa block and creates a sequence id list of sequences that were marked with any color other than black on the tree
    
    :param nexusfile: Path to a nexus file created for the tree
    """

    lineList = []

    with open(nexusfile, 'r') as file:
        for line in file:
            lineList.append(line)

    try:
        n = lineList.index('begin taxa;\n')
    except:
        raise Exception("The nexus file does not contain the taxa block. See the information about nexus file format.")

    trimList = []

    for line in lineList[n+1:]:
        if(line.lower()=="end;\n" or line.lower()=="end;"):
            break
        split = line.split("[")
        if(len(split[-1].split("=")) == 2 and split[-1].split("=")[0] == "&!color" and split[-1] != "&!color=#000000]\n"):
            trimList.append(re.sub("\n",'',re.sub("\t", '',''.join(split[:-1]))).replace("'", ""))

    return trimList


def fasta_trimmer(remove, fasta, out):
    """
    Searches for sequence names in fasta file and creates a fasta file that EXCLUDES those sequences
    
    :param remove: list of sequence names in fasta file that should be removed
    :param fasta: path to a fasta file that has to be trimmed
    :param out: path to an output file to save the trimmed results
    """

    g = True
    with open(out, "w") as outfile:
        for line in open(fasta):
            if( ">" in line):
                if( re.sub("\n","",re.sub(">","", line)) in remove):
                    g = False
                else:
                    g = True
                    print(line, end="", file=outfile)

            elif(g):
                print(line, end="", file=outfile)

if __name__ == "__main__":

##################################################################################
# declaring the parser and arguments to pass the arguments from console when running this script

    parser = argparse.ArgumentParser(prog="Gardener", description="Program for automating the tree trimming process.", epilog="")

    parser.add_argument('-n', action="store", required=True, dest='nfile', help="Full path to .nexus file with phylogenetic tree.")

    parser.add_argument('-f', action="store", required=True, dest='ffile', help="Full path to .fasta file with a list of sequences that have the same id's as .nexus file")

    parser.add_argument('-o', action="store", dest='ofile', help="Optional argument containing the path to output .fasta file. If not specified, the file will be saved in the same folder as input fasta file.")

    args = parser.parse_args()


##################################################################################
#Checking if passed arguments are okay 

    if not (os.path.exists(args.nfile)):
        raise Exception("The given treefile does not exist! Make sure you passed full path to the .nexus treefile witn --n argument")

    if(type(args.nfile) != str or args.nfile.split(".")[-1] != "nexus"):   
        raise Exception("The given treefile is not correct! A path to .nexus file should be specified with --n argument")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if not (os.path.exists(args.ffile)):
        raise Exception("The given fasta file does not exist! Make sure you passed full path to the .fasta treefile witn --f argument")

    if(type(args.ffile) != str or args.ffile.split(".")[-1] != "fasta"):
        raise Exception("The given fasta file is not correct! A path to .fasta file should be specified with --f argument")


#################################################################################
#Specifying the output path

    if args.ofile is None:
        outpath = re.sub("\\.[^\\.]+$", "_trimmed.", args.ffile) + re.sub(".*\\.", "", args.ffile)
    else:
        outpath = args.ofile

##################################################################################
# reading the nexus file. It should be provided as a .nexus file, then
# Searching for taxa subsection in the file and then selecting the branches that have a specified color that is different than black

    trimList = nexus_search(args.nfile)


###################################################################################
# reading the fasta file. It should be provided as a .fasta file. Does not matter whether its single- or multi-line

    fasta_trimmer(trimList, args.ffile, outpath)



        
        

     
               

		

