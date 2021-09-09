import pandas as pd
import numpy as np
import argparse

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
                    'label',
                    'url'
                ]

def command_line_parsing():

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('--features_file', '-i', 
                        dest='input_file', 
                        required=True, 
                        help='Path to the dataset witch store the features extracted.')

    parser.add_argument('--url-feature-extracted', '-o', 
                        dest='output_file', 
                        required=True, 
                        help='Path to csv file where the collected features will be stored.')

    return parser.parse_args()


def list_series_to_dataframe(list_series):

    list_series.columns = ['old'] 

    dataframe = pd.DataFrame(list_series['old'].to_list(), columns=features_names)

    return dataframe

def main():

    args = command_line_parsing()

    dataset = pd.read_csv(args.input_file)

    dataframe = list_series_to_dataframe(dataset)

    dataframe.to_csv(args.output_file, index=False)


if __name__ == '__main__':

    main()