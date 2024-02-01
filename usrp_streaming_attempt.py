# A non-working attempt to get two USRP N210s to stream data to each other synchronously
# I ran out of time to play around with this code properly using the N210s

import threading
import time
import uhd
import uhd.types
import uhd.usrp
import numpy as np 
from matplotlib import pyplot as plt

def receive_thread(usrp1,usrp2,t):

    print("Starting rx thread...")

    # create receive thread
    usrp1_rx_stream = usrp1.get_rx_stream(uhd.stream_args("fc32"))
    usrp2_rx_stream = usrp2.get_rx_stream(uhd.stream_args("fc32"))
    
    # the metadata is useful for including timestamps...haven't quite figured that out yet
    
    usrp1_rx_metadata = uhd.types.RxMetadata()
    usrp2_rx_metadata = uhd.types.RxMetadata()
    
    usrp1_received_samples = np.empty(len(t), dtype=np.complex64)
    usrp2_received_samples = np.empty(len(t), dtype=np.complex64)
    usrp1_rx_stream.recv(usrp1_received_samples, metadata=usrp1_rx_metadata)
    usrp2_rx_stream.recv(usrp2_received_samples, metadata=usrp2_rx_metadata)
    
        # Process the received samples
    plt.plot(usrp1_rx_stream)
    plt.plot(usrp2_rx_stream)
        

def main(usrp1,usrp2):

    # set USRP clock and PPS
    usrp1.set_clock_source("external")
    usrp1.set_time_source("external")
    usrp2.set_clock_source("external")
    usrp2.set_time_source("external")

    # set usrp realtime clock to zero at next PPS signal
    usrp1.set_time_unknown_pps(uhd.types.TimeSpec(0.0))
    usrp2.set_time_unknown_pps(uhd.types.TimeSpec(0.0))
    time.sleep(1)
    
    # set usrp parameters using timed commands to ensure synchronisation
    center_freq = 950e6
    sample_rate = 5e6
    duration = 5
    amplitude = 0.05
    tx_gain = 10
    rx_gain = 10
    channel = 0
    
    now_time = usrp1.get_time_now()
    
    usrp1.set_command_time(now_time+uhd.types.TimeSpec(0.5))
    usrp2.set_command_time(now_time+uhd.types.TimeSpec(0.5))
    
    usrp1.set_tx_rate(sample_rate, channel)
    usrp1.set_rx_rate(sample_rate, channel)
    usrp1.set_tx_freq(center_freq, channel)
    usrp1.set_rx_freq(center_freq, channel)
    usrp1.set_tx_gain(tx_gain, channel)
    usrp1.set_rx_gain(rx_gain, channel)
    
    usrp2.set_tx_rate(sample_rate, channel)
    usrp2.set_rx_rate(sample_rate, channel)
    usrp2.set_tx_freq(center_freq, channel)
    usrp2.set_rx_freq(center_freq, channel)
    usrp2.set_tx_gain(tx_gain, channel)
    usrp2.set_rx_gain(rx_gain, channel)
    
    time.sleep(1)
    
    usrp1.clear_command_time()
    usrp2.clear_command_time()
    
    # create a simple sine wave signal
    t = np.arange(0, duration, 1/sample_rate)
    samples = amplitude*np.exp(1j * np.pi * t)
    
    # start receive thread
    
    receive_thread = threading.Thread(target=receive_thread, args=(usrp1,usrp2,t))
    receive_thread.start()
    
    # create streaming sources
    
    usrp1_tx_stream = usrp1.get_tx_stream(uhd.stream_args("fc32"))
    usrp2_tx_stream = usrp1.get_tx_stream(uhd.stream_args("fc32"))
    
    # the metadata is useful for including timestamps...haven't quite figured that out yet
    
    usrp1_tx_metadata = uhd.types.TxMetadata()
    usrp2_tx_metadata = uhd.types.TxMetadata()
    
    
    # stream samples
    
    usrp1_tx_stream.send(samples, metadata=usrp1_tx_metadata)
    usrp2_tx_stream.send(samples, metadata=usrp2_tx_metadata)

    usrp1.close()
    usrp2.close()


if __name__ == "__main__":

    # create a USRP device
    usrp1 = uhd.usrp.MultiUSRP("addr = 192.168.68.253")
    usrp2 = uhd.usrp.MultiUSRP("addr = 192.168.68.254")

    main(usrp1,usrp2)
