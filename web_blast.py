import re
import sys
import time
import requests

try:
    import urllib.parse as urllib_parse  # py3
except ImportError:
    import urllib as urllib_parse  # py2


def url_escape(value):
    """Returns a URL-encoded version of the given value."""
    return urllib_parse.quote_plus(value)

if __name__ == '__main__':
    if(len(sys.argv) < 4):
        print ("usage: web_blast.py program database query [query]...")
        print ("where program = megablast, blastn, blastp, rpsblast, blastx, tblastn, tblastx")
        print ("example: web_blast.py blastp nr protein.fasta")
        print ("example: web_blast.py rpsblast cdd protein.fasta")
        print ("example: web_blast.py megablast nt dna1.fasta dna2.fasta")
        sys.exit()

    program  = sys.argv[1]
    database = sys.argv[2]

    if program == 'megablast':
        program = 'blastn&MEGABLAST=on'
    elif program == 'rpsblast':
        program = 'blastp&SERVICE=rpsblast'

    encoded_query = ''
    for query in sys.argv[3:]:
        with open (query) as QUERY:
            for line in QUERY:
                encoded_query = encoded_query + url_escape(line)

    args = "CMD=Put&PROGRAM=%s&DATABASE=%s&QUERY=%s" %(program, database, encoded_query)
    # print (args)
    url = "https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi?%s" %(args)
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
    # data = {"CMD": "Put", "PROGRAM":program, "DATABASE":database, "QUERY":encoded_query}
    res = requests.post(url=url, headers=HEADERS)
    res.encoding = 'gbk'

    rid  = ''
    rtoe = ''
    for line in res.content.decode('utf-8').split("\n"):
        obj1 = re.match(r".*?RID = (.*)",line)
        obj2 = re.match(r".*?RTOE = (.*)", line)
        try:
            rid = obj1.group(1)
        except:
            pass

        try:
            rtoe = obj2.group(1)
        except:
            pass

    # print (rid)
    # print (rtoe)
    while(True):
        print ("continueing")
        time.sleep(5)

        req = requests.get("https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Get&FORMAT_OBJECT=SearchInfo&RID=%s" %(rid))

        flag = False
        flag_2 = False
        for line in req.content.decode('utf-8').split("\n"):
            obj1 = re.match(r"\s+Status=WAITING", line)
            if obj1 is not None:
                flag = True

            obj1 = re.match(r"\s+Status=READY", line)
            if obj1 is not None:
                flag_2 = True

            if flag or flag_2:
                break
        if flag_2:
            break

    print ("Status READY!")
    req = requests.get("https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Get&FORMAT_TYPE=Text&RID=%s" %(rid))
    with open("out.txt","w") as QUERY:
        flag_start = False
        Query_id = ''
        for line in req.content.decode('utf-8').split("\n"):
            print (line)
            if (re.match("^$",line, re.M|re.I) or re.match("^Length",line, re.M|re.I) or re.match("^Sequences producing significant alignments",line, re.M|re.I)):
                continue

            obj = re.match("Query=(.*)",line, re.M|re.I)
            if obj is not  None:
                flag_start = True
                Query_id = obj.group(1)
                continue

            obj = re.match("ALIGNMENTS", line, re.M|re.I)
            if obj is not None:
                flag_start = False

            if flag_start:
                QUERY.write(Query_id + " " + line + "\n")
