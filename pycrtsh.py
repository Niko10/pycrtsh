import requests
import argparse


PROG_BANNER = """
                        _       _     
                       | |     | |    
  _ __  _   _  ___ _ __| |_ ___| |__  
 | '_ \| | | |/ __| '__| __/ __| '_ \ 
 | |_) | |_| | (__| |  | |_\__ \ | | |
 | .__/ \__, |\___|_|   \__|___/_| |_|
 | |     __/ |                        
 |_|    |___/   
 
 
 
 By Ori Hadad                      
"""
PROG_NAME = "pycrtsh.py"
PROG_DESC = "Find sub-domains using Certificate Transparency with crt.sh as the resource"
PROG_USAGE = "python pycrtsh.py exmaple-domain.com --output /output/directory/subdomains.txt"

CRTSH_URL = "https://crt.sh/?q={}&output=json"


def args():
    parser = argparse.ArgumentParser(prog=PROG_NAME,
                                     description=PROG_DESC,
                                     usage=PROG_USAGE)
    parser.add_argument("domain", help="Find sub-domains for this domain")
    parser.add_argument("--output", help="Output to this path", default=None)
    parser.add_argument("--humble", help="skip the ascii art banner", default=False, action="store_true")
    args = parser.parse_args()
    return args.domain, args.output, args.humble


def main():
    domain, output, humble = args()
    if not humble:
        print(PROG_BANNER)

    print("[*] Running sub-domains search for {}".format(domain))

    response = requests.get(CRTSH_URL.format(domain))
    subs = set()
    for row in response.json():
        subs.add(row['common_name'])

    if output:
        print("[*] Output to: {}".format(output))
        with open(output, "w+") as fp:
            fp.write("\n".join(sorted(subs)))
    else:
        print("\n".join(sorted(subs)))


if __name__ == '__main__':
    main()