# Générateur de devoirs de maths avec valeurs aléatoires.

## Vue d'ensemble
Ce script est conçu pour créer des devoirs personnalisés et leurs corrigés. Il lit une liste de noms d'élèves à partir d'un fichier CSV, génère des valeurs aléatoires pour chaque élève à remplacer dans les template LaTeX spécifiés. Puis il génère les devoirs et les corrigés sous forme de PDF. Le script fusionne également tous les PDF individuels en deux PDF uniques pour imprimer facilement, l'un contenant tous les devoirs et l'autre contenant tous les corrigés.

## Prérequis
Avant d'utiliser ce script, assurez-vous d'avoir les logiciels suivants installés sur votre ordinateur :

1. Python 3
2. Distribution LaTeX (par exemple, TeX Live, MikTeX)
3. Packages Python :
   - pandas
   - pypdf

Vous pouvez installer les packages Python requis à l'aide de pip :

```
pip install pandas pypdf
```

## Fichiers en entrée
1. `eleves.csv`: Un fichier CSV contenant la liste des élèves de la classe. Les noms des élèves doivent être au format "NOM Prénom" et situés dans la première colonne, à partir de la troisième ligne. Format sous lequel nous le fourni pronote (vous risquez d'avoir un devoir au nom de "Moyenne").
2. `template.tex`: Un template LaTeX pour le devoir. Les variables remplaçables doivent être formatées comme `{v1}`, `{v2}`, etc. Ainsi qu'une variable `{student_name}`
3. `template_c.tex`: Un template LaTeX pour le corrigé du devoir. Les variables remplaçables doivent être formatées comme `{v1}`, `{v2}`, etc.

## Utilisation
1. Placez le script, le fichier CSV et les template LaTeX dans le même dossier.
2. Exécutez le script.
3. Entrez le nom du devoir lorsque vous y êtes invité. Ce nom sera utilisé comme préfixe pour les PDF générés et les sous-répertoires.
4. Le script générera des devoirs personnalisés et des corrigés pour chaque élève et les sauvegardera en tant que PDF dans des sous-répertoires distincts nommés d'après le devoir (par exemple, "Devoir_1" et "Devoir_1_Corrige").
5. Le script fusionnera également tous les PDF individuels en deux PDF uniques, l'un contenant tous les devoirs (par exemple, "Devoir_1.pdf") et l'autre contenant toutes les corrigés (par exemple, "Devoir_1_Corriges.pdf").

## Préparation des templates LaTeX

Pour utiliser le script, vous devez préparer deux templates LaTeX : un pour le devoir (`template.tex`) et un pour les corrigés (`template_c.tex`). Suivez ces étapes pour modifier vos documents existants pour les utiliser avec le script :

### Étape 1: Identifier les variables à randomiser
Déterminez quels éléments de vos documents de devoir et de corrigé vous souhaitez randomiser pour chaque élève. Ces éléments peuvent inclure des valeurs numériques, des coefficients ou toute autre variable pouvant être personnalisée.

### Étape 2: Remplacer les variables par des espaces réservés
Pour chaque variable que vous souhaitez randomiser, remplacez-la par un espace réservé au format `{vN}`, où `N` est une valeur entière. Commencez par `{v1}` et augmentez l'entier pour chaque nouvelle variable.

Par exemple, si vous avez une équation comme celle-ci :

```
x + 3 = 5
```

Remplacez les coefficients et les constantes par des espaces réservés :

```
x + {v1} = {v2}
```

Assurez-vous de remplacer les variables dans les templates de devoir et de corrigé.

### Étape 3: Ajustez les algorithmes de résolution de problèmes dans le script
Dans le script `homework_generator.py`, localisez la fonction `main()` et le commentaire `# Personnalisation des valeurs spécifiques pour le devoir et le corrigé selon les besoins.`. C'est ici que le script génère des valeurs aléatoires pour les variables utilisées dans les templates LaTeX.

Personnalisez cette section du code pour générer des valeurs aléatoires pour chaque espace réservé que vous avez ajouté aux templates. Le script doit attribuer les valeurs générées aux éléments correspondants de la liste `v`. Le premier élément de la liste `v[0]` est réservé au nom de l'élève, vous devez donc commencer à ajouter vos valeurs à partir de `v[1]`.

Par exemple, si vous avez deux espaces réservés `{v1}` et `{v2}` dans vos templates, vous pourriez générer des valeurs aléatoires comme ceci :

```
v[1] = random.randint(1, 5)
v[2] = random.randint(4, 10)
```

### Étape 4: Testez le script
Après avoir préparé vos templates LaTeX et ajusté le script, exécutez le script pour vérifier si tout fonctionne comme prévu. Vérifiez que les PDF générés contiennent les bonnes valeurs aléatoires pour chaque élève.

N'oubliez pas de conserver une sauvegarde de vos documents de devoir et de corrigé originaux avant d'effectuer des modifications, au cas où vous auriez besoin de revenir à la version d'origine.

Remarque: Il n'y a pas que les valeurs numériques qui peuvent être remplacées, du texte et formattage LaTeX sont modulable.
Par exemple si vous avez une fraction dans votre template:
```
$A = \frac{{v1}}{{v2}}$
```
Comme les variable sont aléatoires, si vous voulez simplifiez cette fraction uniquement lorsqu'elle n'est pas déjà irréductible vous pouvez faire ceci:
```
$A = \frac{{v1}}{{v2}}{v3}$
```
Et dans le code python vous aurez alors:
```
#Définition de v[1] et v[2] déjà faites
v[3]=''
r=math.gcd(v[1],v[2])
if r==1:
	num=v[1]//r
	den=v[2]//r
	if den==1:
		v[3]=f'={num}'  #Comme le dénominateur fait 1, on écrit $A = \frac{a}{b}=num$ dans le fichier .tex
	else:
		v[3]=f'=\\frac{{num}}{{den)}} #Ce qui écrit $A = \frac{a}{b}=\frac{num}{den}$ dans le fichier .tex
```

Il est possible aussi d'individualiser les graphiques 

## Personnalisation
Si vos listes d'élèves sont sous un autre format, vous pouvez ajuster la fonction `read_students`

## Dépannage
Si vous rencontrez des problèmes lors de l'utilisation du script, vérifiez les points suivants :

1. Assurez-vous que les logiciels requis et les packages Python sont installés.
2. Vérifiez que le fichier CSV et les templates LaTeX sont correctement formatés et placés dans le même dossier que le script.
3. Vérifiez le terminal pour les messages d'erreur ou les avertissements qui peuvent fournir plus d'informations sur le problème.
4. Commentez les lignes:
	```
		for ext in [".aux", ".log", ".tex"]:
			os.remove(output_path + ext)
	```
	Dans la fonction generate_pdf pour garder les fichiers de génération des pdf.
