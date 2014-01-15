dist-zip: elevation.zip

elevation.zip: *.py
	-rm elevation.zip
	find . -name "*~" -exec rm {} \;
	find . -name "*.bak" -exec rm {} \;
	cd ..;zip elevation/elevation.zip elevation/*.py elevation/*.png \
	elevation/AUTHORS elevation/LICENSE elevation/metadata.txt \
	elevation/Makefile elevation/README.md elevation/TODO

clean:
	-rm elevation.zip
