After logging into the server with username & password

1. Install nltk by running following command:
  pip install nltk --user

  NLTK will be successfully installed

2. Under {csgrads1:~} type python
   After entering into python interpretor enter:
   >>> import nltk
   >>> nltk.download('punkt')

   >>> import nltk
   >>> nltk.download('stopwords')

   >>> import nltk
   >>> nltk.download('wordnet')

   >>> import nltk
   >>> nltk.download('averaged_perceptron_tagger')

3. Exit the python interpretor by pressing 'Ctrl + D'

4. Under {csgrads1:~} type the following:
   python assignment3.py '/people/cs/s/sanda/cs6322/Cranfield/' '/people/cs/s/sanda/cs6322/hw3.queries'

   Note: assignment3.py is the python file containing source code
	'/people/cs/s/sanda/cs6322/Cranfield/' is the first argument which is containing the cranfield location
	'/people/cs/s/sanda/cs6322/hw3.queries' is the second argument which is containing the queries