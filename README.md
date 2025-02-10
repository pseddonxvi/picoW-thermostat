# picoW-thermostat

Based off picoW-basics repository: https://github.com/lurbano/picoW-basics

Note: Setting up to save data file (circuitpython) (the boot.py file)
* https://learn.adafruit.com/cpu-temperature-logging-with-circuit-python?view=all

# Fork info

This fork adds upgrades to the hardware design. It includes a new laser-cut box design that moves the RPi Pico W to the center. It also has cutouts for two 3.5mm aux jacks that allow for different sensor modules to be plugged in to both 3V and 5V. The /design-files folder has .svg and .cdr files for laser cutting on 1/4in thick wood, along with refernce images for assembly.

## Wiring

On the sensor cable, ground is wired to the sleeve, GPIO is wired to the ring, and 3v/5v power is wired to the tip of the audio jack. The respective resistor for that sensor (in this case a DS18B20 and 4.7kΩ) is soldered directly onto the pins of the audio jack so it can be hidden inside of the strain-relief casing of the jack.
![DS18B20 Headphone Jack Wiring](https://github.com/user-attachments/assets/91c090f0-49b4-48bf-a0cd-37d84b9f4ae4)

The sensor box has two aux ports, the left one in the image below is wired for 5V and the right for 3V. The 5V jack runs to GP22 and the 3V jack runs to GP27. Both jacks are wired so that ground is on the sleeve, GPIO is on the ring, and 3v/5v power goes to the tip, just like the sensor cable above.
![Pico Sensor Box Wiring](https://github.com/user-attachments/assets/c18a5a3e-8525-438f-a569-dfc9990ae887)
