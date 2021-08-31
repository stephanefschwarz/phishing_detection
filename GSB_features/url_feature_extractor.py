from urllib import parse
from urllib.parse import urlparse
import re
import time
import tldextract

IP = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

# -----------------------------------
# To be removed
# url_parse = urlparse(URL)
# url_tldex = tldextract.extract(URL)
# URL = "http://123.0.0.1/mydocuments/a.file.html"
# To be removed
# -----------------------------------

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def is_local_ref(url):
  """
  Checks whether `url` is a local ref.
  """
  parsed = urlparse(url)

  return not(bool(parsed.netloc)) and bool(parsed.path)

# ////////////////////////////////////////////////////
# // Host features
# ////////////////////////////////////////////////////

# kUrlHostIsIpAddress
def is_ip(url):

    url_domain_netloc = tldextract.extract(url).domain

    kUrlHostIsIpAddress = False if (re.findall(IP, url_domain_netloc) == []) else True
    return kUrlHostIsIpAddress

# kUrlTldToken
def get_host_token(url):

    url_tldex = tldextract.extract(url)
   
    kUrlTldToken = url_tldex.suffix
    return kUrlTldToken

# kUrlDomainToken
def get_domain_token(url):

    url_tldex = tldextract.extract(url)

    kUrlDomainToken = url_tldex.domain
    return kUrlDomainToken

# kUrlOtherHostToken
def get_domain_others(url):

    url_tldex_subdomain = tldextract.extract(url)

    splited = url_tldex_subdomain.split('.')
    size_limit = 1 if len(splited) < 3 else len(splited) - 1 

    kUrlOtherHostToken = splited[-size_limit:]
    return kUrlOtherHostToken

# ////////////////////////////////////////////////////
# // Aggregated features
# ////////////////////////////////////////////////////

# kUrlNumOtherHostTokensGTOne
def other_tokens_greater_one(url):

    url_tldex_subdomain = tldextract.extract(url).subdomain

    kUrlNumOtherHostTokensGTOne = True if len(get_domain_others(url_tldex_subdomain)) > 1 \
                                                                                else False

    return kUrlNumOtherHostTokensGTOne

# kUrlNumOtherHostTokensGTThree
def other_tokens_greater_three(url):

    url_tldex_subdomain = tldextract.extract(url).subdomain

    kUrlNumOtherHostTokensGTThree = True if len(get_domain_others(url_tldex_subdomain)) > 3 \
                                                                                else False

    return kUrlNumOtherHostTokensGTThree

# ////////////////////////////////////////////////////
# // URL path features
# ////////////////////////////////////////////////////

# kUrlPathToken
def get_path_token(url):

    url_parse_path = parse(url).path

    kUrlPathToken = [(token) for token in re.split(r"\W+", url_parse_path) if len(token) > 1]

    return kUrlPathToken