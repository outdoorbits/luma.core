# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

import luma.core.error


__all__ = ["rpi_gpio", "spidev"]


try:  # pragma: no cover
    from gpiozero import OutputDevice
except RuntimeError as e:
    if str(e) in ['This module can only be run on a Raspberry Pi!', 'Module not imported correctly!']:
        raise luma.core.error.UnsupportedPlatform('gpiozero access not available')

class PinOutputDevice(OutputDevice):
    HIGH    = True
    LOW        = False

    def set_status(self, new_status):
        if new_status:
            self.on()
        else:
            self.off()

def __spidev__(self):  # pragma: no cover
    # spidev cant compile on macOS, so use a similar technique to
    # initialize (mainly so the tests run unhindered)
    import spidev
    return spidev.SpiDev()


def __rpi_gpio__(self):
    # RPi.GPIO _really_ doesn't like being run on anything other than
    # a Raspberry Pi... this is imported here so we can swap out the
    # implementation for a mock
    return PinOutputDevice


def rpi_gpio(Class):
    setattr(Class, __rpi_gpio__.__name__, __rpi_gpio__)
    return Class


def spidev(Class):
    setattr(Class, __spidev__.__name__, __spidev__)
    return Class
