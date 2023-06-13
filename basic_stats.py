import functions
import numpy as np

file = ["./new_data/joined_bib_FINAL.txt"]
n_authors, years, types, tc, nr = functions.join_bibdata_wos_format(2, file)

## Number of Authors
total = 0
for authors in n_authors:
    total += authors
print(total)
print(functions.calculate_mean(n_authors))
years_new = functions.to_number(years)
tc_new  = functions.to_number(tc)
nr_new  = functions.to_number(nr)
## Number of years
beg_y = max(years_new)
print(beg_y)

print(functions.calculate_mean(years_new))
print(functions.calculate_mean(tc_new))
total = 0
for item in nr_new:
    total += item
print(total)
# types, total citations, number of references