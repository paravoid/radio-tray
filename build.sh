#!/bin/sh

rm -rf dist/*
python setup.py sdist
python setup.py bdist

dpkg-buildpackage -b -rfakeroot
mv ../radiotray_0.7.2_{all.deb,*.changes} dist

