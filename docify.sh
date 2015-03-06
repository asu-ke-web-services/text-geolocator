fig run web sphinx-apidoc --force --separate --private -o "docs/source" "geolocator"
fig run web make clean -C docs/
fig run web make html -C docs/
