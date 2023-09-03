import tkinter as tk
from tkinter import filedialog

def parse_gff(file_path):
    gene_data = {}
    with open(file_path, 'r') as gff_file:
        for line in gff_file:
            if line.startswith('#'):
                continue
            fields = line.strip().split('\t')
            feature_type = fields[2] 
            if feature_type == 'gene':
                chromosome = fields[0]
                start = int(fields[3])
                end = int(fields[4])
                attributes = fields[8].split(';')
                gene_name = None
                for attribute in attributes:
                    if attribute.startswith('Name='):
                        gene_name = attribute.split('=')[1]
                        break
                if gene_name:
                    gene_data[gene_name] = (feature_type, chromosome, start, end)
    return gene_data

def parse_gtf(file_path):
    gene_data = {}
    with open(file_path, 'r') as gtf_file:
        for line in gtf_file:
            if line.startswith('#'):
                continue
            fields = line.strip().split('\t')
            feature_type = fields[2]  
            if feature_type == 'gene':
                chromosome = fields[0]
                start = int(fields[3])
                end = int(fields[4])
                attributes = fields[8].split(';')
                gene_name = None
                for attribute in attributes:
                    if attribute.strip():
                        key, value = attribute.strip().split(" ", 1)
                        if key == 'gene_id':
                            gene_name = value.strip("\"")
                            break
                if gene_name:
                    gene_data[gene_name] = (feature_type, chromosome, start, end)
    return gene_data

def parse_file(file_path, file_type):
    if file_type == 'GFF':
        return parse_gff(file_path)
    elif file_type == 'GTF':
        return parse_gtf(file_path)
    else:
        return {}
        
def find_genes_in_range(gene_data, bed_file_path, range_distance=50000):
    result_text.delete(1.0, tk.END)
    
    with open(bed_file_path, 'r') as bed_file:
        for line_number, line in enumerate(bed_file, start=1):
            fields = line.strip().split('\t')
            if len(fields) < 3:
                result_text.insert(tk.END, f"Error: Line {line_number} in BED file does not have enough columns.\n")
                continue
            
            chromosome = fields[0]
            try:
                start = int(fields[1])
                end = int(fields[2])
            except ValueError:
                result_text.insert(tk.END, f"Error: Line {line_number} in BED file contains non-numeric start or end position.\n")
                continue

            genes_within_range = []

            result_text.insert(tk.END, f"{chromosome}:{start}-{end}\n")
            
            for gene_name, (feature_type, gene_chromosome, gene_start, gene_end) in gene_data.items():
                if gene_chromosome == chromosome and abs(gene_start - start) <= range_distance:
                    genes_within_range.append((gene_name, gene_start, gene_end))

            genes_within_range.sort(key=lambda x: x[1])

            if genes_within_range:
                for gene_name, gene_start, gene_end in genes_within_range:
                    gene_relative_start = max(gene_start, start)
                    gene_relative_end = min(gene_end, end)
                    gene_display = f"{gene_name}\t|\t{gene_start}-{gene_end} ({gene_relative_start}-{gene_relative_end})"
                    result_text.insert(tk.END, f"{gene_display}\n")
            else:
                result_text.insert(tk.END, "No gene in the specified range\n")
            result_text.insert(tk.END, "\n")

def browse_gff():
    file_path = filedialog.askopenfilename(title="Select GFF File", filetypes=[("GFF files", "*.gff")])
    gff_entry.delete(0, tk.END)
    gff_entry.insert(0, file_path)

def browse_gtf():
    file_path = filedialog.askopenfilename(title="Select GTF File", filetypes=[("GTF files", "*.gtf")])
    gtf_entry.delete(0, tk.END)
    gtf_entry.insert(0, file_path)

def browse_bed():
    file_path = filedialog.askopenfilename(title="Select BED File", filetypes=[("BED files", "*.bed")])
    bed_entry.delete(0, tk.END)
    bed_entry.insert(0, file_path)

def save_results_to_file():
    result_content = result_text.get(1.0, tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    with open(file_path, 'w') as file:
        file.write(result_content)

def process_files():
    gff_file_path = gff_entry.get()
    gtf_file_path = gtf_entry.get()
    bed_file_path = bed_entry.get()
    range_distance = int(range_entry.get())

    gene_data = {}
    if gff_file_path:
        gene_data.update(parse_gff(gff_file_path))
    if gtf_file_path:
        gene_data.update(parse_gtf(gtf_file_path))

    find_genes_in_range(gene_data, bed_file_path, range_distance)

    tk.Button(root, text="Save Results", command=save_results_to_file, bg="#8e24aa", fg="white").grid(row=7, column=0, columnspan=3, padx=5, pady=10)

root = tk.Tk()
root.title("GeneXtract")
root.configure(bg="#f0f0f0")  

root.configure(bg="#f0f0f0")  
tk.Label(root, text="GFF File:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
gff_entry = tk.Entry(root, width=50)
gff_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=browse_gff, bg="#e57373", fg="white").grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="GTF File:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
gtf_entry = tk.Entry(root, width=50)
gtf_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=browse_gtf, bg="#64b5f6", fg="white").grid(row=1, column=2, padx=5, pady=5)

tk.Label(root, text="BED File:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)
bed_entry = tk.Entry(root, width=50)
bed_entry.grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=browse_bed, bg="#81c784", fg="white").grid(row=2, column=2, padx=5, pady=5)

tk.Label(root, text="Window Size:", bg="#f0f0f0").grid(row=3, column=0, padx=5, pady=5)
range_entry = tk.Entry(root, width=10)
range_entry.grid(row=3, column=1, padx=5, pady=5)
range_entry.insert(0, "50000")

tk.Button(root, text="Process Files", command=process_files, bg="#ffa726", fg="white").grid(row=4, column=0, columnspan=3, padx=5, pady=10)

result_text = tk.Text(root, wrap=tk.WORD, width=60, height=10)
result_text.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

developer_label = tk.Label(root, text="Developed by Ymberzal", bg="#f0f0f0", fg="blue")
developer_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()
