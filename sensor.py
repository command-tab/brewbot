#!/usr/bin/env python

import time
import math
import requests
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 1


# Read SPI data from MCP3008 chip, 8 possible ADCs (0 thru 7)
# https://gist.github.com/ladyada/3151375
# This method written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if (adcnum > 7) or (adcnum < 0):
        return -1
    GPIO.output(cspin, True)
    GPIO.output(clockpin, False)  # start clock low
    GPIO.output(cspin, False)  # bring CS low

    commandout = adcnum
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3  # we only need to send 5 bits here
    for i in range(5):
        if commandout & 0x80:
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)

    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if GPIO.input(misopin):
            adcout |= 0x1

    GPIO.output(cspin, True)

    adcout >>= 1  # first bit is 'null' so drop it
    return adcout


# This method adapted from https://openenergymonitor.org/forum-archive/node/3434.html
def sample_rms(ct_pin, spi_clk_pin, spi_mosi_pin, spi_miso_pin, spi_cs_pin):
    NUMBER_OF_SAMPLES = 1000
    SUPPLY_VOLTAGE = 3300
    ICAL = 60.6  # CT sensor ratio (30A/0.015A)*33 ohm burden = its calibration value
    # When 30A is flowing past the sensor, it will output 0.015 A
    sumI = 0
    sampleI = 512
    filteredI = 0
    for n in range(0, NUMBER_OF_SAMPLES):
        lastSampleI = sampleI
        sampleI = readadc(ct_pin, spi_clk_pin, spi_mosi_pin, spi_miso_pin, spi_cs_pin)
        lastFilteredI = filteredI
        filteredI = 0.996 * (lastFilteredI + sampleI - lastSampleI)
        sqI = filteredI * filteredI
        sumI += sqI
    I_RATIO = ICAL * ((SUPPLY_VOLTAGE / 1000.0) / 1023.0)
    Irms = I_RATIO * math.sqrt(sumI / NUMBER_OF_SAMPLES)
    sumI = 0
    return Irms

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler board
SPI_CLK_PIN = 18
SPI_MISO_PIN = 23
SPI_MOSI_PIN = 24
SPI_CS_PIN = 25

LED_PIN = 17

# set up the SPI interface pins
GPIO.setup(SPI_MOSI_PIN, GPIO.OUT)
GPIO.setup(SPI_MISO_PIN, GPIO.IN)
GPIO.setup(SPI_CLK_PIN, GPIO.OUT)
GPIO.setup(SPI_CS_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)

# CT sensor attached to ADC pin 0
ADC_CT_PIN = 0


def notify_slack():
    try:
        webhook_url = 'https://hooks.slack.com/services/...'
        requests.post(webhook_url, json={
            'text': 'Fresh pot brewing!',
            'channel': '#brewbot'
        })
    except:
        pass


def light(lit=True):
    if lit:
        GPIO.output(LED_PIN, GPIO.HIGH)
        return
    GPIO.output(LED_PIN, GPIO.LOW)

# How many positive readings do we want before notifying Slack?
THRESHOLD = 2
count = 0
while True:
    amperage = sample_rms(ADC_CT_PIN, SPI_CLK_PIN, SPI_MOSI_PIN, SPI_MISO_PIN, SPI_CS_PIN)
    if amperage > 7.0:
        light(lit=True)
        if count == THRESHOLD:
            count = 0
            notify_slack()
            time.sleep(14*60)
        else:
            count += 1
    else:
        count = 0
        light(lit=False)
    time.sleep(60)
