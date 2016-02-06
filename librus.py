from bs4 import BeautifulSoup


class GradeBook:
	"""GradeBook - Stores grades. Allows sorting and displaying all at once.

	Variables:
	grades (list) - The list of grades.
	subjects (list) - The list of school subjects.
	teachers (dictionary) - A dictionary of teachers. {subject:teacher}
	subject_grades (dictionary) - A list of grades per subject. {subject:[grades]}
	midterm_grades (dictionary) - A list of midterm grades per subject. {subject:[grades]}
	
	Functions:
	add(grade) - Add a grade into the GradeBook.
	display() - Return the grades from the GradeBook, allowing to display them.
	sort_by_weight(reverse=False) - Sort the grades by their weight.
	sort_by_date(reverse=False) - Sort the grades by their date.
	sort_by_grade(reverse=False) - Sort the grades by their value.
	calculate_average(subject) - Calculates average of a specified subject, taking weights in account.
	"""

	def __init__(self):
		"""Initializes the GradeBook by initializing variables."""
		self.grades = []
		self.subjects = []
		self.teachers = {}
		self.subject_grades = {}
		self.midterm_grades = {}

	def add(self, grade):
		"""Add a grade into the GradeBook.

		Parameters:
		grade - a Grade() object.
		"""
		self.grades.append(grade)
		if grade[3] not in self.subjects: # grade[3] is the school subject
			self.subjects.append(grade[3])
			self.subject_grades[grade[3]] = []
			self.midterm_grades[grade[3]] = []

		if grade[9] not in self.teachers:
			self.teachers[grade[3]] = grade[9] # {subject:teacher}

		if grade[1] == 1: # If grade numtype equals MidtermGrade
			if "śródroczna" in grade[7]: # If śródroczna is in description
				self.midterm_grades[grade[3]].append(grade)

		self.subject_grades[grade[3]].append(grade)

	def display(self):
		"""Return the grades from the GradeBook, allowing to display them."""
		display_text = ""
		for grade in self.grades:
			display_text += grade.display()
		return display_text

	def sort_by_weight(self, reverse=False):
		"""Sort the grades by their weight.

		Keyword arguments:
		reverse (bool) - whether to reverse the list or not. (default False)
		"""
		self.grades.sort(key=lambda x: int(x[8]), reverse=reverse)

	def sort_by_date(self, reverse=False):
		"""Sort the grades by their date.

		Keyword arguments:
		reverse (bool) - whether to reverse the list or not. (default False)
		"""
		self.grades.sort(key=lambda x: str(x[5]), reverse=reverse)

	def sort_by_grade(self, reverse=False):
		"""Sort the grades by their value.

		Keyword arguments:
		reverse (bool) - whether to reverse the list or not. (default False)
		"""
		self.grades.sort(key=lambda x: int(x[13]), reverse=reverse)

	def calculate_average(self, subject):
		"""Calculates an average of a specified subject, taking weights in account.

		Arguments:
		subject (string) - The mentioned subject."""
		if subject not in self.subjects:
			raise NameError('Subject not found - '+subject+'. Use ones specified in GradeBook.subjects next time.')

		temp_grades = []
		temp_sum = 0
		temp_count = 0
		for x in self.subject_grades[subject]:
			if x.absolute_value and (x.calculate_towards_avg_grade == 1): # doesnt equal 0 and counts towards average
				temp_grades.append(x)

		for x in temp_grades:
			temp_sum += x.absolute_value * x.weight
			temp_count += x.weight

		return float(temp_sum/temp_count)

