# brewbot

A coffee brewing Slack notification system using a non-invasive current sensor and Raspberry Pi. The setup watches energy consumption and waits for a rise in current draw above 7A, followed by several minutes of sustained usage. Once the time threshold has passed, it does an HTTP POST to a Slack webhook, sleeps for about 15 minutes, then starts monitoring again.

![ADC board and Raspberry Pi](https://raw.githubusercontent.com/commandtab/brewbot/master/images/full_kit.jpg)

![Boards mounted inside enclosure](https://raw.githubusercontent.com/commandtab/brewbot/master/images/box.jpg)

![ADC board front and back](https://raw.githubusercontent.com/commandtab/brewbot/master/images/adc_board_front_and_back.jpg)

## Parts List

* [MCP3008 8-Channel 10-Bit Analog to Digital Converter](http://www.adafruit.com/products/856)
* [Raspberry Pi model B](http://www.adafruit.com/products/998)
* [16-pin IC socket](http://www.adafruit.com/products/2203)
* [Assortment of heat shrink tubing](http://www.adafruit.com/products/344)
* [Panel mount to Micro USB adapter](http://www.adafruit.com/products/937)
* [10KΩ 1/4W LED resistor](https://www.sparkfun.com/products/11508)
* [Half-size Perma-Proto Raspberry Pi Breadboard PCB Kit](http://www.adafruit.com/products/1148)
* [5mm Yellow LED](https://www.sparkfun.com/products/9594)
* 1/8" panel mount audio jack
* 10uF electrolytic decoupling capacitor
* 33Ω 1/2W burden resistor
* 2x 470KΩ 1/2W voltage divider resistors
* [30A non-invasive current sensor](https://www.sparkfun.com/products/11005)
* [22 AWG Solid Core Hook Up Wire](https://www.sparkfun.com/products/11367)
* 5x7 photo box, from The Container Store
* [8 GB Class 10 SDHC card](http://www.amazon.com/gp/product/B00B588HY2)
* [Edimax EW-7811Un Wireless Nano USB Adapter](http://www.amazon.com/dp/B005CLMJLU)
* 6x Nylon screws washers and nuts
* [8" AC Cord Clips](http://www.acehardware.com/product/index.jsp?productId=29313236)
* [HDMI to Mini HDMI adapter](http://www.monoprice.com/Product?c_id=104&cp_id=10419&cs_id=1041909&p_id=3654&seq=1&format=2)
* [6' Mini HDMI to HDMI Cable](http://www.monoprice.com/Product?c_id=102&cp_id=10242&cs_id=1024201&p_id=3645&seq=1&format=2)
* [10' USB A Male to B Male Cable](http://www.monoprice.com/Product?p_id=8617)

## Connections

While I don't have a schematic handy, the gist of the connections is running the CT sensor to an analog input on the MCP3008 chip (See: [How to build an Arduino energy monitor](https://openenergymonitor.org/forum-archive/node/58.html)), then wiring the digital SPI output of the MCP3008 to Raspberry Pi GPIO pins. Adafruit has a [guide on connecting the MCP3008 to a Raspberry Pi](https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008) that was useful.
