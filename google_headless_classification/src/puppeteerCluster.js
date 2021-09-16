const data = require('../resources/phishing_urls.json')
const { Cluster } = require('puppeteer-cluster')
const querystring = require('querystring')
const { v1 } = require('uuid')
const { join } = require('path')

const createCsvWriter = require('csv-writer').createObjectCsvWriter;
const csvWriter = createCsvWriter({
    path: './output_phishing_urls.csv',
    header: [
        {id: 'url', title: 'URL'},
        {id: 'label', title: 'LABEL'},
        {id: 'diagnose', title: 'DIAGNOSE'}
    ]
});

const STATUS_SUSPENDED = " Account Suspended";
var PAGE_INFO = [];


async function render({ page, data : { finalUrl } }) {
    
    //const output = join(__dirname, `/../output/${v1()}.pdf`)
    var url = finalUrl;
    var label = '';
    var diagnose = '';
    
    try {
              
        await page.goto(finalUrl, { waitUntil: 'networkidle2', });

        const status_reason = await page.evaluate(() => {
            try {
                
                return document.querySelector('div[class="container"] > span[class="status-reason"]').innerText;
                
            } catch (error) {
                return null                
            }
            
        });  
        
        //check_status_reason(finalUrl, status_reason)

        if (status_reason == STATUS_SUSPENDED){
            //console.log(`<${url}> \n suspended - Phishing detected  \n -------`);
            label = 'phishing';
            diagnose = 'suspended';
        } else {
            label = 'safe';
            diagnose = 'no_status_reason';
        }
        
    } catch (error) {

        label = 'phishing';
                    
        if (error.message.includes('ERR_CERT_COMMON_NAME_INVALID')) {            
            //console.log(`<${finalUrl}> \n Certificate error - PHISHING DETECTED!! \n -------`);
            diagnose = 'ERR_CERT_COMMON_NAME_INVALID';

        }else if (error.message.includes('ERR_NAME_NOT_RESOLVED')) {            
            //console.log(`<${finalUrl}> \n Name error - PHISHING DETECTED!! \n -------`);
            diagnose = 'ERR_NAME_NOT_RESOLVED';
            
        }else if (error.message.includes('ERR_CERT_AUTHORITY_INVALID')) {            
            //console.log(`<${finalUrl}> \n Invalid Certificate - PHISHING DETECTED!! \n -------`);
            diagnose = 'ERR_CERT_AUTHORITY_INVALID';
            
        }else if (error.message.includes('ERR_ADDRESS_UNREACHABLE')) {            
            //console.log(`<${finalUrl}> \n Inreachable address - PHISHING DETECTED!! \n -------`);
            diagnose = 'ERR_ADDRESS_UNREACHABLE';
            
        }else if (error.message.includes('Protocol error')) {            
            //console.log(`<${finalUrl}> \n Protocol error {This page has been reported as dangerous} - PHISHING DETECTED!! \n -------`);
            diagnose = 'PROTOCOL_ERROR';
            
        }else if (error.message.includes('ERR_CONNECTION_RESET')) {            
            //console.log(`<${finalUrl}> \n Connection reset - PHISHING DETECTED!! \n -------`);
            diagnose = 'ERR_CONNECTION_RESET';
            
        }else if (error.message.includes('ERR_SSL_VERSION_OR_CIPHER_MISMATCH')) {            
            //console.log(`<${finalUrl}> \n Mismatch - PHISHING DETECTED!! \n -------`);
            diagnose = 'ERR_SSL_VERSION_OR_CIPHER_MISMATCH';
            
        } else {
            //console.log(`<${finalUrl}> \n ERROR: |${error}| \n -------`);
            diagnose = error.message;            
        }
    } 

    let records = {'url':url, 'label':label, 'diagnose':diagnose};
    
    PAGE_INFO.push(records)
    
    let bodyHTML = await page.evaluate(() => document.body.innerHTML);
    if (bodyHTML == ''){
        console.log(`${finalUrl} PHISHING`);
    }
    console.log(`BODY: |${bodyHTML}|`); // use body for status reason
    
    console.log('ended', finalUrl)
    console.log("----------------");
}

function createQueryStringFromObject(data) {
    const separator = null;
    const keyDelimiter = null;
    const options = { encodeURIComponent: querystring.unescape };
    const qs = querystring.stringify(data, separator, keyDelimiter, options);
    return qs;
}

async function main() {

    const cluster = await Cluster.launch({
        concurrency: Cluster.CONCURRENCY_CONTEXT,
        maxConcurrency: 10,
        puppeteerOptions: {
            headless: true,
            args: ['--no-sandbox']
        },
        executablePath: '/opt/google/chrome/chrome',
        userDataDir: '/opt/google/chrome/chrome'
    });

    await cluster.task(render);
    
    for (const item of data) {
       
        const finalUrl = item.url;
        
        await cluster.queue({finalUrl});
        
    }

    await cluster.idle();
    await cluster.close();
/*
    csvWriter.writeRecords(PAGE_INFO)       // returns a promise
    .then(() => {
        console.log('...Done');
    });

*/
}

function check_status_reason(url, status_reason){

    if (status_reason == STATUS_SUSPENDED){
        console.log(`<${url}> \n suspended - Phishing detected  \n -------`);
    }
}


main()



