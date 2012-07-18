MAKEFLAGS += --no-print-directory

all:
	@(cd dist; python setup.py bdist_egg >/dev/null; mv dist/*.egg .; rm -fr dist build *.egg-info)
	@(echo "`ls dist/*.egg` -- is built")

clean:
	@rm -f *.pyc
	@rm -fr dist/build dist/dist dist/*.egg-info dist/*.egg

install:
	@(if [ "`ls dist/*.egg 2>/dev/null`" = "" ]; then make dist; fi)
	@(cd dist; easy_install `ls *.egg` >/dev/null)
	@(cd dist; echo "`ls *.egg` -- is installed")

uninstall:
	@(yes|pip uninstall pyHFS >/dev/null)
	@(cd dist; echo "`ls *.egg` -- is uninstalled")
