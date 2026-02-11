import os
import re
import csv
from pypdf import PdfReader

def extract_regex_from_pdfs():
    # Define directories and files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    downloads_dir = os.path.join(current_dir, "downloads")
    output_csv = os.path.join(current_dir, "resultado_busca_regex.csv")
    
    # Regex pattern
    regex_pattern = re.compile(r"DE ?\d{18,20}")
    
    results = []
    
    # Check if downloads directory exists
    if not os.path.exists(downloads_dir):
        print(f"Directory not found: {downloads_dir}")
        return

    print(f"Scanning PDFs in: {downloads_dir}")
    
    # Get list of PDF files
    pdf_files = [f for f in os.listdir(downloads_dir) if f.lower().endswith('.pdf')]
    total_files = len(pdf_files)
    
    print(f"Found {total_files} PDF files.")

    for i, filename in enumerate(pdf_files):
        filepath = os.path.join(downloads_dir, filename)
        try:
            reader = PdfReader(filepath)
            num_pages = len(reader.pages)
            pages_to_check = min(num_pages, 10)
            
            found_match = False
            match_text = ""
            
            for page_num in range(pages_to_check):
                page = reader.pages[page_num]
                text = page.extract_text()
                
                match = regex_pattern.search(text)
                if match:
                    match_text = match.group()
                    found_match = True
                    break
            
            if found_match:
                results.append([filename, match_text])
                print(f"[{i+1}/{total_files}] Match found in {filename}: {match_text}")
            else:
                 # Optional: print for no match to show progress, or keep it quiet
                 # print(f"[{i+1}/{total_files}] No match in {filename}")
                 pass

        except Exception as e:
            print(f"[{i+1}/{total_files}] Error processing {filename}: {e}")

    # Write results to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Filename", "Match"])
        writer.writerows(results)
        
    print(f"\nSearch complete. Results saved to {output_csv}")

if __name__ == "__main__":
    extract_regex_from_pdfs()
