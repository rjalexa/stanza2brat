# stanza2brat
 A simple program showing how to generate files from Stanford's STANZA NLP library to BRAT Standoff format

env.yml has the very simple prerequisite libraries to be installed.
This was developed on an Apple M1 desktop so your mileage will vary

Currently the text to be analysed is simply a constant you can change in the code file.

Please use the right language code by changing the corresponding constant. Currently it's
set to 'it' for Italian but you can use any other language code such as 'en' for other
STANZA supported languages.

Once the files have been generated they need to be manually moved to your working
BRAT directory in a dedicated directory under the data directory. Also take care of
changing the ownership of the files to one readable and writable to the BRAT webserver.

Enjoy
