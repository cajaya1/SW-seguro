import pandas as pd
import os
import random

# --- CONFIGURACIÓN ---
INPUT_FILE = "dataset_local.csv"
OUTPUT_FILE = "dataset_contraste.csv"
CARPETA_REPOS = "repos_descargados" # Donde se clonaron los repos en el paso 1
EXTENSIONS = (".py", ".js", ".java", ".cpp", ".ts")

print("Starting dataset repair process (contrast strategy)")

# 1. Recover vulnerable samples from previous mining
# These are valuable as they come from real security commits
try:
    df_original = pd.read_csv(INPUT_FILE)
    df_vuln = df_original[df_original['label'] == 1]
    # Remove duplicates
    df_vuln = df_vuln.drop_duplicates(subset=['code'])
    print(f"Recovered {len(df_vuln)} vulnerable files (Class 1).")
except:
    print("Error: dataset_local.csv file not found")
    exit()

# 2. Search for secure files (random sampling) from repositories
# Assumption: random files from repositories are 'secure' to generate contrast
print("Searching for normal files in downloaded repositories...")

safe_files = []
target_safe_count = len(df_vuln) # Balanced dataset (50/50 ratio)

# Traverse repository folders
all_files = []
for root, dirs, files in os.walk(CARPETA_REPOS):
    for file in files:
        if file.endswith(EXTENSIONS):
            full_path = os.path.join(root, file)
            all_files.append(full_path)

# Shuffle and select randomly
random.shuffle(all_files)

print(f"   Found {len(all_files)} total files on disk.")

count = 0
for path in all_files:
    if count >= target_safe_count:
        break
    
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()
            
        # Basic filter: non-empty and minimum size threshold
        if len(code) > 50:
            safe_files.append({
                "repo": "random_sample",
                "sha": "n/a",
                "filename": path,
                "code": code,
                "label": 0 # CLASS 0 = SECURE (GENERIC)
            })
            count += 1
    except:
        continue

df_safe = pd.DataFrame(safe_files)
print(f"Collected {len(df_safe)} secure files (Class 0).")

# 3. Combine and save datasets
df_final = pd.concat([df_vuln, df_safe])
# Shuffle all data
df_final = df_final.sample(frac=1, random_state=42).reset_index(drop=True)

df_final.to_csv(OUTPUT_FILE, index=False)
print(f"\nNew dataset saved: {OUTPUT_FILE}")
print(f"Total records: {len(df_final)}")
print("   Model will now compare 'Real Vulnerabilities' vs 'Normal Code'.")
print("   This approach should significantly improve accuracy.")