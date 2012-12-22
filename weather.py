    #!/usr/bin/python
    #
    # HD44780 LCD Test Script for
    # Raspberry Pi
    #
    # Author : Matt Hawkins
    # Site   : http://www.raspberrypi-spy.co.uk
    #
    # Date   : 26/07/2012
    #

    # The wiring for the LCD is as follows:
    # 1 : GND
    # 2 : 5V
    # 3 : Contrast (0-5V)*
    # 4 : RS (Register Select)
    # 5 : R/W (Read Write)       - GROUND THIS PIN
    # 6 : Enable or Strobe
    # 7 : Data Bit 0             - NOT USED
    # 8 : Data Bit 1             - NOT USED
    # 9 : Data Bit 2             - NOT USED
    # 10: Data Bit 3             - NOT USED
    # 11: Data Bit 4
    # 12: Data Bit 5
    # 13: Data Bit 6
    # 14: Data Bit 7
    # 15: LCD Backlight +5V**
    # 16: LCD Backlight GND

    #import
import RPi.GPIO as GPIO
import time
from datetime import datetime
import urllib2
import re

    # Define GPIO to LCD mapping
LCD_RS = 17
LCD_E  = 4
LCD_D4 = 24
LCD_D5 = 22
LCD_D6 = 23
LCD_D7 = 21
LCD_LED = 18

    # Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

    # Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

def main():
      # Main program block

      GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
      GPIO.setwarnings(False)
      GPIO.setup(LCD_E, GPIO.OUT)  # E
      GPIO.setup(LCD_RS, GPIO.OUT) # RS
      GPIO.setup(LCD_D4, GPIO.OUT) # DB4
      GPIO.setup(LCD_D5, GPIO.OUT) # DB5
      GPIO.setup(LCD_D6, GPIO.OUT) # DB6
      GPIO.setup(LCD_D7, GPIO.OUT) # DB7
      GPIO.setup(LCD_LED, GPIO.OUT) # LED

      # Initialise display
      lcd_init()

      # LED backlite ON
      GPIO.output(LCD_LED, True)

      #Weather Address
      weatherURL1 = "http://aaltohtml5name.foreca.com/aaltohtml5-oct12a/data.php?l=102735943&products=cc,daily"

      while True:
        start_time = time.time()
        elapsed_time = time.time() - start_time

        while ( elapsed_time < 3 ):
      
              # Send some test
              lcd_byte(LCD_LINE_1, LCD_CMD)
              lcd_string(datetime.now().strftime('  %H : %M : %S '))
              lcd_byte(LCD_LINE_2, LCD_CMD)
              lcd_string(datetime.now().strftime('%a %d %b %Y'))

              elapsed_time = time.time() - start_time

        #Weekdays
        today = datetime.now().strftime('%a')

        if today == "Mon":
            hoje = "Segunda"
            amanha = "Terca"
            depois = "Quarta"
        elif today == "Tue":
            hoje = "Terca"
            amanha = "Quarta"
            depois = "Quinta"
        elif today == "Wed":
            hoje = "Quarta"
            amanha = "Quinta"
            depois = "Sexta"
        elif today == "Thu":
            hoje = "Quinta"
            amanha = "Sexta"
            depois = "Sabado"
        elif today == "Fri":
            hoje = "Sexta"
            amanha = "Sabado"
            depois = "Domingo"
        elif today == "Sat":
            hoje = "Sabado"
            amanha = "Domingo"
            depois = "Segunda"
        elif today == "Sun":
            hoje = "Domingo"
            amanha = "Segunda"
            depois = "Terca"

        response1 = urllib2.urlopen(weatherURL1)
        html1 = response1.read()

        w = 1
        arr = {}
        a = ""
        x=0
        while a != "</w":
            while a != "<fc" and a != "</w":
                a = html1[x:x+3]
                x +=1
            x +=1
            arr[(w,1)] = a
            while a != " />" and a != "</w":
                a = html1[x:x+3]
                arr[(w,1)] = arr[(w,1)] + a[1:2]
                x +=1
            arr[(w,1)] = arr[(w,1)] + ">"
            # print arr[(w,1)]
            w +=1

        y=1
        while y < 4:
            html1 = arr[(y,1)]
            r_temp1 = re.compile("tx=\"[0-9]{1,3}\"")
            r_temp2 = re.compile("tn=\"[0-9]{1,3}\"")
            r_cond1 = re.compile("sT=\"[\D\W]{1,40}\"")
         
            temp1_search = r_temp1.search(html1)
            temp2_search = r_temp2.search(html1)
            cond1_search = r_cond1.search(html1)

            if temp1_search:
                temp1 = temp1_search.group(0)
                temp1 = re.sub("\D", "", temp1)
                #print "Máxima "+temp1+"C"
            else:
                temp1 = "Not found"
                #print "no temp found"
       
            if temp2_search:
                temp2 = temp2_search.group(0)
                temp2 = re.sub("\D", "", temp2)
                #print "Mínima "+temp2+"C"
            else:
                temp2 = "No temp fond"
                #print "no temp2 found"
          
            if cond1_search:
                cond1 = cond1_search.group(0)
                cond1 = cond1[4:len(cond1)-8]
                if cond1 == "Cloudy":
                    cond = "Nublado"
                    #print "Nublado"
                elif cond1 == "Overcast and light rain":
                    cond = "Chuviscos"
                    #print "Chuviscos"
                elif cond1 == "Overcast and showers":
                    cond = "Aguaceiros"
                    #print "Aguaceiros"
                elif cond1 == "Cloudy and light rain":
                    cond = "Chuviscos"
                    #print "Chuviscos"
                elif cond1 == "Clear":
                    cond = "Ceu limpo"
                    #print "Céu limpo"
                elif cond1 == "Partly cloudy and showers":
                    cond = "Aguaceiros"
                    #print "Aguaceiros"
                elif cond1 == "Partly cloudy and light rain":
                    cond = "Chuva fraca"
                    #print "Chuva fraca"
                elif cond1 == "Overcast":
                    cond = "Nublado"
                    #print "Nublado"
                elif cond1 == "Partly cloudy, possible thunderstorms with rain":
                    cond = "Trovoada"
                    #print "Trovoada"
                elif cond1 == "Partly cloudy":
                    cond = "Parcialmente Nublado"
                    #print "Parcialmente Nublado"
                elif cond1 == "Mostly clear":
                    cond = "Ceu limpo"
                    #print "Céu limpo"
                elif cond1 == "Cloudy and showers":
                    cond = "Aguaceiros"
                    #print "Aguaceiros"
                elif cond1 == "Overcast, thunderstorms with rain":
                    cond = "Trovoada"
                    #print "Trovoada"
                else:
                    cond = cond1
                    #print cond1
            else:
                cond = "Not found"
                #print "no cond found"

            if y == 1:
                  cond_hoje = cond
                  tempmax_hoje = temp1
                  tempmin_hoje = temp2
            elif y == 2:
                  cond_ama = cond
                  tempmax_ama = temp1
                  tempmin_ama = temp2
            elif y == 3:
                  cond_depois = cond
                  tempmax_depois = temp1
                  tempmin_depois = temp2

            y +=1


        lcd_byte(LCD_LINE_1, LCD_CMD)
        lcd_string("Tempo",1)
        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string("Hoje",2)


        time.sleep(2) # 3 second delay

        lcd_byte(LCD_LINE_1, LCD_CMD)
        lcd_string("Min "+tempmin_hoje+"C"+" Max "+tempmax_hoje+"C",1)
        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string(cond_hoje,2)

        time.sleep(4)
        
        lcd_byte(LCD_LINE_1, LCD_CMD)
        lcd_string("Tempo",2)
        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string("%s" %(amanha),2)

        time.sleep(2)

        lcd_byte(LCD_LINE_1, LCD_CMD)
        lcd_string("Min "+tempmin_ama+"C"+" Max "+tempmax_ama+"C",1)
        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string(cond_ama,2)

        time.sleep(4)
        

        lcd_byte(LCD_LINE_1, LCD_CMD)
        lcd_string("Tempo",2)
        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string("%s" %(depois),2)

        time.sleep(2)

        
        lcd_byte(LCD_LINE_1, LCD_CMD)
        lcd_string("Min "+tempmin_depois+"C"+" Max "+tempmax_depois+"C",1)
        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string(cond_depois,2)


        time.sleep(4) # 3 second delay

      
      #time.sleep(3) # 3 second delay

      # Send some text
      #lcd_byte(LCD_LINE_1, LCD_CMD)
      #lcd_string("Raspberrypi-spy")
      #lcd_byte(LCD_LINE_2, LCD_CMD)
      #lcd_string(".co.uk")

      # time.sleep(20)

