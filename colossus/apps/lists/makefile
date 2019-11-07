TESTDIR = tests
PYLINT = flake8
PYLINTFLAGS =
PYTHONFILES = $(shell ls *.py)
TEST_FILES = $(shell ls $(TESTDIR)/test_*.py)
export user_type = test

FORCE:

prod: tests
	-git commit -a
	git push origin master

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

#pytests: $(PYTHONFILES)
#./pytests.sh

tests: lint

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

test_used_cars:
	nosetests tests.test_used_cars --nocapture

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm *.csv
	-rm $(TESTDIR)/*~


tests: FORCE