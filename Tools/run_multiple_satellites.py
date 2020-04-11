#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import subprocess


def main():

    initial_states_table = pd.read_csv(filepath_or_buffer="Tools/sat_initial_states.csv", sep=",", header=None)
    initial_states = initial_states_table.values

    file_name = "InOut/SC_Simple_Multi.txt"
    num_sats = len(initial_states[0])

    for iSats in range(num_sats):
        pos_x_str = str(initial_states[0][iSats])
        pos_y_str = str(initial_states[1][iSats])
        pos_z_str = str(initial_states[2][iSats])
        position_str = pos_x_str + "  " + pos_y_str + "  " + pos_z_str + " !  Pos wrt Formation (m), expressed in F\n"

        vel_x_str = str(initial_states[3][iSats])
        vel_y_str = str(initial_states[4][iSats])
        vel_z_str = str(initial_states[5][iSats])
        velocity_str = vel_x_str + "  " + vel_y_str + "  " + vel_z_str + " !  Vel wrt Formation (m/s), expressed in F\n"

        file = open(file_name, "r")
        data_lines = file.readlines()
        file.close

        del data_lines[9]
        del data_lines[9]
        data_lines.insert(9, position_str)
        data_lines.insert(10, velocity_str)

        file = open(file_name, "w")
        data_lines = "".join(data_lines)
        file.write(data_lines)
        file.close()

        subprocess.call("./42")


if __name__ == '__main__':
    main()
