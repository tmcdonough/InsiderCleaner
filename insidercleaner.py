import urllib
import csv
import time

def validate_page(page):
    valid = False
    for row in page:
        if "<td width='40%'>" in row:
            valid = True
            return valid
        else:
            continue
    return valid

def get_page(link):
    #print "getting page from link: "+str(link)
    attempts = 0
    initial = ''    
    while attempts < 5:
        try:
            initial = urllib.urlopen(link)
            break
        except:
            print "Error, trying again"
            if attempts == 0:
                time.sleep(15)
            elif attempts == 1:
                time.sleep(60)
            elif attempts == 2:
                time.sleep(180)
            else:
                time.sleep(1000)
            attempts += 1
    page = []
    for i in initial:
        page.append(i)
    return page

def construct_link(cik):
    part1 = 'http://www.sec.gov/cgi-bin/own-disp?action=getissuer&CIK='
    part2 = '&type=&dateb=&owner=include&start='    
    link = part1+cik+part2
    return link

def run_through(cik_list, outfile):
    CIKs1 = csv.reader(open(cik_list, "rU"))
    CIKs = []
    for i in CIKs1: # conversion to list done simply for counting
        CIKs.append(i)
    addedcount = 0 # keeps track of number of valid CIKs (i.e., CIKs with insider transactions stored by SEC)
    with open(outfile, "w") as out_file:
        for i in CIKs:
            CIK = i[0]
            curr = time.clock()
            currentct = float(CIKs.index(i)+1)
            totalct = float(len(CIKs))
            time_remaining_seconds = (((curr-start)/currentct)*(totalct-currentct))
            time_remaining_minutes = ((((curr-start)/currentct)*(totalct-currentct))/60)
            time_remaining_hours = (((((curr-start)/currentct)*(totalct-currentct))/60)/60)
            est_completed = (currentct/totalct)
            valid = validate_page(get_page(construct_link(CIK)))
            def boiler_plate():
                print "     "+str(currentct)+" of "+str(totalct)+" CIKs checked ("+str(est_completed*100)[:5]+'%)'
                print "     "+str(addedcount)+" entries valid ("+str((addedcount/currentct)*100)[:5]+'%)'
                print "     "+str(int(currentct-addedcount))+" entries invalid"
                print "     "+str(int(currentct))+" entries checked"
                print "     Estimated time remaining: "+str(time_remaining_hours)[:5]+" hours = "+str(time_remaining_minutes)[:7]+" minutes"
            if valid:
                addedcount += 1
                print str(CIK)+" is valid"
                boiler_plate()
                out_file.write(CIK+"\n")
                #entry = [CIK]
                #for cik in entry:
                    #out_file.write("%s\n" % (cik))
                #entry = []
            else:
                print str(CIK)+" is invalid"
                boiler_plate()

start = time.clock()
run_through("CIK_med.csv", "master.csv")
end = time.clock()
print "runtime: "+str((end-start)/60)[:7]+" minutes"