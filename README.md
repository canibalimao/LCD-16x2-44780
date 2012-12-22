LCD-16x2-44780
==============

Python scripts for 44780 LCD (Weather, clock, IP address) with Portuguese translation


Just run a script as "sudo" and you'll see the result on the screen.


To use the weather script with your location, do this:

1- Go here: http://aaltohtml5name.foreca.com/aaltohtml5-oct12a/search.php?q=XXXXXXXXXXXX and change the "XXXXXXXXXXXX" to the name of the desire town.
2- Copy the "id" of your location.
3- Go here: http://aaltohtml5name.foreca.com/aaltohtml5-oct12a/data.php?l=XXXXXXXXX&products=cc or here: http://aaltohtml5name.foreca.com/aaltohtml5-oct12a/data.php?l=XXXXXXXXX&products=cc,daily (according to the link you're changing on the code) and change the "XXXXXXXXX" to the code you copied before.
4- If you see the weather of you town you've done it right, so just copy that link and past it in the right place of the script.



IMPORTANT:
==========
Don't forget to confirm the GPIO pins you're using to your LCD and do the necessary changes on the code!





------------------------------ Copyright and Thanks ------------------------------

This is a compilation of various codes I had found on internet, and optimized to my needs thanks to many people on RaspberryPi's official forum, specially Texy (the LCD's seller) and gordon77 (wrote an essential part of the weather code for me).
