# ZombieGene Project

This is a bioinformatics pipeline designed to find gene families that have different intron patterns (Intron Loss/Gain). It marks exon-intron junctions with an 'X' to track them through sequence alignment.

## How it's organized

### Main Script
- `run_pipeline.py`: The main script to run everything.

### Source Files (`src/`)
Contains 6 steps of the analysis.

1. `1_stitch_and_blast.py`: Prepare sequences and run BLAST  
2. `2_build_matrix.py`: Create a distance matrix  
3. `3_hierarchical_clustering.py`: Group similar genes  
4. `4_grouping.py`: Put gene families into FASTA files  
5. `5_multialign.py`: Run ClustalW alignment  
6. `6_find_interesting_groups.py`: Find groups where 'X' positions don't match  

### Utilities
- `zombie_utils.py` : Helper functions for translation and file reading.

## Requirements

You need to have these installed:

- Python 3 (with `numpy` and `scipy`)
- `blastp` and `makeblastdb`
- `clustalw2`

## How to run
You can run the full analysis with one command:
```bash
python3 run_pipeline.py <GFF3_FILE> <FASTA_FILE> <TRIAL_NAME>
```
Example:
```bash
python3 run_pipeline.py ./test_data/at.gff3.gz ./test_data/at.fa.gz my_test
```

## Results

The results will be saved in the `build/` folder under your chosen trial name:

`groups/`: Individual FASTA files for each gene family.

`multi_aln/`: Alignment results.

Terminal Output: The names of "Interesting Groups" (where introns are different) will be printed on your screen.