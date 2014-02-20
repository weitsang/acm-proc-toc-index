import sys
from titlecase import titlecase

# An incrementing counter for the order of a paper.
order = 1

# An incrementing counter for the page number of a paper.
# EDIT this if the paper does not start at Page 1.
page = 1

# List of all papers
papers = {}

# List of all papers authored by an author.  
# The key is last name + " " + first name.
papers_by = {}

# Affiliation of an author.
# The key is last name + " " + first name.
affiliation_of = {}

class Paper:
	pass

def last_name_of(author):
# assume author is a string consisting of first name, last name, 
# and affiliation, separated by commas.
	fields = author.split(',')
	return fields[1].strip()

def first_name_of(author):
# assume author is a string consisting of first name, last name, 
# and affiliation, separated by commas.
	fields = author.split(',')
	return fields[0].strip()

def format_author(author):
# assume author is a string consisting of first name, last name, 
# and affiliation, separated by commas.
	fields = author.split(',')
	return "%s %s, %s.\\\\" % (fields[0].strip(), fields[1].strip(), fields[2].strip())

def format_title(title, page):
# assume author is a string consisting of first name, last name, 
# and affiliation, separated by commas.
	return "\\vspace{2mm}\\textsf{\\textbf{%s} (Page %d)}\\\\" % (title, page)

def format_index_author(author, affiliation):
# assume author is a string consisting of first name, last name, 
# and affiliation, separated by commas.
	fields = author.split(',')
	return "\\textsf{%s %s, %s}\\\\" % (fields[1].strip(), fields[0].strip(), affiliation)

def format_index_title(title, page, count, num_of_papers):
# assume author is a string consisting of first name, last name, 
# and affiliation, separated by commas.
	if num_of_papers != count:
		return "\\hspace*{5mm}{\\fnote\\textrm{%s} (Page %d)}\\\\" % (title, page)
	else:
		return "\\vspace*{4mm}\n\\hspace*{4mm}{\\fnote\\textrm{%s} (Page %d)}\\\\" % (title, page)

def get_index_letter(author):
	fields = author.split(',')
	if fields[0][0] != '\\':
		return fields[0][0].upper()
	else:
		# special european characters, assume to be in the format of \x{y}
		return fields[0][0:4];

def format_index_letter(c):
	return "{\\large {\\bf %s}}\\\\*[3mm]" % c

# Read from input file and parse everything into
# a list of papers
f = open(sys.argv[1], 'r')
line = f.readline()
while line:
# A line with a single number indicates the beginning of 
# a "paper block".  The number indicates the number of pages 
# in the paper.
	fields = line.split()
	if line.strip() == "" or len(fields) > 1 or not fields[0].isdigit():
		# Ignore junk or blank lines
		line = f.readline()
		continue

	# line contains only one item and consists only of digits.
	# This mark the beginning of a paper block.
	p = Paper()
	num_of_pages = int(fields[0])
	p.starting_page_number = page 
	page += num_of_pages

	papers[order] = p
	p.order = order
	order += 1

	# Next line is supposed to be the title
	p.title = titlecase(f.readline().strip())
	p.authors = []

	# Next line is supposed to be the first author.
	line = f.readline()
	while line:
		if line.strip() == "":
			break

		# assume author is a string consisting of first name, last name, 
		# and affiliation, separated by commas.
		try:
			fields = line.split(',', 2)
			first = fields[0].strip()
			last = fields[1].strip()
			aff = fields[2].strip()
		except IndexError:
			print >> sys.stderr, "Each line should have three fields separated by commands: first name, last name, and affiliation."
			print >> sys.stderr, "The following line does not:\n"
			print >> sys.stderr, line
			sys.exit(0)
			

		p.authors.append(line)

		# Build the key.  We need this since we are going to sort
		# by last name followed by first name.
		key = last + "," + first
		if key not in papers_by:
			papers_by[key] = []
		papers_by[key].append(p)
		affiliation_of[key] = aff

		line = f.readline()

# Print the list of papers according to page numbers
# Biuld the author index in the process.
for key in sorted(papers.iterkeys()):
	p = papers[key]
	print format_title(p.title, p.starting_page_number)
	for author in p.authors:
		print format_author(author)
	print "\n"

# Print the index of authors according to last name
print "\\newpage"
print "\\textsf{\\Huge{Author Index}}\n"
print "\\vspace{8mm}"

# We print the prefix alphabet of the last name.
old_alphabet = '@' # the ascii character before 'A'
for key in sorted(papers_by.iterkeys()):
	c = get_index_letter(key)
	if c > old_alphabet:
		print format_index_letter(c)
		old_alphabet = c
	print format_index_author(key, affiliation_of[key])
	num_of_papers = len(papers_by[key])
	count = 1
	for p in papers_by[key]:
		print format_index_title(p.title, p.starting_page_number, count, num_of_papers)
		count += 1
