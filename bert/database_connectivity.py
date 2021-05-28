import mysql.connector

def DataUpdate(pain, pain_location, missed_events, sleep, stress, feedback): 
    mydb = mysql.connector.connect(
        host="localhost", 
        user="root",  
        passwd="root", 
        database="Rasa_feedback"
    ) 

    mycursor = mydb.cursor() 
    
    #sql="CREATE TABLE Rasa_feedback (pain INT(255), pain_location VARCHAR(255), missed_events BOOLEAN, sleep VARCHAR(255), stress VARCHAR(255), feedback VARCHAR(255));"

    sql='INSERT INTO Rasa_feedback (pain, pain_location, missed_events, sleep, stress, feedback) VALUES ("{0}", "{1}", "{2}", "{3}", "{4}", "{5}");'.format(pain, pain_location, missed_events, sleep, stress, feedback)
    mycursor.execute(sql)

    mydb.commit()
    
    print(mycursor.rowcount, "record inserted.")

# if __name__=="__main__":
#     DataUpdate("8", "legs", 1, "8 hours", "high", "Great")