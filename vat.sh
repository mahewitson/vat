#!/bin/bash
for i in `find / -name *.html`
do
        python3 vat.py $i
done
