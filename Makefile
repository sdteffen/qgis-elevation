dist-zip: elevation.zip

elevation.zip: *.py
	cd ..;zip elevation/elevation.zip elevation/*.py elevation/*.png \
	elevation/AUTHORS elevation/LICENSE elevation/metadata.txt \
	elevation/Makefile elevation/README.md elevation/TODO
