import urllib.request
import datetime
import logging
import argparse


logging.basicConfig(filename = "errors.log",  level= logging.ERROR)
assignment2 = logging.getLogger()

# download data csv from s3  //aws
def downloadData(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
    return the_page


# process data with error log
def processData(contents):  
    data = contents.decode('utf8').split('\n')
    personDict = {}
    format = "%d/%m/%Y"
    
    for item in data[1:-1]:
        val = item.split(',')
        try:
            date = datetime.datetime.strptime(val[2],format)
            personDict[val[0]] = (val[1],date)
#             print(type(date))
        except:
            assignment2.error('Error processing line '+val[0]+' for ID '+val[0]+'')
    return personDict

# display person info
def displayPerson(id, personData):
    try:
        info = list(personData[str(id)])
        return "Person "+str(id)+" is "+info[0]+" with a birthday of "+ datetime.datetime.strftime(info[1],"%Y/%m/%d") 
    except:
        return "No user found with that id.."        
    
# Main function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help='please enter url')
    args = parser.parse_args()
    if args.url != None:
        try:
            csvData = downloadData(args.url)
            # print(input("Enter a valid number: "))
            personData = processData(csvData)
            ID=0
            while True:
                ID = int(input("Please enter number or to exit enter 0 or less: "))
                if ID > 0:
                    print(displayPerson(ID, personData))                
                else:
                    break
        except:
            assignment2.error('Error occured while getting data from url')    

    else:
        print("Exit")
        parser.exit()     

if __name__ == "__main__":
    main()    