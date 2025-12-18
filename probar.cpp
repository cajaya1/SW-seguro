// vulnerable_overflow.cpp
#include <iostream>
#include <cstring>
#include <cstdlib>

using namespace std;

// Función gigante y peligrosa
void process_admin_command(char* input_str) {
    // PELIGRO: Buffer Overflow clásico
    // El buffer es de 50, pero strcpy no revisa si el input es mayor. 
    char buffer[50];
    char command[100];
    
    // Complejidad ciclomática innecesaria
    if (input_str != NULL) {
        int len = 0;
        while(input_str[len] != '\0') {
            len++;
        }

        if (len > 0) {
            // PELIGRO: Copia insegura de memoria
            strcpy(buffer, input_str);
            
            // Lógica de autenticación pobre
            if (strcmp(buffer, "admin") == 0) {
                cout << "Access Granted" << endl;
                
                // PELIGRO: Command Injection
                // Un atacante puede poner: "admin; rm -rf /"
                strcpy(command, "echo User logged in: ");
                strcat(command, buffer);
                
                // Ejecuta comando del sistema operativo
                system(command);
            } else {
                for(int i=0; i<5; i++) {
                    cout << "Access Denied..." << endl;
                }
            }
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cout << "Usage: program <name>" << endl;
        return 1;
    }
    process_admin_command(argv[1]);
    return 0;
}