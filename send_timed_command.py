import uhd
import numpy as np

def main():
    # create a USRP device
    usrp = uhd.usrp.MultiUSRP("addr=10.28.128.3")

    # set USRP clock source
    usrp.set_clock_source("internal")

    # set usrp realtime clock (to 0 for now)
    usrp.set_time_now(uhd.types.TimeSpec(0.0))

    # set the center frequency
    usrp.set_tx_freq(2.45e9)
    
    # create a simple sine wave signal
    samples = np.exp(1j * np.pi * np.arange(4000))

    # send the signal
    usrp.send_timed_command(samples, uhd.types.TimeSpec(2))


if __name__ == "__main__":
    main()