class Grade:
	"""Grade - A grade object. Stores all of values, allows displaying it on a function call.

	Variables:
	values (list) - Provided by Parser class, a list of values:
		[0] - grade_id
		[1] - grade_numtype
		[2] - grade_type
		[3] - school_subject
		[4] - grade_value
		[5] - date
		[6] - day_of_the_week
		[7] - category
		[8] - weight
		[9] - teacher
		[10] - calculate_towards_avg_grade
		[11] - added
		[12] - description
		Added upon initialization to the list:
		[13] - absolute_value	
	grade_numtype (int) - Type of the grade:
		0 - DescriptiveGrade - Doesn't have weight (-1) and doesn't specify calculating towards avg grade (-1). Sometimes has a description.
		1 - MidtermGrade - Doesn't have weight (-1), doesn't calculate towards avg grade. (0)
		2 - StandardGrade - Has weight and can calculate towards average grade. (doesn't have to)
		3 - ShapingGrade - Doesn't have weight and doesn't specify calculating towards avg grade, always has a description.
	grade_id (int) - ID of grade in Librus.
	grade_type (string) - Type of the grade, corresponds to grade_numtype.
	grade_value (string) - The grade itself.
	absolute_value (int) - A numerical representation of the grade. (without the +/- at end and without T/np)
	school_subject (string) - School subject of the grade.
	date (string) - Date in which the grade was written. YYYY-MM-DD
	day_of_the_week (string) - Day of the week in which the grade was written. (pon./wt./śr./czw./pt.)
	category (string) - Type/category of the grade, for ex. exam/vocal exam.
	weight (int) - Weight of the grade. If no data specified, -1.
	teacher (string) - Teacher who teaches the subject.
	added (string) - Teacher who added the grade (usually the same as var teacher)
	calculate_towards_avg_grade (int) - Whether the grade calculates to average or not, 0/1. If no data specified, -1.
	description (string) - Description of the grade.

	Functions:
	__init__(values) - Accepts the values from Parser.parse_grade and puts them into array. Initializing method.
	update(values) - Updates the values with new ones. Done on initialization.
	display() - Returns a text representation of the grade, which can be used for display.
	set_absolute_values() - Turns the grade_value into absolute_value. Done on initialization.
	return_values() - Returns the internal list of values.
	"""

	def __init__(self, values):
		"""Initializes the Grade by initializing variables, updating them and creating a numeral representation of the grade.

		Parameters:
		values (list) - A list of values, provided by Parser.parse_grade.
		"""
		self.values = []
		self.grade_id = 0
		self.grade_numtype = 0
		self.grade_type = ""
		self.school_subject = ""
		self.grade_value = ""
		self.absolute_value = 0
		self.date = ""
		self.day_of_the_week = ""
		self.category = ""
		self.weight = 0 
		self.teacher = ""
		self.calculate_towards_avg_grade = 0 
		self.added = ""
		self.description = "" 

		self.update(values)
		self.set_absolute_values()
		self.values.append(self.absolute_value) # values[13]

	def __getitem__(self, index):
		"""Allows sorting with .sort()."""
		return self.values[index]

	def __str__(self):
		"""Allows printing the Grade without any issues."""
		return self.display()

	def update(self, values):
		"""Updates the variables in Grade class with ones provided in arguments. Called on initialization.

		Parameters:
		values (list) - A list of values, provided by Parser.parse_grade.
		"""
		self.values = values

		self.grade_id = int(values[0])
		self.grade_numtype = int(values[1])
		self.grade_type = values[2]
		self.school_subject = values[3]
		self.grade_value = values[4]
		self.date = values[5]
		self.day_of_the_week = values[6]
		self.category = values[7]
		self.weight = int(values[8])
		self.teacher = values[9]
		self.calculate_towards_avg_grade = int(values[10])
		self.added = values[11]
		self.description = values[12]
		#self.absolute_value = values[13]

	def display(self):
		"""Returns a text representation of the grade, which can be used for display."""
		display_string = "["
		display_string += self.date + ", " + self.day_of_the_week + "] - <" + self.school_subject + "> ("
		display_string += self.grade_value + ")"
		if self.weight != -1:
			display_string += " - Waga: " + str(self.weight)
		if self.calculate_towards_avg_grade != -1:
			display_string += ". Liczy się: "
			display_string += {0: "Nie", 1: "Tak"}[self.calculate_towards_avg_grade]
		display_string += ". Typ oceny: " + self.category
		display_string += ". Dodał/a " + self.teacher + ", id w Librusie: " + str(self.grade_id) + "."
		if self.description:
			display_string += " Opis: "+self.description
		display_string += "\n"
		return display_string

	def set_absolute_values(self):
		"""Turns the grade_value into absolute_value. Called on initialization"""
		if self.grade_value in ("-", "+", "T", "np"):
			self.absolute_value = 0
		else:
			if len(self.grade_value) > 1:
				if "+" == self.grade_value[1]:
					self.absolute_value = float(self.grade_value[0])
					self.absolute_value += 0.5
				elif "-" == self.grade_value[1]:
					self.absolute_value = float(self.grade_value[0])
					self.absolute_value -= 0.25
			else:
				self.absolute_value = int(self.grade_value)

	def return_values(self):
		"""Returns the internal list of values."""
		return self.values


