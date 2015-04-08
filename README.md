# mdts2-ts

Pre-requisities:
- nose
- testtools

$ pip install nose testtools

To run the TS unit tests:

$ nosetests -c etc/mdts-unit.conf

To run the functional MDTS tests:

$ nosetests

Both commands will report:
- an xml of the results at logs/mdts-output.xml
- a log file with the logging information from tests at logs/mdts-output.log
