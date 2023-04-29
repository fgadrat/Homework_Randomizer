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
    
    # Récupérer le chemin absolu du fichier .tex.
    abs_tex_output_path = os.path.abspath(tex_output_path)

    # Compile le fichier .tex
    subprocess.run(["pdflatex", "-quiet", "-interaction=nonstopmode", abs_tex_output_path], cwd=os.path.dirname(tex_output_path))
    
    # Nettoie les fichiers temporaires. Commentez ces deux lignes peut aider au débogage.
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
        # Génération des valeurs aléatoires pour chaque élève, placées dans une liste 'v'. Bon d'accord on a rarement besoin de 100 valeurs.
        v = [random.randint(1, 10) for _ in range(100)]

        # Ajout du nom de l'élève en première position de la liste 'v'.
        v[0]=student
                
        # Personnalisation des valeurs spécifiques pour le devoir et le corrigé selon les besoins.
        #......
        
        while True: #Création des points pour former le rectangle tel que u.v=6*4-2*12=0
            a, b = random.sample([4, 6], 2)
            c, d = random.sample([2, 12], 2)
            #6*4+2*12 fait 48 pas 0, il faut avoir une ou trois coordonnées négatives.
            signe = [1, 1, 1, -1] if random.random() < 0.5 else [-1, -1, -1, 1]
            random.shuffle(signe)
            a, b, c, d = [a * signe[0], b * signe[1], c * signe[2], d * signe[3]]
            xA, yA = random.randint(-8, 8), random.randint(-8, 8)
            xB, yB = xA + a, yA + c #B=A+u
            xC, yC = xA + b, yA + d #C=A+v
            xM, yM = xA + (a + b) // 2, yA + (c + d) // 2
            xD, yD = xA + a+b, yA + c+d
            #Symétrie du rectangle pour avoir plus de possibilités.
            if random.random()<0.5:
                xA, yA, xB, yB, xC, yC, xD, yD, xM, yM = yA, xA, yB, xB, yC, xC, yD, xD, yM, xM
            #Je veux que toutes mes coordonnées soient entre -8 et 8 pour que ça tienne dans mon graphique.
            if all(-8 <= coord <= 8 for coord in [xA, yA, xB, yB, xC, yC, xD, yD]):
                break
        #On place les valeurs du problèmes dans les variables v[k] qui vont servir au remplacement.
        v[1:11] = xA, yA, xB, yB, xC, yC, xD, yD, xM, yM
        #Longueur MA
        v[21]=xA-xM
        v[22]=yA-yM
        v[23]=v[21]**2
        v[24]=v[22]**2
        #Longueur MB
        v[25]=xB-xM
        v[26]=yB-yM
        v[27]=v[25]**2
        v[28]=v[26]**2
        #Longueur MC
        v[29]=xC-xM
        v[30]=yC-yM
        v[31]=v[29]**2
        v[32]=v[30]**2
        
        v[33]=xC-xA
        v[34]=yC-yA
        
        #Ex2 Q1: Je veux une soustration de la forme d/(bc)-e/(ac) à mettre au même dénominateur. Le ppc est abc, au lieu d'être le produit des dénominateurs.
        primes = [2,3,5,7]
        primes_temp=primes
        
        a, b = random.sample(primes_temp, 2)
        primes_temp = [k for k in primes_temp if k not in [a, b]]
        primes.extend([11, 13])
        
        d, e = random.sample(primes_temp, 2)
        
        c=4
        while math.gcd(c,d)!=1 or math.gcd(c,e)!=1:
            c=random.randint(3,6)
        v[11:15]=d, b*c, e, a*c
        
        v[35:40]=a, b, d*a, a*b*c, e*b
        v[40]=v[37]-v[39]
        #On simplifie cette fraction si elle est simplifiable
        v[41]=''
        r=math.gcd(v[40],v[38])
        if r!=1:
            num=v[40]//r
            den=v[38]//r
            if den==1:
                v[41]+=f'={num}'
            else:
                v[41]+=f'=\\frac{{{num}}}{{{den}}}'
                
        #Q2a
        v[42]=2*v[15]
        v[43]=v[15]**2
        #Q2b
        v[16]=random.randint(1,5)
        v[44]=2*v[16]
        v[45]=v[44]+1
        #Q3a
        a=random.randint(1,7)
        b=random.randint(1,7)
        if a==b:
            b+=1
        if a==1:
            v[17]=''
        else:
            v[17]=a**2
        v[18]=2*a*b
        v[19]=b**2
        
        v[46]=a
        v[47]=b
        
        
        
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
    for student in students: #Itérer sur la liste d'élèves assure que les devoirs dans le pdf fusionné seront dans le même ordre que dans la liste.
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
