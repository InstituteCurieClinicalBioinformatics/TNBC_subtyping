from argparse import ArgumentParser
import subprocess
from affy import *
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "scripts"))

def main(inFile, outDir, mode, dataset, split, threshold, gitDir):
    code = subprocess.call(f"Rscript {gitDir}/scripts/clustering.r -i {inFile} -o {outDir} -m {mode} -s {split}", shell=True)
    if code == 0:
        computeTestStats(os.path.join(outDir, "final_clusters.csv"), dataset, outDir)
        subprocess.call(f"Rscript {gitDir}/scripts/pathways.R -i {os.path.join(outDir, f'{dataset}_WithPval.csv')} -o {outDir} -t {threshold}", shell=True)

if __name__ == "__main__":
    parser = ArgumentParser(description="-Launch affymetrix analysis")

    parser.add_argument("-d", "--dataset", required=True, help="Dataset ID. Used to name output file.")
    parser.add_argument("-i", "--inputFile", required=True, help="Path to the input file.")
    parser.add_argument("-m", "--mode", required=True, help="Data type to cluster. Must be rnaseq or microarray", choices = ["rnaseq", "microarray"])
    parser.add_argument("-o", "--outDir", required=True, help="Path to the output folder. Must exists.")
    parser.add_argument("-s", "--split", help="Number of data split to perform for crossing gene name with probes name. Depending on specs machine, do not perform split can lead to out of memory exception", type=int, default=200)
    parser.add_argument("-t", "--threshold", help="Pvalue cutoff", type=float, default=0.05)

    args = parser.parse_args()
    gitDir = os.path.dirname(os.path.realpath(__file__))

    main(args.inputFile, args.outDir, args.mode, args.dataset, args.split, args.threshold, gitDir)