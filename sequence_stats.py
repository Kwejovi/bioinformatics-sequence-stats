"""
Bioinformatics Sequence Quality Pipeline
- Reads a FASTA file
- Calculates length and GC%
- Checks for ambiguous bases
- Filters sequences based on quality
- Saves results to CSV
- Saves cleaned sequences to a new FASTA file
"""

from Bio import SeqIO
import csv

# Input FASTA file
fasta_file = "sequences.fasta"
output_csv = "sequence_stats.csv"
clean_fasta = "clean_sequences.fasta"

# Quality thresholds (customize later if needed)
MIN_LENGTH = 200   # Remove short sequences
ALLOW_AMBIGUOUS = False

def calculate_gc(seq):
    g = seq.upper().count("G")
    c = seq.upper().count("C")
    return (g + c) / len(seq) * 100

def has_ambiguous(seq):
    ambiguous_bases = set("RYWSKMBDHVN")
    return any(base.upper() in ambiguous_bases for base in seq)

clean_records = []
results = []

for record in SeqIO.parse(fasta_file, "fasta"):
    seq = record.seq
    length = len(seq)
    gc_content = calculate_gc(seq)
    ambiguous = has_ambiguous(seq)

    results.append([
        record.id,
        length,
        round(gc_content, 2),
        ambiguous
    ])

    # Apply quality filters
    if length >= MIN_LENGTH and (ALLOW_AMBIGUOUS or not ambiguous):
        clean_records.append(record)

# Save results to CSV
with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Length (bp)", "GC %", "Ambiguous"])
    writer.writerows(results)

# Save cleaned FASTA for next steps
SeqIO.write(clean_records, clean_fasta, "fasta")

print("✅ Analysis complete!")
print(f"📄 Stats saved to: {output_csv}")
print(f"🧬 Clean sequences saved to: {clean_fasta}")
print(f"Total input sequences: {len(results)}")
print(f"Sequences passed QC: {len(clean_records)}")
