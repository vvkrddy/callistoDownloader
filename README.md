# callistoDownloader

A python package for downloading spectrograms sourced from the [e-Callisto](http://www.e-callisto.org), which is an international network of solar radio spectrometers.

This package allows for bulk downloads of spectrograms for a given set of days in a given month and year, for a list of given instruments (visit [link](http://soleil.i4ds.ch/solarradio/data/readme.txt) for a list of all instruments from which the data is sourced).

The downloads are structured within a <code>e-Callisto</code> directory inside the working directory. The same is illustrated below:


```
working directory/
└───e-Callisto/
    └───yyyy/
        └───mm/
            └───dd/
                └───file1..
                    file2..
```

## Documentation
Soon!
## Functions of this package:
`which_years()`
<br>Prints all those years for which any spectrograms are available

`which_months(select_year)`
<br>Prints all those months of a given year for which spectrograms are available

`which_days(select_year, select_month)`
<br>Prints all those days of a given year and month for which spectrograms are available

`download(select_year, select_month, select_days, instruments)`
<br>Downloads the spectrograms for given list of days of a given year and month; for given list of instruments

