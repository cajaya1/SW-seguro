import pandas as pd
from pydriller import Repository
import os
import time

# --- CONFIGURACIÓN ---
# Lista de Repositorios para Minería Profunda
# Puedes agregar o quitar según tu espacio en disco.
REPO_URLS = [
    "https://github.com/pallets/flask.git",
    "https://github.com/django/django.git",
    "https://github.com/requests/requests.git",
    "https://github.com/ansible/ansible.git",
    "https://github.com/keras-team/keras.git"
]

KEYWORDS = ["security", "vulnerability", "cve", "fix", "patch", "denial of service", "xss", "injection"]
EXTENSIONS = (".py", ".js", ".java", ".cpp", ".ts")
ARCHIVO_SALIDA = "dataset_local.csv"
CARPETA_REPOS = "repos_descargados" # Aquí se guardarán los clones

# Crear carpeta para repos si no existe
if not os.path.exists(CARPETA_REPOS):
    os.makedirs(CARPETA_REPOS)

# Inicializar CSV si no existe
if not os.path.exists(ARCHIVO_SALIDA):
    pd.DataFrame(columns=["repo", "sha", "filename", "code", "label"]).to_csv(ARCHIVO_SALIDA, index=False)
    print(f"New file created: {ARCHIVO_SALIDA}")
else:
    print(f"Existing file detected: {ARCHIVO_SALIDA}. New data will be appended.")

print(f"Starting deep local mining process")
print(f"Repositories will be cloned to: ./{CARPETA_REPOS} (This will save time on restarts)\n")

for url in REPO_URLS:
    repo_name = url.split("/")[-1].replace(".git", "")
    print(f"--- Procesando Repositorio: {repo_name} ---")
    
    # Buffer para guardar por lotes y no escribir en disco a cada segundo
    buffer = []
    count_v = 0
    count_s = 0
    
    try:
        # Pydriller handles cloning. 'clone_repo_to' saves the repository locally.
        # If it already exists, Pydriller uses it and only performs 'git pull' for faster processing
        repo_mining = Repository(path_to_repo=url, clone_repo_to=CARPETA_REPOS)
        
        for commit in repo_mining.traverse_commits():
            try:
                # 1. Filtro de Mensaje
                msg = commit.msg.lower()
                if any(k in msg for k in KEYWORDS):
                    
                    for file in commit.modified_files:
                        # 2. Filtro de Archivo y Contenido
                        if file.filename.endswith(EXTENSIONS) and file.source_code_before and file.source_code:
                            
                            # --- CAPTURA: ANTES DEL FIX (VULNERABLE - CLASE 1) ---
                            buffer.append({
                                "repo": repo_name,
                                "sha": commit.hash,
                                "filename": file.filename,
                                "code": file.source_code_before,
                                "label": 1
                            })
                            count_v += 1

                            # --- CAPTURA: DESPUÉS DEL FIX (SEGURO - CLASE 0) ---
                            buffer.append({
                                "repo": repo_name,
                                "sha": commit.hash,
                                "filename": file.filename,
                                "code": file.source_code,
                                "label": 0
                            })
                            count_s += 1
                
                # Intermediate save every 100 records for safety
                if len(buffer) >= 100:
                    df_chunk = pd.DataFrame(buffer)
                    df_chunk.to_csv(ARCHIVO_SALIDA, mode='a', header=False, index=False)
                    buffer = [] # Clear buffer
                    print(f"Partial save completed: {count_v} vulnerable, {count_s} secure files accumulated...")

            except Exception as e:
                # If a commit fails, continue to the next one
                continue
        
        # Final save for the current repository
        if buffer:
            pd.DataFrame(buffer).to_csv(ARCHIVO_SALIDA, mode='a', header=False, index=False)
        
        print(f"Completed {repo_name}. Total found: {count_v} Vulnerable / {count_s} Secure files.\n")

    except Exception as e:
        print(f"Critical error in {repo_name}: {e}")
        continue

print(f"\nMining process completed. Data saved to '{ARCHIVO_SALIDA}'.")