def lcd_init():
      # Initialise display
      lcd_byte(0x33,LCD_CMD)
      lcd_byte(0x32,LCD_CMD)
      lcd_byte(0x28,LCD_CMD)
      lcd_byte(0x0C,LCD_CMD) 
      lcd_byte(0x06,LCD_CMD)
      lcd_byte(0x01,LCD_CMD) 

def lcd_string(message):
      # Send string to display
      # style=1 Left justified
      # style=2 Centred
      # style=3 Right justified
  
      if style==1:
        message = message.ljust(LCD_WIDTH," ")  
      elif style==2:
        message = message.center(LCD_WIDTH," ")
      elif style==3:
        message = message.rjust(LCD_WIDTH," ")

      for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)

def lcd_byte(bits, mode):
      # Send byte to data pins
      # bits = data
      # mode = True  for character
      #        False for command

      GPIO.output(LCD_RS, mode) # RS

      # High bits
      GPIO.output(LCD_D4, False)
      GPIO.output(LCD_D5, False)
      GPIO.output(LCD_D6, False)
      GPIO.output(LCD_D7, False)
      if bits&0x10==0x10:
        GPIO.output(LCD_D4, True)
      if bits&0x20==0x20:
        GPIO.output(LCD_D5, True)
      if bits&0x40==0x40:
        GPIO.output(LCD_D6, True)
      if bits&0x80==0x80:
        GPIO.output(LCD_D7, True)

      # Toggle 'Enable' pin
      time.sleep(E_DELAY)   
      GPIO.output(LCD_E, True) 
      time.sleep(E_PULSE)
      GPIO.output(LCD_E, False) 
      time.sleep(E_DELAY)     

      # Low bits
      GPIO.output(LCD_D4, False)
      GPIO.output(LCD_D5, False)
      GPIO.output(LCD_D6, False)
      GPIO.output(LCD_D7, False)
      if bits&0x01==0x01:
        GPIO.output(LCD_D4, True)
      if bits&0x02==0x02:
        GPIO.output(LCD_D5, True)
      if bits&0x04==0x04:
        GPIO.output(LCD_D6, True)
      if bits&0x08==0x08:
        GPIO.output(LCD_D7, True)

      # Toggle 'Enable' pin
      time.sleep(E_DELAY)   
      GPIO.output(LCD_E, True) 
      time.sleep(E_PULSE)
      GPIO.output(LCD_E, False) 
      time.sleep(E_DELAY)   

if __name__ == '__main__':
      main()
