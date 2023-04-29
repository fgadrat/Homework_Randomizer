Homework Assignment Randomizer

## Overview
This script is designed to create personalized homework assignments and their solutions for students. It reads a list of student names from a CSV file, generates random values for each student to replace elements on the specified LaTeX templates, and then outputs the homework assignments and solutions as PDFs. The script also merges all the individual PDFs into two single PDFs, one containing all the assignments and the other containing all the solutions.

## Prerequisites
Before using this script, ensure that you have the following software installed on your computer:

1. Python 3
2. LaTeX distribution (e.g., TeX Live, MikTeX)
3. Python packages:
   - pandas
   - pypdf

You can install the required Python packages using pip:

```
pip install pandas pypdf
```

## Input Files
1. `eleves.csv`: A CSV file containing the list of students in the class. The student names should be in the format "LASTNAME Firstname" and located in the first column, starting from the third row.
2. `template.tex`: A LaTeX template for the homework assignment. Replaceable variables should be formatted as `{v1}`, `{v2}`, etc. as well as a `{student_name}` variable.
3. `template_c.tex`: A LaTeX template for the homework solutions. Replaceable variables should be formatted as `{v1}`, `{v2}`, etc.

## Usage
1. Place the script, CSV file, and LaTeX templates in the same folder.
2. Run the script.
3. Enter the name of the homework assignment when prompted. This name will be used as a prefix for the generated PDFs and subdirectories.
4. The script will generate personalized homework assignments and solutions for each student, and save them as PDFs in separate subdirectories named after the homework assignment (e.g., "Homework_1" and "Homework_1_Corrige").
5. The script will also merge all the individual PDFs into two single PDFs, one containing all the assignments (e.g., "Homework_1.pdf") and the other containing all the solutions (e.g., "Homework_1_Corriges.pdf").

## Preparing the LaTeX Templates

In order to use the script, you need to prepare two LaTeX templates: one for the homework assignment (`template.tex`) and one for the solutions (`template_c.tex`). Assuming you already have LaTeX assignments and solutions, follow these steps to modify your existing documents for use with the script:

### Step 1: Identify variables to randomize
Determine which elements in your assignment and solution documents you want to randomize for each student. These elements can include numeric values, coefficients, or any other variables that can be customized.

### Step 2: Replace variables with placeholders
For each variable you want to randomize, replace it with a placeholder in the format `{vN}`, where `N` is an integer value. Start with `{v1}` and increment the integer for each new variable.

For example, if you have an equation like this:

```
x + 3 = 5
```

Replace the coefficients and constants with placeholders:

```
x + {v1} = {v2}
```

Make sure to replace the variables in both the assignment and solution templates.

### Step 3: Adjust problem-solving algorithms in the script
In the `homework_generator.py` script, locate the `main()` function and the comment `# Personnalisation des valeurs spécifiques pour le devoir et le corrigé selon les besoins.`. This is where the script generates random values for the variables used in the LaTeX templates.

Customize this section of the code to generate random values for each placeholder you added to the templates. The script should assign the generated values to the corresponding elements in the `v` list. The first element of the list `v[0]` is reserved for the student name, so you should start adding your values from `v[1]`.

For example, if you have two placeholders `{v1}` and `{v2}` in your templates, you could generate random values like this:

```
v[1] = random.randint(1, 5)
v[2] = random.randint(4, 10)
```

Note: It's not just numerical values that can be replaced. Text and LaTeX formatting is also modifiable.
For example, if you have a fraction une your template_c:
```
$A = \frac{{v1}}{{v2}}$
```
Let's say you want the solution to also give the simplified expression if the fraction can be simplified. You can change your LaTeX template like this:
```
$A = \frac{{v1}}{{v2}}{v3}$
```
And in your Python code, you'll add:
```
v[3]=''
r=math.gcd(v[1],v[2])
if r==1:
	num=v[1]//r
	den=v[2]//r
	if den==1:
		v[3]=f'={num}'
	else:
		v[3]=f'=\\frac{{num}}{{den)}}
```
It's also possible to make personalized graphics with LaTeX by changing the drawing parameters.

## Customization
Modify the `read_students` function if your student list is not in the same format.

## Troubleshooting
If you encounter issues while using the script, check the following:

1. Ensure that the required software and Python packages are installed.
2. Verify that the CSV file and LaTeX templates are formatted correctly and placed in the same folder as the script.
3. Check the command prompt for error messages or warnings that may provide more information about the issue.
4. Commentez the lines:
```
	for ext in [".aux", ".log", ".tex"]:
		os.remove(output_path + ext)
```
In the generate_pdf function to keep the pdf generation files.