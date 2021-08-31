import numpy as np
import requests
from bs4 import BeautifulSoup
import re
from url_feature_extractor import *

HTTPS = re.compile('^(http|https)://')


# ////////////////////////////////////////////////////
# // DOM HTML form features
# ////////////////////////////////////////////////////

def get_page(url):

    page = requests.get(url)
    html = BeautifulSoup(page.content, 'html.parser')

    return html

def get_all_page_links(html):

    all_links = html.findAll(href=True)
    all_links = [element['href'] for element in all_links]

    return all_links

# kPageHasForms
def has_forms(html):

    forms = html.findAll('form')
    kPageHasForms = not(forms == [])

    return forms, kPageHasForms 

# kPageActionOtherDomainFreq
def other_domain_ratio(url, forms):

    domain = get_domain_token(url)

    all_domains = [get_domain_token(form.get('action')) for form in forms if form.get('action') != '']

    occorrences = all_domains.count(domain)
    total = len(forms)

    return occorrences / total

# kPageActionURL
def page_action_url(forms):

    all_action_urls = [form.get('action') for form in forms]
    
    return all_action_urls


# kPageHasTextInputs
def has_text_inputs(html):

    text_inputs = html.findAll('inputs', {'type':'text'})
    kPageHasTextInputs = not(text_inputs == [])

    return text_inputs, kPageHasTextInputs

# kPageHasPswdInputs
def has_pswd_inputs(html):

    pswd_inputs = html.findAll('inputs', {'type':'password'})
    kPageHasPswdInputs = not(pswd_inputs == [])

    return pswd_inputs, kPageHasPswdInputs

# kPageHasRadioInputs
def has_radio_inputs(html):

    radio_inputs = html.findAll('inputs', {'type':'radio'})
    kPageHasRadioInputs = not(radio_inputs == [])

    return radio_inputs, kPageHasRadioInputs


# kPageHasCheckInputs
def has_check_inputs(html):

    check_inputs = html.findAll('inputs', {'type':'checkbox'})
    kPageHasCheckInputs = not(check_inputs == [])

    return check_inputs, kPageHasCheckInputs

# ////////////////////////////////////////////////////
# // DOM HTML link features
# ////////////////////////////////////////////////////

# kPageLinkDomain
def token_ext_domain(url, html):

    all_links = get_all_page_links(html)

    domains = np.array([get_domain_token(href_url) for href_url in all_links])
    host_domain = get_domain_token(url)

    ext_domains = np.unique(np.where(domains != host_domain))

    return ext_domains, len(domains)

# kPageExternalLinksFreq
def external_links(url, html):

    ext_domains, total_domains = token_ext_domain(url, html)

    return len(ext_domains) / total_domains

# kPageSecureLinksFreq
def use_https(html):

    all_links = get_all_page_links(html)

    total_links = len(np.unique(all_links))

    starts_with_https = [bool(re.match(HTTPS, url) for url in all_links)]

    return sum(starts_with_https) / total_links

# ////////////////////////////////////////////////////
# // DOM HTML script features
# ////////////////////////////////////////////////////

# kPageNumScriptTagsGTOne
def n_script_greater_one(html):

    scripts = html.findAll('scripts')

    if len(scripts) > 1:
        return True
    return False

# kPageNumScriptTagsGTSix
def n_script_greater_six(html):

    scripts = html.findAll('scripts')

    if len(scripts) > 6:
        return True
    return False

# ////////////////////////////////////////////////////
# // Other DOM HTML features
# ////////////////////////////////////////////////////

# kPageImgOtherDomainFreq
def img_external_src(url, html):
    
    all_img = html.findAll('img')
    all_img_domains = [get_domain_token(element['src']) for element in all_img if element['src'] != '']

    host_domain = get_domain_token(url)

    ext_domains = np.unique(np.where(all_img_domains != host_domain))

    return len(all_img_domains) / len(ext_domains)
    

# ////////////////////////////////////////////////////
# // Page term features
# ////////////////////////////////////////////////////