Files in this Google Drive folder:

* arxiv-metadata-2020-no-description.csv
* arxiv-metadata-2020-full.csv
* oai:arXiv.org:2001.11818.oai\_dc.xml
* biorxiv-2020-no-description.csv
* biorxiv-2020-full.csv
* medrxiv-biorxiv-covid-papers.csv

## arxiv-metadata- files:

I gathered them using the Python project [oaiharvest](https://pypi.org/project/oaiharvest/) with the command

```
oai-harvest -f 2020-01-01 http://export.arxiv.org/oai2
```

This gives me all of the metadata files in arxiv that have been _updated_ on/after January 1st, 2020. This includes new submissions, but also includes random old stuff that arxiv internally "updated" for no discernable reason.

`oai-harvest` creates an XML file for each arxiv metadata file. I included one of them as an example: oai:arXiv.org:2001.11818.oai_dc.xml.

(a) The arxiv dates are based on first submission, so we do not need to worry about revisions. There are at least a dozen examples of papers that were re-submitted rather than revised -- you can find them by searching for duplicate titles. There are few enough of these, and even fewer straddle the boundary between 2020 and other years, so I ignored them. But for completeness's sake, let me describe two reasons why this might happen:

Reason 1: Accident

* https://arxiv.org/abs/1911.10425 This was submitted in 2019, and revised multiple times, including in 2020 most recently. The "date" in the dataset is correctly identified as 2019 and so this is filtered out from the CSV in the Google Drive.
* https://arxiv.org/abs/2004.06213 This was accidentally submitted as a new manuscript, instead of a revision to the above, in 2020. Thus the date is in 2020, and it is in the dataset.

Reason 2: Adding an author, or other significant revision

* https://arxiv.org/abs/1906.05827 submitted in 2019 (hence filtered out from our data)
* https://arxiv.org/abs/2002.09277 deliberately re-submitted in 2020, with new sections and new co-author (hence included)

(b) I only kept files with a `dc:date` tag in 2020.

(c) I wrote two files: -no-description.csv omits the `dc:description` (abstract) field, and `-full.csv` includes it.

(d) I checked for several people -- Dan, Aaron, and a math professor, and they all appeared at least as many times as I expected. Perhaps worth making sure with more scrutiny that ALL the 2020 arxiv submissions are here.

## biorxiv metadata files:

I gathered them by iterating over the API, ie, increasing the last number in this URL by increments of 100: https://api.biorxiv.org/details/biorxiv/2020-01-01/2020-04-25/0

**Important**: unlike the arxiv, the date for biorxiv is based on the _latest revision_. See, eg, this paper (https://www.biorxiv.org/content/10.1101/552125v5.article-info), which shows up as the third result in the API call above. The date is listed as Jan 1st, 2020, which is its latest update, but was submitted in 2019.

Fortunately, the version count of each preprint is given in the column `version`. **I recommend filtering the data to `version == 1`**.

Just as with the arxiv data, `-no-description.csv` does not contain abstract (here I also filtered out title); `-full.csv` does.


## medrxiv-biorxiv-covid-papers.csv

This one is just a scrape of the JSON feed at the bottom of [medrxiv's page on COVID preprints](https://connect.medrxiv.org/relate/content/181). It should include all of the files as of today.

## Remaining medrxiv papers

I tried to download a similar JSON for non-COVID medrxiv papers, but couldn't find a similar feed. I tried messing with the URL and replacing the "181" with other numbers but didn't get usable data.

There appears to be a daily scrape of abstracts on medrxiv going back to 2019 [here](https://github.com/mcguinlu/autosynthesis/blob/master/data/medRxiv_abstract_list.csv) (maintained by the author of the [medrxivR project](https://github.com/mcguinlu/medrxivr/), but it does not include first names, and only includes last name of first author.

## Source code

I have code for parsing the output of `oai-harvest`, and for restructuring the json from medrxiv, and I am happy to share/put on github. 
