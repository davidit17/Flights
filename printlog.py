import datetime

p = 'problem'
# insert to db if offer date if offerdate is not exist


if  (datetime.datetime.strptime(findLastDate(),"%Y-%m-%d").date()) < max(merged.offerDate) :
    insert(merged)
    p = "Data inserted"
else :
    p = "Already in database" + " last date : " + str(findLastDate()) + "current date : " +str (max(merged.offerDate))
   

#print log - to log.txt file

today = datetime.date.today()

with open("log.txt", "a") as text_file:
    text_file.write(" Date : " + str(today) + " result: " +  p + "\n")