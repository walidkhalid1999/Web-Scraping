from bs4 import BeautifulSoup 
import csv
import requests


#connect to the URL
date = input("please enter the date in the following formate mm/dd/yyyy : ")
page = requests.get("https://www.yallakora.com/match-center?date={}".format(date))


def main(page):
    
    #get all of the content of the page
    src = page.content
    
    #put the code in beatiful format to read
    soup = BeautifulSoup(src , "lxml")
    matches_details = []
    
    #get the div that contains all of the matches in the content
    championship = soup.find_all("div" , {'class' : 'matchCard'})
    
    def get_match_info(championship):
        #get the champions in this day
        championship_title = championship.contents[1].find("h2").text.strip() 
        
        #get all matches in this day
        all_matches = championship.contents[3].find_all("li")
        number_of_matches = len(all_matches)
        
        #looping on the number of matches to get the teams name , scores , and the time 
        for i in range(number_of_matches):
            #get the teams
            team_a = all_matches[i].find("div" , {'class' : 'teamA'}).text.strip()
            team_b = all_matches[i].find("div" , {'class' : 'teamB'}).text.strip()
            
            #get the scores
            match_result = all_matches[i].find('div' , {'class' : 'MResult'}).find_all('span' , {'class' : 'score'})
            score = "{} - {}".format(  match_result[0].text.strip() , all_matches[1].text.strip() )
            
            #get the time of the matches
            time = all_matches[i].find('div' , {'class' : 'MResult'}).find('span' , {'class' : 'time'}).text.strip()
            
            #put all this information in a dict to present it 
            matches_details.append({
                                    "champion type" : championship_title , 
                                    "first team" : team_a , 
                                    "second team" : team_b  , 
                                    "match time" : time , 
                                    "match score" : score
                                    })
    
    #looping on all of the champions to extract these data from every champion in this day        
    for i in range(len(championship)):
        get_match_info(championship[i])
    
    #the headers of the table
    keys = matches_details[0].keys()
    
    #create a CSV file to store these data in it
    with open ('example.csv' , 'w') as output_file:
        dict_writer = csv.DictWriter(output_file , keys)
        dict_writer.writeheader()
        dict_writer.writerows(matches_details)
        print("file created")

    
    
main(page)
