class Parser:
	"""Parser - a parser object, used to parse HTML into variables.

	Functions:
	parse_grade(grade) - Parses BeautifulSoup grades provided by Parser.parse_html. Returns a list of values. 
	parse_html(html) - Parses HTML into BeautifulSoup grades.
	"""
	def __init__(self):
		pass

	def parse_grade(self, grade):
		"""parse_grade - Parses a grade object provided by BeautifulSoup [don't confuse with the class Grade]. Returns a list of values."""
		school_subject = repr(grade.findParents('tr')[0]).split('/tree_colapsed.png"/>')[1].split('<td>')[1].split('</td>')[0]
		grade_id = repr(grade).split("szczegoly/")[1].split('" title')[0]
		grade_value = str(grade.text)
		category = repr(grade).split("Kategoria: ")[1].split('&lt;')[0]
		date = repr(grade).split("Data: ")[1].split('&lt;')[0].split(' (')[0]
		day_of_the_week = repr(grade).split("Data: ")[1].split('&lt;')[0].split(' (')[1].split(')')[0]
		teacher = repr(grade).split('Nauczyciel: ')[1].split('&lt;')[0]
		added = repr(grade).split('Dodał: ')[1].split('&lt;')[0]

		try:
			calculate_towards_avg_grade = {'tak': True, 'nie': False}[repr(grade).split('średniej: ')[1].split('&lt;')[0]]
			has_average = True
		except:
			calculate_towards_avg_grade = -1
			has_average = False

		try:
			weight = repr(grade).split('Waga: ')[1].split('&lt;')[0]
			has_weight = True
		except:
			weight = -1
			has_weight = False
		
		if 'ksztaltujace' in grade_id:
			grade_id = grade_id.split('ksztaltujace/')[1]
			grade_type = "ShapingGrade"
			grade_numtype = 3
		else:
			grade_numtype = has_weight + has_average
			grade_type = {0: "DescriptiveGrade", 1: "MidtermGrade", 2: "StandardGrade"}[grade_numtype]

		try:
			description = repr(grade).split('Ocena: ')[1].split('&lt;')[0]
		except:
			description = ""

		return [grade_id, grade_numtype, grade_type, school_subject, grade_value, date, day_of_the_week, category,
		weight, teacher, calculate_towards_avg_grade, added, description]

	def parse_html(self, html):
		"""parse_html(html) - parses html and returns a list of soup grades (used in Parser.parse_grade)"""
		soup = BeautifulSoup(html, "html.parser")
		soupGrades = soup.findAll("a", {"class": "ocena"})
		return soupGrades

def read_file(name):
	"""read_file(name) - opens a file and returns its content."""
	tFile = open(name, "r", encoding="utf8")
	tContent = tFile.readlines()
	tFile.close()
	return "/n".join(tContent)

def save_file(name, content):
	"""save_file(name, content) - opens a file and writes into it."""
	tFile = open(name, "w", encoding="utf8")
	tFile.write(content)
	tFile.close()
	return True

objParser = Parser()
objDziennik = GradeBook()
html = read_file("main.html")
oceny = objParser.parse_html(html)
for i in range(len(oceny)):
	if i - 1: # first grade is no. 0, and doesnt parse due to librus being dumb and putting a >testgrade in html source
		objDziennik.add(Grade(objParser.parse_grade(oceny[i-1])))

objDziennik.sort_by_grade()
oceny_txt = objDziennik.display()
print(oceny_txt)

for przedmiot, ocena in objDziennik.midterm_grades.items():
	print(przedmiot)
	print(objDziennik.calculate_average(przedmiot))
	for i in ocena:
		print(i.display())
	#print(przedmiot)
	#print(ocena)

save_file("oceny.txt", oceny_txt)