# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 11:32:13 2017

@author: panos
"""
import RPi.GPIO as GPIO
import time
import os
import smtplib
GPIO.setmode(GPIO.BOARD) #Ορίζουμε ότι θα αναφερόμαστε στα pin με την φυσική τους διάταξη
GPIO.setup(7, GPIO.IN) #Ορίζουμε το PIN 7 σαν ΕΙΣΟΔΟ
GPIO.setup(11, GPIO.IN) #Ορίζουμε το PIN 11 σαν ΕΙΣΟΔΟ, θα χρησιμοποιηθεί για τον ορισμό του επόμενου βαγονιού ως δοκιμής
GPIO.setup(12, GPIO.IN) #Ορίζουμε το PIN 12 σαν ΕΙΣΟΔΟ, θα χρησιμοποιηθεί για ΟΚ
GPIO.setup(13, GPIO.IN) #Ορίζουμε το PIN 13 σαν ΕΙΣΟΔΟ, θα χρησιμοποιηθεί για  ΑΚΥΡΟ
#Αρχικοποίηση
### FAILSAIFE###
#Έχουμε φτιάξει ένα αρχείο με ονομασία total.txt.
#Αν για κάποιο λόγο κολλήσει ή επανεκκινήσει το raspberry, ο συνολικός αριθμός βαγονιών θα επανα-ανακτηθεί, από εκεί!
#Να κάνουμε το ίδιο ίσως και για τις τιμές bagoni1...5
#ΤO DO....

orismos = 0
prev_input = 0 #Ορίζουμε μια μεταβλητή ως προηγούμενη είσοδο με τιμή 0 (υποθέτουμε ότι το τερματικό δεν είναι πατημένο)
prev_input11 = 0
prev_input12 = 0
prev_input13 = 0
input11=0
input12=0
input13=0
counter = 0 #Τρέχουσα μέτρηση
counterold=0 #Χθεσινή μέτρηση
total = 0 #Συνολική μέτρηση
#Λαμβάνουμε την τιμή της ώρας εκκίνησης
from time import strftime
month1 = int(strftime("%m"))
day1 = int(strftime("%d"))
hour1 = int(strftime("%H")) #Lambanoume thn arithmitiki timh ths wras
minute1 =  int(strftime("%M"))
#Ορίζω έως 5 βαγόνια για δοκιμή. Αρχική τιμή μηδέν.
bagoni1 = 50 #AYTO ΠΙΘΑΝΟΝ ΝΑ ΤΟ ΑΛΛΑΞΟΥΜΕ ΣΥΜΦΩΝΑ ΜΕ ΤΗΝ ΣΚΕΨΗ ΤΟΥ FAILSAFE
bagoni2 = 23
bagoni3 = 65
bagoni4 = 22
bagoni5 = 70
datetime1 = '1-1-2018, 00:00:00'
datetime2 = '1-1-2018, 00:00:00'
datetime3 = '1-1-2018, 00:00:00'
datetime4 = '1-1-2018, 00:00:00'
datetime5 = '1-1-2018, 00:00:00'
timestamp = 0
rythm=1
#Ορισμός παραμέτρων για την αποστολή email
sender = 'no-reply@panagiotopoulos.gr' #orismos timhs apostolea, tha xrhsimopoiithei argotera otan tha stelnoume eidopoihseis mesw email
receivers = ['panagiotopoulos@gmail.com'] #to idio me apo panw
emailheader="""From: Dryer Control <no-reply@panagiotopoulos.gr>
To: Panos <panagiotopoulos@gmail.com>
Subject: Εξέρχεται Βαγόνι
"""

#
#
#
#
#Ξεκινάει επαναλαμβανόμενα η λήψη μετρήσεων
while True:
  orismos = 0
  #διαβάζει την είσοδο στο Pin7
  input = GPIO.input(7)
  #αν η τελευταία ανάγνωση ήταν low και αυτή είναι high, κάνε τα εξής...
  if ((not prev_input) and input):
    os.system('clear')
    print("Έξοδος Βαγονιού")
    counter = counter+1
    timestamp =time.time()
    if counter ==1:
	timestamp1 = timestamp
    total = total +1
    day = int(strftime("%d"))
    print strftime("%Y-%m-%d %H:%M:%S")
    print 'Έχουν βγει', counter, 'βαγόνια σήμερα, και', total, 'συνολικά.'
    apothikeuma = strftime("%Y-%m-%d %H:%M:%S")+str(counter)
    file = open('vagonia.txt','a')	
    file.write(apothikeuma)
    file.close()
    file = open('total.txt','w')	
    file.write(str(total))
    file.close()
    if counter>1:
	rythm = counter/((timestamp-timestamp1)/3600)
	print 'Μέσος ρυθμός βαγονιών σήμερα', rythm, 'βαγόνια ανά ώρα' 
    print 'Την προηγούμενη ημέρα βγήκαν:', counterold, 'βαγόνια.'
    diff1 = (bagoni1 + 107)-total
    diff2 = (bagoni2 + 107)-total
    diff3 = (bagoni3 + 107)-total
    diff4 = (bagoni4 + 107)-total
    diff5 = (bagoni5 + 107)-total
    #Αν σε μια θέση μνήμης υπάρχει βαγόνι υπό δοκιμή, τυπώνουμε σε πόσα βαγόνια θα βγει το συγκεκριμένο.
    #Όταν η διαφορά (σε πόσα βαγόνια) μηδενίσει, τυπώνουμε ότι βγήκε τώρα και μηδενίζουμε την θέση μνήμης.
    if bagoni1>0:
	message1 = 'Το βαγόνι που μπήκε την '+ str(datetime1)+', θα βγει σε '+str(diff1)+' βαγόνια, ή περίπου '+str(diff1/rythm)+' ώρες. (ΘΕΣΗ ΜΝΗΜΗΣ: 1)'	
	print message1
    if diff1 == 0:
	print 'Το βαγόνι που μπήκε την', datetime1, '(ΘΕΣΗ ΜΝΗΜΗΣ: 1), βγήκε ΤΩΡΑ'
	bagoni1 = 0
	print 'Η θέση μνήμης 1 άδειασε'
    if bagoni2>0:
        message2 = 'Το βαγόνι που μπήκε την '+ str(datetime2)+', θα βγει σε '+str(diff2)+' βαγόνια, ή περίπου '+str(diff2/rythm)+' ώρες. (ΘΕΣΗ ΜΝΗΜΗΣ: 2)'	
	print message2
    if diff2 == 0:
        print 'Το βαγόνι που μπήκε την', datetime2, '(ΘΕΣΗ ΜΝΗΜΗΣ: 2), βγήκε ΤΩΡΑ'
        bagoni2 = 0
        print 'Η θέση μνήμης 2 άδειασε'
    if bagoni3>0:
	message3 = 'Το βαγόνι που μπήκε την '+ str(datetime3)+', θα βγει σε '+str(diff3)+' βαγόνια, ή περίπου '+str(diff3/rythm)+' ώρες. (ΘΕΣΗ ΜΝΗΜΗΣ: 3)'	
	print message3
    if diff3 == 0:
        print 'Το βαγόνι που μπήκε την', datetime3, '(ΘΕΣΗ ΜΝΗΜΗΣ: 3), βγήκε ΤΩΡΑ'
        bagoni3 = 0
        print 'Η θέση μνήμης 3 άδειασε'
    if bagoni4>0:
        message4 = 'Το βαγόνι που μπήκε την '+ str(datetime4)+', θα βγει σε '+str(diff4)+' βαγόνια, ή περίπου '+str(diff4/rythm)+' ώρες. (ΘΕΣΗ ΜΝΗΜΗΣ: 4)'	
	print message4
    if diff4 == 0:
        print 'Το βαγόνι που μπήκε την', datetime4, '(ΘΕΣΗ ΜΝΗΜΗΣ: 4), βγήκε ΤΩΡΑ'
        bagoni4 = 0
        print 'Η θέση μνήμης 4 άδειασε'
    if bagoni5>0:
        message5 = 'Το βαγόνι που μπήκε την '+ str(datetime5)+', θα βγει σε '+str(diff5)+' βαγόνια, ή περίπου '+str(diff5/rythm)+' ώρες. (ΘΕΣΗ ΜΝΗΜΗΣ: 5)'	
	print message5
    if diff5 == 0:
        print 'Το βαγόνι που μπήκε την', datetime5, '(ΘΕΣΗ ΜΝΗΜΗΣ: 5), βγήκε ΤΩΡΑ'
        bagoni5 = 0
        print 'Η θέση μνήμης 5 άδειασε'
    #αποστολή ειδοποιήσεων
    if diff1 ==10:
	message = emailheader + message1
	try:
        	smtpObj = smtplib.SMTP('smtp.otenet.gr', 25)
                smtpObj.sendmail(sender, receivers, message)         
                print "Εστάλη email για το βαγόνι ΘΕΣΗΣ 1"
        except:
        	pass
    if diff2 ==10:
	message = emailheader + message2
	try:
        	smtpObj = smtplib.SMTP('smtp.otenet.gr', 25)
                smtpObj.sendmail(sender, receivers, message)         
                print "Εστάλη email για το βαγόνι ΘΕΣΗΣ 2"
        except:
        	pass
    if diff3 ==10:
	message = emailheader + message3
	try:
        	smtpObj = smtplib.SMTP('smtp.otenet.gr', 25)
                smtpObj.sendmail(sender, receivers, message)         
                print "Εστάλη email για το βαγόνι ΘΕΣΗΣ 3"
        except:
        	pass
    if diff4 ==10:
	message = emailheader + message4
	try:
        	smtpObj = smtplib.SMTP('smtp.otenet.gr', 25)
                smtpObj.sendmail(sender, receivers, message)         
                print "Εστάλη email για το βαγόνι ΘΕΣΗΣ 4"
        except:
        	pass
    if diff5 ==10:
	message = emailheader + message5
	try:
        	smtpObj = smtplib.SMTP('smtp.otenet.gr', 25)
                smtpObj.sendmail(sender, receivers, message)         
                print "Εστάλη email για το βαγόνι ΘΕΣΗΣ 5"
        except:
        	pass
  #ενημέρωση προηγούμενης εισόδου
  prev_input = input
  #slight pause to debounce
  time.sleep(0.05)

  #Διαβάζουμε την είσοδο 11 (ΟΡΙΣΜΟΣ ΒΑΓΟΝΙΟΥ ΠΡΟΣ ΠΑΡΑΚΟΛΟΥΘΗΣΗ)
#  input11 = GPIO.input(11)  #### ΟΤΑΝ ΣΥΝΔΕΘΕΙ ΚΑΝΟΝΙΚΑ ΤΟ ΜΠΟΥΤΟΝ ΤΟ ΒΓΑΖΟΥΜΕ ΑΠΟ ΣΧΟΛΙΟ
  #if the last reading was low and this one high, print
  if ((not prev_input11) and input11):
   if bagoni1*bagoni2*bagoni3*bagoni4*bagoni5>0:
    print 'ΔΥΣΤΥΧΩΣ ΔΕΝ ΥΠΑΡΧΕΙ ΔΙΑΘΕΣΙΜΗ ΘΕΣΗ ΜΝΗΜΗΣ'
   else:
    print("Θέλετε να ορίσετε το επόμενο βαγόνι που θα μπει, προς παρακολούθηση;")
    print 'Πατήστε το μπουτόν ΟΚ για να προχωρήσετε ή ΑΚΥΡΟ για να αναιρέσετε'


    #Διαβάζουμε την είσοδο 12 για επιβεβαίωση
#    input12 = GPIO.input(12)  #### ΟΤΑΝ ΣΥΝΔΕΘΕΙ ΚΑΝΟΝΙΚΑ ΤΟ ΜΠΟΥΤΟΝ ΤΟ ΒΓΑΖΟΥΜΕ ΑΠΟ ΣΧΟΛΙΟ
    #if the last reading was low and this one high, print
    if ((not prev_input12) and input12):
    	print("OΚ")
	orismos = 1
    #ενημέρωση προηγούμενης εισόδου για το PIN12 και λίγο κόψιμο για να κάνει debounce
    prev_input12 = input12
    time.sleep(0.05)

    #Διαβάζουμε την είσοδο 13 για ακύρωση
#   input13 = GPIO.input(13)  #### ΟΤΑΝ ΣΥΝΔΕΘΕΙ ΚΑΝΟΝΙΚΑ ΤΟ ΜΠΟΥΤΟΝ ΤΟ ΒΓΑΖΟΥΜΕ ΑΠΟ ΣΧΟΛΙΟ
    #if the last reading was low and this one high, print
    if ((not prev_input13) and input13):
        print("Η καταχώρηση αναιρέθηκε")
	orismos = 0
    #ενημέρωση προηγούμενης εισόδου για το PIN13 και λίγο κόψιμο για να κάνει debounce
    prev_input13 = input13
    time.sleep(0.05)

  #ενημέρωση προηγούμενης εισόδου για το PIN11
  prev_input11 = input11
  #slight pause to debounce
  time.sleep(0.05)



  #κόψιμο κάνα 2υο δευτερόλεπτα για να προλαβουμε να δουμε τις ενημερωσεις
  
  #AN έχουμε ορίσει να παρακολουθήσουμε κάποιο βαγόνι, ελέγχουμε μια μια τις θέσεις μνήμης και στην πρώτη που θα βρούμε κενή καταγράφουμε τον
  #αύξοντα αριθμό του βαγονιού από το total αρχικά, καθώς επίσης και την ημερομηνία και ώρα εισόδου (ορισμού στην ουσία) για να αναφερόμαστε σε
  #αυτό.
  if orismos == 1:
	if bagoni1==0:
		bagoni1=total
		datetime1=strftime("%d-%m-%Y %H:%M:%S")
		print 'Το βαγόνι που μπαίνει στο ξηραντηριο την', datetime1, 'καταχωρήθηκε στην ΘΕΣΗ ΜΝΗΜΗΣ 1'
	elif bagoni2==0:
		bagoni2=total
		datetime2=strftime("%d-%m-%Y %H:%M:%S")
		print 'Το βαγόνι που μπαίνει στο ξηραντηριο την', datetime2, 'καταχωρήθηκε στην ΘΕΣΗ ΜΝΗΜΗΣ 2'
	elif bagoni3==0:
		bagoni3=total
		datetime3=strftime("%d-%m-%Y %H:%M:%S")
		print 'Το βαγόνι που μπαίνει στο ξηραντηριο την', datetime3, 'καταχωρήθηκε στην ΘΕΣΗ ΜΝΗΜΗΣ 3'
	elif bagoni4==0:
		bagoni4=total
		datetime4=strftime("%d-%m-%Y %H:%M:%S")
		print 'Το βαγόνι που μπαίνει στο ξηραντηριο την', datetime4, 'καταχωρήθηκε στην ΘΕΣΗ ΜΝΗΜΗΣ 4'
	else :
		bagoni5=total
		datetime5=strftime("%d-%m-%Y %H:%M:%S")
		print 'Το βαγόνι που μπαίνει στο ξηραντηριο την', datetime5, 'καταχωρήθηκε στην ΘΕΣΗ ΜΝΗΜΗΣ 5'



  #Αν ο μετρητής δεν είναι μηδενικός, όταν αλλάξει η ημέρα μηδενίζει...αυτό να μπει στο τέλος
  if counter > 0:
	if int(strftime("%d")) - day > 0:
		counterold = counter #κρατάμε μνήμη την χθεσινή παραγωγή
		counter = 0 #μηδενίζουμε

