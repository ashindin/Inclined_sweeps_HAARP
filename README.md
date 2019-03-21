# Inclined_sweeps_HAARP
## Get source data
### Zenodo record
Shindin, Alexey. (2019). Properties of Stimulated Electromagnetic Emissions during Inclined HF Pumping of the Ionosphere near the 4th Electron Gyroharmonic at HAARP - data set (Version 1.0.0) [Data set]. Zenodo. [http://doi.org/10.5281/zenodo.2600237](http://doi.org/10.5281/zenodo.2600237)  

File "raw_data_archive.urls" contains all urls for the data set above.

### Download the data
i.e. using wget:
```bash
wget -i raw_data_archive.urls
```
### Check the data 
In Linux:
```bash
sed 's/\r$//' checksums.sha | sed 's/\r/\n'/ | sha1sum -c
```
In Windows one can use [Double commander](https://doublecmd.sourceforge.io/) to do this.

### Unpack the data
Third-party software needed: [7zip](https://www.7-zip.org/) for '\*.7z' files, [wavpack](http://www.wavpack.com/) for '\*.wv' files.  
```bash
wvunpack -r *.wv
7z -y x "*.7z"
```
## Reproducing the figures
### Setup environment
All code tested with Anaconda 2018.12 python distribution:  
* Python 3.7.1
* numpy-1.15.4
* pandas-0.23.4
* matplotlib-3.0.2
* scipy-1.1.0  

To extract RF data from '\*.DRXS12' files [GNU Octave](https://www.gnu.org/software/octave/) (or Matlab) is requied. Octave code tested with GNU Octave 5.1.0.
### Extract RF Data from '\*.DRXS12'
```bash
octave-cli extract_spew.m
```
### Figure 1
```bash
python3 figure1.py
```
