import requests
import argparse

PROG_NAME = "pycrtsh.py"
PROG_DESC = "Find sub-domains using Certificate Transparency with crt.sh as the resource"

CRTSH_URL = "https://crt.sh/?q={}&output=json"

def args():
    parser = argparse.ArgumentParser(prog=PROG_NAME,
                                     description=PROG_DESC)
    parser.add_argument("domain", help="Find sub-domains for this domain")
    parser.add_argument("--output", help="Output to this path", default=None)
    args = parser.parse_args()
    return (args.domain, args.output)

def main():
    domain, output = args()

    print("""args:
    domain = {}
    output = {}""".format(domain, output))

    response = requests.get(CRTSH_URL.format(domain))
    subs = set()
    for row in response.json():
        subs.add(row['common_name'])

    if output:
        with open(output, "w+") as fp:
            fp.write("\n".join(sorted(subs)))
    else:
        print(sorted(subs))


if __name__ == '__main__':
    main()