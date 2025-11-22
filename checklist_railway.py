#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Checklist interactivo para desplegar en Railway
"""

import os
import subprocess

CHECKLIST = [
    ("Instalar Railway CLI", "npm install -g @railway/cli"),
    ("Verificar Python 3.11+", "python --version"),
    ("Instalar dependencias", "cd backend && pip install -r requirements.txt"),
    ("Probar API localmente", "cd backend && python run.py"),
    ("Ejecutar tests", "cd backend && python test_api.py"),
    ("Inicializar Railway", "railway init"),
    ("Desplegar backend", "railway up"),
    ("Configurar variables", "railway variable"),
    ("Verificar despliegue", "railway logs"),
]

def print_header():
    """Imprime el encabezado"""
    print("\n" + "█" * 60)
    print("█  CHECKLIST DESPLIEGUE RAILWAY")
    print("█" * 60 + "\n")

def print_item(index, item, completed):
    """Imprime un item del checklist"""
    status = "✓" if completed else "○"
    print(f"  [{status}] {index}. {item[0]}")

def main():
    """Menú principal"""
    
    completed = [False] * len(CHECKLIST)
    
    while True:
        print_header()
        
        # Mostrar checklist
        for i, (title, _) in enumerate(CHECKLIST, 1):
            print_item(i, (title,), completed[i-1])
        
        # Progreso
        completed_count = sum(completed)
        progress = int((completed_count / len(CHECKLIST)) * 20)
        print(f"\n  Progreso: [{'█' * progress}{'░' * (20 - progress)}] {completed_count}/{len(CHECKLIST)}")
        
        print("\nOpciones:")
        print("  1-9: Marcar paso como completado")
        print("  r:   Revertir un paso")
        print("  e:   Ejecutar comando")
        print("  s:   Saltar al despliegue")
        print("  q:   Salir")
        
        choice = input("\nSelecciona opción: ").strip().lower()
        
        if choice == "q":
            break
        elif choice == "e":
            step = input("Número del paso a ejecutar (1-9): ").strip()
            try:
                idx = int(step) - 1
                if 0 <= idx < len(CHECKLIST):
                    cmd = CHECKLIST[idx][1]
                    print(f"\n$ {cmd}\n")
                    os.system(cmd)
                    completed[idx] = input("\n¿Completado? (s/n): ").lower() == "s"
            except ValueError:
                print("Número inválido")
        elif choice == "r":
            step = input("Número del paso a revertir (1-9): ").strip()
            try:
                idx = int(step) - 1
                if 0 <= idx < len(CHECKLIST):
                    completed[idx] = False
            except ValueError:
                print("Número inválido")
        elif choice == "s":
            if all(completed):
                print("\n✓ ¡Todos los pasos completados!")
                print("Despliegue listo para Railway")
                break
            else:
                print("\n⚠️  No todos los pasos están completos")
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(CHECKLIST):
                    completed[idx] = not completed[idx]
            except ValueError:
                print("Opción inválida")
        
        input("\nPresiona Enter para continuar...")
        os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    main()
