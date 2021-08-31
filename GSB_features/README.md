# GSB features for phishing Detection [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

> All features was obtained from [Chromium](https://github.com/chromium/chromium/tree/d7da0240cae77824d1eda25745c4022757499131/components/safe_browsing/content/renderer/phishing_classifier) Github repository.

# Environment setup

Setting up docker image frpm dockerfile:

```console
$ docker build -t chromium/features .
```

Running the docker image inside GPU (It is not used for feature extraction, but will be useful later). The code for feature extraction was parallelized on CPU.

```console
nvidia-docker run --tty --interactive --userns=host --volume /home/:/home/usr/work --name features_extractor chromium/features /bin/bash
```

Inside container, run:

```python
python .\generate_feature_vector.py -i '..\dataset\dataset.csv' -o '..\dataset\output_file.csv'
```

Make sure the input `.csv` has the columns `url` and `label`. Otherwise, an error will occur.

## Features from URL

There are three levels of features we can extract from the URL. The first one refers to the host features, the second one comes from the aggregated features, the final one consists of features from the URL path.
The details of each feature category is described bellow.

### Host features

-  `kUrlHostIsIpAddress`: Set if the URL's hostname is an IP address.

-  `kUrlTldToken`: Token feature containing the portion of the hostname controlled by a registrar, for example "com" or "co.uk".

-  `kUrlDomainToken`: Token feature containing the first host component below the registrar. For example, in "www.google.com", the domain would be "google".

-  `kUrlOtherHostToken`: Token feature containing each host component below the domain. For example, in "www.host.example.com", both "www" and "host" would be "other host tokens".

### Aggregated features

-  `kUrlNumOtherHostTokensGTOne`: Set if the number of "other" host tokens for a URL is greater than one. Longer hostnames, regardless of the specific tokens, can be a signal that the URL is phishy.

-  `kUrlNumOtherHostTokensGTThree`: Set if the number of "other" host tokens for a URL is greater than three.

### URL path features

-  `kUrlPathToken`: Token feature containing each alphanumeric string in the path that is at least 3 characters long.  For example, "/abc/d/efg" would have 2 path token features, "abc" and "efg".  Query parameters are not included.

## DOM HTML features

Besides features from URL, the DOM HTML has also strong features to be explored. These features are classified into four classes, (1) form related (2) Link (3) HTMP script and (4) general ones.

### Form Features

-  `kPageHasForms`: Set if the page has any `<form>` elements.

-  `kPageActionOtherDomainFreq`: The fraction of form elements whose |action| attribute points to a URL on a different domain from the document URL.

-  `kPageActionURL`: Token feature containing each URL that an |action| attribute points to.

-  `kPageHasTextInputs`: Set if the page has any `<input type="text">` elements (includes inputs with missing or unknown types).

-  `kPageHasPswdInputs`: Set if the page has any `<input type="password">` elements.

-  `kPageHasRadioInputs`: Set if the page has any `<input type="radio">` elements.

-  `kPageHasCheckInputs`: Set if the page has any `<input type="checkbox">` elements.

### Link features

-  `kPageExternalLinksFreq`: The fraction of links in the page which point to a domain other than the domain of the document.  See "URL host features" above for a discussion of how the doamin is computed.

-  `kPageLinkDomain`: Token feature containing each external domain that is linked to.

-  `kPageSecureLinksFreq`: Fraction of links in the page that use https.

### HTML script features

-  `kPageNumScriptTagsGTOne`: Set if the number of `<script>` elements in the page is greater than 1.

-  `kPageNumScriptTagsGTSix`: Set if the number of `<script>` elements in the page is greater than 6.

### Others features

-  `kPageImgOtherDomainFreq`: The fraction of images whose src attribute points to an external domain.


# Contributing

If you find any error, or ways to improve performance, open an issue or a new pull request.