#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.8.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import sip


def snipfcn_snippet_0(self):
    self.uhd_usrp_sink_1_0.set_time_source('_external_')
    self.uhd_usrp_source_0.set_time_source('_external_')
    self.uhd_usrp_sink_1_0.set_clock_source('external')
    self.uhd_usrp_source_0.set_clock_source('external')

    self.uhd_usrp_sink_1_0.set_time_next_pps(uhd.time_spec(0.0))
    self.uhd_usrp_source_0.set_time_next_pps(uhd.time_spec(0.0))

    time.sleep(2)

    nowtime = self.uhd_usrp_sink_1_0.get_time_now()
    self.uhd_usrp_sink_1_0.set_command_time(nowtime+uhd.time_spec(0.5))
    self.uhd_usrp_source_0.set_command_time(nowtime+uhd.time_spec(0.5))
    self.uhd_usrp_sink_1_0.set_center_freq(953e6, 0)
    self.uhd_usrp_sink_1_0.set_center_freq(955e6, 1)
    self.uhd_usrp_source_0.set_center_freq(955e6, 0)
    self.uhd_usrp_source_0.set_center_freq(953e6, 1)
    time.sleep(1)
    self.uhd_usrp_sink_1_0.clear_command_time()
    self.uhd_usrp_source_0.clear_command_time()

    now_time = self.uhd_usrp_sink_1_0.get_time_now()
    self.uhd_usrp_sink_1_0.set_command_time(nowtime+uhd.time_spec(0.5))
    self.uhd_usrp_source_0.set_command_time(nowtime+uhd.time_spec(0.5))

    self.uhd_usrp_sink_1_0.set_start_time(now_time+uhd.time_spec(3))
    self.uhd_usrp_source_0.set_start_time(now_time+uhd.time_spec(3))
    time.sleep(1)
    self.uhd_usrp_sink_1_0.clear_command_time()
    self.uhd_usrp_source_0.clear_command_time()
    print (uhd.time_spec_t.get_real_secs(now_time))


def snippets_main_after_init(tb):
    snipfcn_snippet_0(tb)

class LinToCirc(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "LinToCirc")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 5e6
        self.phase = phase = -80
        self.freq2 = freq2 = 955e6
        self.freq1 = freq1 = 953e6
        self.amp = amp = 1.9

        ##################################################
        # Blocks
        ##################################################

        self._phase_range = Range(-180, 180, 0.25, -80, 200)
        self._phase_win = RangeWidget(self._phase_range, self.set_phase, "Phase", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._phase_win)
        self._amp_range = Range(1.0, 2.1, 0.005, 1.9, 200)
        self._amp_win = RangeWidget(self._amp_range, self.set_amp, "Amplitude", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._amp_win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("addr0=192.168.68.253, addr1=192.168.68.254", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=[0,1],
            ),
        )
        self.uhd_usrp_source_0.set_clock_source('external', 0)
        self.uhd_usrp_source_0.set_time_source('external', 0)
        self.uhd_usrp_source_0.set_clock_source('external', 1)
        self.uhd_usrp_source_0.set_time_source('external', 1)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_source_0.set_center_freq(freq2, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_normalized_gain(1, 0)

        self.uhd_usrp_source_0.set_center_freq(freq1, 1)
        self.uhd_usrp_source_0.set_antenna("RX2", 1)
        self.uhd_usrp_source_0.set_normalized_gain(1, 1)
        self.uhd_usrp_sink_1_0 = uhd.usrp_sink(
            ",".join(("addr0=192.168.68.253, addr1=192.168.68.254", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=[0,1],
            ),
            "",
        )
        self.uhd_usrp_sink_1_0.set_clock_source('external', 0)
        self.uhd_usrp_sink_1_0.set_time_source('external', 0)
        self.uhd_usrp_sink_1_0.set_clock_source('external', 1)
        self.uhd_usrp_sink_1_0.set_time_source('external', 1)
        self.uhd_usrp_sink_1_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_1_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_1_0.set_center_freq(freq1, 0)
        self.uhd_usrp_sink_1_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_1_0.set_normalized_gain(0.5, 0)

        self.uhd_usrp_sink_1_0.set_center_freq(freq2, 1)
        self.uhd_usrp_sink_1_0.set_antenna("TX/RX", 1)
        self.uhd_usrp_sink_1_0.set_normalized_gain(0.5, 1)
        self.qtgui_sink_x_0_1_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            962e6, #fc
            samp_rate, #bw
            "E_V", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_1_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_1_0_win = sip.wrapinstance(self.qtgui_sink_x_0_1_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_1_0.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_0_1_0_win)
        self.qtgui_sink_x_0_1 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            960e6, #fc
            samp_rate, #bw
            "E_H", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_1.set_update_time(1.0/10)
        self._qtgui_sink_x_0_1_win = sip.wrapinstance(self.qtgui_sink_x_0_1.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_1.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_0_1_win)
        self.blocks_sub_xx_0_0 = blocks.sub_cc(1)
        self.blocks_sub_xx_0 = blocks.sub_cc(1)
        self.blocks_phase_shift_0_0_0 = blocks.phase_shift(phase, False)
        self.blocks_phase_shift_0_0 = blocks.phase_shift(90, False)
        self.blocks_phase_shift_0 = blocks.phase_shift(90, False)
        self.blocks_multiply_const_vxx_0_0_0_1 = blocks.multiply_const_cc(amp)
        self.blocks_multiply_const_vxx_0_0_0_0 = blocks.multiply_const_cc(0.7071067812)
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_cc(0.7071067812)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_cc(0.7071067812)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.7071067812)
        self.blocks_add_xx_0_0 = blocks.add_vcc(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 2.0e6, (50e-3), 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 2.2e6, (50e-3), 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_phase_shift_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_add_xx_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.uhd_usrp_sink_1_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.uhd_usrp_sink_1_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.qtgui_sink_x_0_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0, 0), (self.qtgui_sink_x_0_1_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0_1, 0), (self.blocks_add_xx_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0_1, 0), (self.blocks_sub_xx_0_0, 0))
        self.connect((self.blocks_phase_shift_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_phase_shift_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_phase_shift_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0_0, 0))
        self.connect((self.blocks_phase_shift_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0_1, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_sub_xx_0_0, 0), (self.blocks_phase_shift_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.uhd_usrp_source_0, 1), (self.blocks_phase_shift_0_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_sub_xx_0_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "LinToCirc")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.qtgui_sink_x_0_1.set_frequency_range(960e6, self.samp_rate)
        self.qtgui_sink_x_0_1_0.set_frequency_range(962e6, self.samp_rate)
        self.uhd_usrp_sink_1_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_phase(self):
        return self.phase

    def set_phase(self, phase):
        self.phase = phase
        self.blocks_phase_shift_0_0_0.set_shift(self.phase)

    def get_freq2(self):
        return self.freq2

    def set_freq2(self, freq2):
        self.freq2 = freq2
        self.uhd_usrp_sink_1_0.set_center_freq(self.freq2, 1)
        self.uhd_usrp_source_0.set_center_freq(self.freq2, 0)

    def get_freq1(self):
        return self.freq1

    def set_freq1(self, freq1):
        self.freq1 = freq1
        self.uhd_usrp_sink_1_0.set_center_freq(self.freq1, 0)
        self.uhd_usrp_source_0.set_center_freq(self.freq1, 1)

    def get_amp(self):
        return self.amp

    def set_amp(self, amp):
        self.amp = amp
        self.blocks_multiply_const_vxx_0_0_0_1.set_k(self.amp)




def main(top_block_cls=LinToCirc, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    snippets_main_after_init(tb)
    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
