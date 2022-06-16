# write your code here
import gzip
from collections import Counter
archive_files = []
archive_results = {}
for archives in range(3):
    archive_files.append(input())
for file_name in archive_files:
    with gzip.open(file_name, 'r') as data:
        lines = []
        for line in data:
            line = line.decode('UTF-8')
            lines.append(line.rstrip())
    sequences = []
    cg_total = 0
    sequence_length = 0
    reads = 0
    for index in range(len(lines)):
        if '@SRR' in lines[index]:
            line = lines[index + 1]
            sequences.append(line)
            length = len(line)
            sequence_length += length
            reads += 1
            cg = (line.count('G') + line.count('C')) / length
            cg_total += cg
    ave_length = round(sequence_length / reads)
    cg_ave = round((cg_total / reads) * 100, 2)
    duplicates = Counter(sequences)
    repeats = sum(duplicates[i] - 1 for i in duplicates if duplicates[i] - 1 > 0)
    ns = [n.count('N') / len(n) * 100 for n in duplicates if 'N' in n]
    reads_with_ns = len(ns)
    ns_per_read = round(sum(ns) / reads, 2)
    archive_results[file_name] = [reads, ave_length, repeats, reads_with_ns, cg_ave, ns_per_read]

combined_read_n = {key: repeats + reads_with_ns for key in archive_results}
best = min(combined_read_n, key=combined_read_n.get)
reads, average_length, repeats, reads_with_ns, cg_average, ns_per_read = archive_results[best]
print(f'Reads in the file = {reads}:')
print(f'Reads sequence average length = {average_length}')
print(f'Repeats = {repeats}')
print(f'Reads with Ns = {reads_with_ns}')
print(f'GC content average = {cg_average}%')
print(f'Ns per read sequence = {ns_per_read}%')
