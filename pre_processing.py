import pandas as pd
import numpy as np
from typing import Union, List

SHORTENERS = ['bit', 'tinyurl', 'is', 's', 'gg']

def solve_data_inconsistencies(dataset:pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame:

    inconsistency = data[~data.parseurl_domain.isin(SHORTENERS)].groupby(['parseurl_domain', 'phishing_numeric']).url.count().reset_index()
    '''
    This piece of code results in a dataframe like this:
    +-------+---------------------------------------------+
    | index | parseurl_domain | phishing_numeric |  url   |
    +-------+---------------------------------------------+
    |   0   |        ,        |        0         |   2    |
    |   1   | ,0800-880-1818  |        0         |   1    |
    |  141  |       0i        |        0         |   16   |
    |  142  |      0link      |        0         |   46   |
    |  144  |       0pt       |        0         |   7    |
    |  145  |      0snd       |        0         |  838   |

    Grouped by parseurl_domain and phishing_numeric, it means that every
    parseurl_domain has two lines if the phishing_numeric is inconsistent.
    '''
    inconsistency = inconsistency.set_index('parseurl_domain').pivot(columns = 'phishing_numeric').dropna()

    '''
    Here we filter by the ones who has two different labels, resultin in something like this:
    +----------------------------+--------------------+-----------+
    |  parseurl_domain  | phishing_numeric O | phishing_numeric 1 |
    +----------------------------+--------------------+-----------+
    |      106apple     |        1.0         |        1.0         |
    | a-icloud-ifind-my |        5.0         |        1.0         |

    Then set all inconsistency as phishing
    '''
    dataset.phishing_numeric[dataset.parseurl_domain.isin(inconsistency.index)] = 1

    return dataset
