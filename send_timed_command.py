import uhd
import uhd.types
import numpy as np

def main():
    # create a USRP device
    usrp = uhd.usrp.MultiUSRP("addr=10.28.128.3")

    # set USRP clock source
    usrp.set_clock_source("internal")

    # set usrp realtime clock (to 0 for now)
    usrp.set_time_now(uhd.types.TimeSpec(0.0))

    # create a simple sine wave signal
    samples = np.exp(1j * np.pi * np.arange(4000))

    # some constants
    tx_duration = 10
    center_freq = 2.45e9
    sample_rate = 10e6
    channels = [0]
    tx_gain = 0
    tx_time = uhd.types.TimeSpec(2)

    # send the signal
    # UHD provides the send_waveform() function to transmit a batch of samples, an example is shown below. 
    # If you specify a duration (in seconds) longer than the provided signal, it will simply repeat it.
    usrp.send_waveform(samples, tx_duration, center_freq, sample_rate, channels, tx_gain, tx_time)


if __name__ == "__main__":
    main()
