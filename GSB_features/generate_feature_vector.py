from pandas.core.frame import DataFrame
from dom_feature_extractor import *
from url_feature_extractor import *

import numpy as np
import pandas as pd
import argparse
import requests
from bs4 import BeautifulSoup

import multiprocessing as mp


features_names = [
                    'kUrlHostIsIpAddress',
                    'kUrlNumOtherHostTokensGTOne',
                    'kUrlNumOtherHostTokensGTThree',
                    'kPageHasForms',
                    'kPageActionOtherDomainFreq',
                    'kPageHasTextInputs',
                    'kPageHasPswdInputs',
                    'kPageHasRadioInputs',
                    'kPageHasCheckInputs',
                    'kPageExternalLinksFreq',
                    'kPageSecureLinksFreq',
                    'kPageNumScriptTagsGTOne',
                    'kPageNumScriptTagsGTSix',
                    'label'
                ]
def main():

    pool = mp.Pool(processes=mp.cpu_count())

    args = command_line_parsing()

    dataset_path = args.url_dataset
    dataset = pd.read_csv(dataset_path, delimiter=';')

    sample_features = pool.map(extract_features, [(idx, row) for idx, row in dataset.iterrows()])

    features_extracted = DataFrame(sample_features, columns=features_names)

    features_extracted.to_csv(args.output_file, index=False)

def command_line_parsing():

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('--url-file', '-i', 
                        dest='url_dataset', 
                        required=True, 
                        help='Path to the URL file dataset.')

    parser.add_argument('--url-feature-extracted', '-o', 
                        dest='output_file', 
                        required=True, 
                        help='Path to csv file where the collected features will be stored.')

    return parser.parse_args()

def extract_features( args ):
   
    _, row = args
    
    features = []

    url = row.url
    label = row.label

    try:            
        page = requests.get(url)

    except:
        return [0] * 13 + [label]

    html = BeautifulSoup(page.content, 'html.parser')

    kUrlHostIsIpAddress = is_ip(url)
    features.append(kUrlHostIsIpAddress)
    # print(kUrlHostIsIpAddress)

    kUrlNumOtherHostTokensGTOne = other_tokens_greater_one(url)
    features.append(kUrlNumOtherHostTokensGTOne)
    # print(kUrlNumOtherHostTokensGTOne)

    kUrlNumOtherHostTokensGTThree = other_tokens_greater_three(url)
    features.append(kUrlNumOtherHostTokensGTThree)
    # print(kUrlNumOtherHostTokensGTThree)

    forms, kPageHasForms = has_forms(html)
    features.append(kPageHasForms)
    # print(kPageHasForms)

    kPageActionOtherDomainFreq = other_domain_ratio(url, forms)
    features.append(kPageActionOtherDomainFreq)
    # print(kPageActionOtherDomainFreq)

    _, kPageHasTextInputs = has_text_inputs(html)
    features.append(kPageHasTextInputs)
    # print(kPageHasTextInputs)

    _, kPageHasPswdInputs = has_pswd_inputs(html)
    features.append(kPageHasPswdInputs)
    # print(kPageHasPswdInputs)

    _, kPageHasRadioInputs = has_radio_inputs(html)
    features.append(kPageHasRadioInputs)
    # print(kPageHasRadioInputs)

    _, kPageHasCheckInputs = has_check_inputs(html)
    features.append(kPageHasCheckInputs)
    # print(kPageHasCheckInputs)

    kPageExternalLinksFreq = external_links(url, html)
    features.append(kPageExternalLinksFreq)
    # print(kPageExternalLinksFreq)

    kPageSecureLinksFreq = use_https(html)
    features.append(kPageSecureLinksFreq)
    # print(kPageSecureLinksFreq)

    kPageNumScriptTagsGTOne = n_script_greater_one(html)
    features.append(kPageNumScriptTagsGTOne)
    # print(kPageNumScriptTagsGTOne)

    kPageNumScriptTagsGTSix = n_script_greater_six(html)
    features.append(kPageNumScriptTagsGTSix)
    # print(kPageNumScriptTagsGTSix)

    features.append(label)

    return features

if __name__ == '__main__':
    main()