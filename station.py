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
import os
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

"""#Radios
RFM = 'http://7779.live.streamtheworld.com:3690/RFM_SC'
RFM_Anos80 = 'http://7749.live.streamtheworld.com:3690/GR80SRFM_SC'
RFM_Oceano = 'http://7719.live.streamtheworld.com:3690/OCEANPACIFIC_SC'
Festival = 'mms://stream.radio.com.pt/roli-enc-520'
Antena1 = 'mms://rdp.oninet.pt/antena1'
CidadeFM = 'mms://195.23.102.196/cidadecbr96'
M80 = 'mms://195.23.102.196/m80cbr96'
NovaEra = 'mms://stream.radio.com.pt/roli-enc-478'
Comercial = 'mms://195.23.102.196/comercialcbr96'"""


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
      weatherURL1 = "http://aaltohtml5name.foreca.com/aaltohtml5-oct12a/data.php?l=102735943&products=cc"

      #IP Address
      ipaddr = urllib2.urlopen("http://automation.whatismyip.com/n09230945.asp").read()

      while True:

        today = datetime.now().strftime('%a')
        month = datetime.now().strftime('%b')

        if today == "Mon":
  	hoj = "Seg"
	elif today == "Tue":
		hoj = "Ter"
	elif today == "Wed":
		hoj = "Qua"
	elif today == "Thu":
		hoj = "Qui"
	elif today == "Fri":
		hoj = "Sex"
	elif today == "Sat":
		hoj = "Sab"
	elif today == "Sun":
		hoj = "Dom"

	if month == "Dec":
	    mes = "Dez"
	elif month == "Jan":
    	    mes = "Jan"
	elif month == "Feb":
    	    mes = "Fev"
	elif month == "Mar":
            mes = "Mar"
	elif month == "Apr":
   	    mes = "Abr"
	elif month == "May":
	    mes = "Mai"
	elif month == "Jun":
	    mes = "Jun"
	elif month == "Jul":
	    mes = "Jul"
	elif month == "Aug":
	    mes = "Ago"
	elif month == "Sep":
   	    mes = "Set"
	elif month == "Oct":
	    mes = "Out"
	elif month == "Nov":
	    mes = "Nov"

        start_time = time.time()
        elapsed_time = time.time() - start_time
        while ( elapsed_time < 3 ):
        # Send some test
              lcd_byte(LCD_LINE_1, LCD_CMD)
              lcd_string(datetime.now().strftime('  %H : %M : %S '),1)
              lcd_byte(LCD_LINE_2, LCD_CMD)
              lcd_string(hoj+datetime.now().strftime(' %d ')+mes+datetime.now().strftime(' %Y'),1)

              elapsed_time = time.time() - start_time

              
        lcd_byte(LCD_LINE_1, LCD_CMD)
        lcd_string("IP Address",2)
        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string(ipaddr,2)


        time.sleep(3)
        
        f = os.popen("mpc current")

        if f == " ":
          estacao = "Idle"

        else:

          station = ""
          for i in f.readlines():
            station += i


          if station == 'http://7779.live.streamtheworld.com:3690/RFM_SC\n':
	    estacao = 'RFM'
	 
	  elif station == 'http://7749.live.streamtheworld.com:3690/GR80SRFM_SC\n':
	    estacao = 'RFM Anos 80'

          elif station == 'http://7719.live.streamtheworld.com:3690/OCEANPACIFIC_SC\n':
	    estacao = 'RFM Oceano Pacifico'

	  elif station == 'mms://stream.radio.com.pt/roli-enc-520\n':
	    estacao = 'Festival'

	  elif station == 'mms://rdp.oninet.pt/antena1\n':
	    estacao = 'Antena 1'

	  elif station == 'mms://195.23.102.196/cidadecbr96\n':
	    estacao = 'CidadeFM'

	  elif station == 'mms://195.23.102.196/m80cbr96\n':
	    estacao = 'M80'
	
	  elif station == 'mms://stream.radio.com.pt/roli-enc-478\n':
	    estacao = 'Nova Era'

	  elif station == 'mms://195.23.102.196/comercialcbr96\n':
	    estacao = 'Comercial'

          elif station == 'http://7709.live.streamtheworld.com:3690/RADIO_RENASCENCA_SC?.wma':
            estacao = 'RR'

	 
	  elif station == "" :
	    estacao = 'Desligado'

          else:
            estacao = station

        #print station, "-> station"
        #print estacao, "-> estacao"

        lcd_byte(LCD_LINE_1, LCD_CMD)
        lcd_string("Radio",2)
        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string(estacao,2)

        time.sleep(3) # 3 second delay


        response1 = urllib2.urlopen(weatherURL1)
        html1 = response1.read()


        r_temp = re.compile("tf=\"[0-9]{1,3}\"")
        r_cond = re.compile("sT=\"[\D\W]{1,40}\"")
   
        temp_search = r_temp.search(html1)
        cond_search = r_cond.search(html1)


        if temp_search:
            temp = temp_search.group(0)
            temp = re.sub("\D", "", temp)
          
        else:
            temp = "no result"

        if cond_search:
            cond = cond_search.group(0)
            cond = cond[4:len(cond)-1]
            if cond == "Cloudy":
                ceu = "Nublado"
            elif cond == "Overcast and light rain":
                ceu = "Chuviscos"
            elif cond == "Overcast and rain":
                ceu = "Chuva"
            elif cond == "Overcast and showers":
                ceu = "Aguaceiros"
            elif cond == "Cloudy and light rain":
                ceu = "Chuviscos"
            elif cond == "Clear":
                ceu = "Ceu limpo"
            elif cond == "Partly cloudy and showers":
                ceu = "Aguaceiros"
            elif cond == "Partly cloudy and light rain":
                ceu = "Chuva fraca"
            elif cond == "Overcast":
                ceu = "Nublado"
            elif cond == "Partly cloudy, possible thunderstorms with rain":
                ceu = "Trovoada"
            elif cond == "Partly cloudy":
                ceu = "Parcialmente Nublado"
            elif cond == "Mostly clear":
                ceu = "Bom"
            elif cond == "Cloudy and showers":
                ceu = "Aguaceiros"
            elif cond == "Overcast, thunderstorms with rain":
                ceu = "Trovoada"

            else:
                ceu = cond

        else:
            ceu = "no result"

        lcd_byte(LCD_LINE_1, LCD_CMD)
        lcd_string("Tempo Agora",2)
        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string(temp+".C "+ceu,2)

        


      #time.sleep(3) # 3 second delay

      # Send some text
      #lcd_byte(LCD_LINE_1, LCD_CMD)
      #lcd_string("Raspberrypi-spy")
      #lcd_byte(LCD_LINE_2, LCD_CMD)
      #lcd_string(".co.uk")

        time.sleep(4)

def lcd_init():
      # Initialise display
      lcd_byte(0x33,LCD_CMD)
      lcd_byte(0x32,LCD_CMD)
      lcd_byte(0x28,LCD_CMD)
      lcd_byte(0x0C,LCD_CMD) 
      lcd_byte(0x06,LCD_CMD)
      lcd_byte(0x01,LCD_CMD) 

def lcd_string(message,style):
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

