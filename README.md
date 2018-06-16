# UVA-Course-Evaluation

This project contains a single python file that defines a class for 
visualizing UVA course evaluations.  In order to use this file, you 
must have the pandas library, the matplotlib library, and the selenium 
library installed.  A chrome driver is used in this project, but you 
can obviously replace it with a driver of your choosing.  If you 
aren't familiar with the selenium library, you might want to google 
how to set it up, as it isn't as simple as doing a regular pip 
install.  This is an example of how I would use 
this project:

1) Create a config.py file as follows:
	username = your_computing_id
	password = your_uva_password

2) Go to Lou's list and find a course you are interested in seeing the 
reviews for.  Click on the name of the course (for example, Program and 
Data Representation).  In the class description, click the link that says 
"Student Evaluations."  Copy this link and put it in a python list.  
Repeat this for all of the classes you are interested in.

3) Create a ClassEvaluations object, using the python list containing your 
links as the parameter. You'll have to babysit it for the first 10 seconds 
or so, as you unfortunately have to DUO authenticate. From here, you can 
use the .show_plots() method or the .save_plots() method on your object.
