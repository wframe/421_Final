REQUIREMENTS:
	PYTHON 2.7
	PATTERN
		pip install pattern
	TEXTBLOB
		pip install textblob
	STANFORD PARSER
		-> download below and unpack into /src/scoring/stanford-parser/:
			https://drive.google.com/file/d/0B_EGNlVgIoFTZXdqaXMyZURkM3c/view?usp=sharing

		Update these values in /src/scoring/syntax.py:
			-> ROOT_DIR - point this the directory where you've downloaded this project
			-> JAVA_HOME - point this at the bin of your java installation. Make sure it's Java 8

		Note that this version of our project is glacially slow, mostly due to the stanford parser

EXECUTION:
	Run:
		python grader.py
	This will run the grader on all files inside the input/original directory