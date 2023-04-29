import os
import random
import pandas as pd
import subprocess
import math
from pypdf import PdfMerger


def generate_pdf(template_path, output_path, v):
    # Génère un PDF à partir d'un modèle LaTeX, en remplaçant les variables.
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
        content = content.replace("{student_name}", v[0])
        for i, value in enumerate(v[1:], start=1):
            content = content.replace("{v%d}" % i, str(value))

    tex_output_path = output_path + ".tex"
    with open(tex_output_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    # Get the absolute path of the .tex file
    abs_tex_output_path = os.path.abspath(tex_output_path)

    # Compile the .tex file
    subprocess.run(["pdflatex", "-quiet", "-interaction=nonstopmode", abs_tex_output_path], cwd=os.path.dirname(tex_output_path))
    
    # Clean up temporary files
    for ext in [".aux", ".log", ".tex"]:
        os.remove(output_path + ext)

def create_homework(student_name, v, homework_name):
    # Crée un devoir personnalisé pour un élève.
    output_path = os.path.join(homework_name, f"{homework_name}_{student_name.replace(' ', '_')}")
    generate_pdf('template.tex', output_path, v)

def create_solution(student_name, v, homework_name):
    # Crée un corrigé personnalisé pour un élève.
    output_path = os.path.join(homework_name + '_Corrige', f"{homework_name}_corrige_{student_name.replace(' ', '_')}")
    generate_pdf('template_c.tex', output_path, v)

def read_students(file_path):
    #Lit un fichier CSV contenant la liste des élèves et retourne une liste de noms.
    #Présume que "NOM Prénom" est dans la première colonne à partir de la troisième ligne (format quand on charge sur pronote).
    df = pd.read_csv(file_path, sep = ';', skiprows=2, header=None)
    return df[0].tolist()

def main():
    # Lecture du fichier "eleves.csv" et récupération des noms des élèves.
    students = read_students("eleves.csv")
            
    # Demande le titre du devoir pour préfixer les fichiers et créer les sous-dossiers.
    print('Nom du devoir:')
    homework_name = input()

    # Création des sous-dossiers pour les devoirs et les corrigés.
    os.makedirs(homework_name, exist_ok=True)
    os.makedirs(homework_name+'_Corrige', exist_ok=True)

    for student in students:
        # Génération des valeurs aléatoires pour chaque élève, placées dans une liste 'v'.
        v = [random.randint(2, 8) for _ in range(100)]

        # Ajout du nom de l'élève en première position de la liste 'v'.
        v[0]=student
                
        # Personnalisation des valeurs spécifiques pour le devoir et le corrigé selon les besoins.
        #......
               
               
               
               
               
               
        # Création du devoir et du corrigé pour l'élève.
        create_homework(student, v, homework_name)
        print(f'Devoir de {student} prêt.')
        create_solution(student, v, homework_name)
        print(f'Corrigé du devoir de {student} prêt.')
        
    # Fusion des PDF dans les sous-dossiers pour créer un PDF unique pour la classe.
    script_directory = os.path.dirname(os.path.abspath(__file__))
    homework_path = os.path.join(script_directory, homework_name)
    solution_path = os.path.join(script_directory, homework_name + '_Corrige')

    
    # Fusion des devoirs.
    merger = PdfMerger()
    for student in students:
        pdf_file = f"{homework_name}_{student.replace(' ', '_')}.pdf"
        file_path = os.path.join(homework_path, pdf_file)
        if os.path.isfile(file_path):
            merger.append(file_path)
    merged_pdf_path = os.path.join(script_directory, homework_name + '.pdf')
    merger.write(merged_pdf_path)
    merger.close()
    
    # Fusion des corrigés.
    merger = PdfMerger()
    for student in students:
        pdf_file = f"{homework_name}_corrige_{student.replace(' ', '_')}.pdf"
        file_path = os.path.join(solution_path, pdf_file)
        if os.path.isfile(file_path):
            merger.append(file_path)
    merged_pdf_path = os.path.join(script_directory, homework_name + '_Corriges.pdf')
    merger.write(merged_pdf_path)
    merger.close()

if __name__ == '__main__':
    main()
