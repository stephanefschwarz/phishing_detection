from dom_feature_extractor import *
from url_feature_extractor import *

import numpy as np
import pandas as pd
import argparse
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import logging
import time

import multiprocessing as mp
from multiprocessing import Pool, cpu_count
from multiprocessing import log_to_stderr, get_logger

#log_to_stderr()
#logger = get_logger()
#logger.setLevel(logging.INFO)

logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

tqdm.pandas()

features_names = [
                    'url',
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
                    'isPhishing'
                ]
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

def extract_features( row ):  
   
    features = []

    url = row.url
    label = row.label



    try:            
        page = requests.get(url)

    except:
        return [0] * 14 + [label]

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
    features.append(url)

    return features

def process_partition(partition):

    return partition.apply(extract_features, axis=1)

def parallelizedSeriesApply(data, extract_features, 
                            NUM_PROCESSES=min(10, cpu_count()), 
                            NUM_PARTITIONS=cpu_count(), 
                            processPartition=process_partition):

    partitions = np.array_split(data, NUM_PARTITIONS)
    results = []

    with Pool(processes=NUM_PROCESSES) as p:
        with tqdm(total=NUM_PARTITIONS, desc='Parallel Processing') as pbar:
            for result in p.imap_unordered(processPartition, partitions):
                pbar.update()
                results.extend(result)

    df = pd.DataFrame(results, columns=features_names)

    return df
    #return pd.concat(results)


def main():

    args = command_line_parsing()

    dataset_path = args.url_dataset
    dataset = pd.read_csv(dataset_path)

    dataset = dataset.drop_duplicates(subset=['url'])

    print('----'*10)
    
    logging.info("Extracting features... \n\n")
    
    start_time = time.time()

    logging.info("Start time: {:.2f}".format(start_time))
    
    output_result = parallelizedSeriesApply(dataset, extract_features)
    
    logging.info("End time: {:.2f}".format(time.time()))
    logging.info("Total time spended: {:.2f}".format(time.time() - start_time))

    logging.info("Saving file...")

    output_result.to_csv(args.output_file, index=False)

    logging.info("Done!")


if __name__ == '__main__':
    main()