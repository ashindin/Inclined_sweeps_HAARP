#!/bin/bash

wget -i raw_data_archive.urls
sed 's/\r$//' checksums.sha | sed 's/\r/\n'/ | sha1sum -c
wvunpack -r *.wv
7z -y x "*.7z"
octave-cli extract_spew.m
python get_spectrograms_A.py
python get_spectrograms_B.py
python get_spectrograms_C.py
python concat_spectrograms.py
python inline_sweeps.py
python fill_database.py
python dm_proc.py
python bum_proc.py
python figure1.py
python figure2.py
python figure3.py

