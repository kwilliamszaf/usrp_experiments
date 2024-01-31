import threading
import uhd
import uhd.types
import numpy as np

def receive_thread(usrp):
    while True:
        # Receive samples from the USRP
        samples = usrp.receive_samples(1000)

        # Process the received samples
        # ...

def main():
    # create a USRP device
    usrp = uhd.usrp.MultiUSRP("addr=10.28.128.3")

    # set USRP clock source
    usrp.set_clock_source("internal")

    # set usrp realtime clock (to 0 for now)
    usrp.set_time_now(uhd.types.TimeSpec(0.0))

    # Start the receive thread
    receive_thread = threading.Thread(target=receive_thread, args=(usrp,))
    receive_thread.start()

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
    usrp.send_waveform(samples, tx_duration, center_freq, sample_rate, channels, tx_gain, tx_time)


if __name__ == "__main__":
    main()
