#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import subprocess


def convert_nadirZ_to_zenithX(raw_vector):
    rot_mat = np.matrix([[0.0, 0.0, -1.0], [1.0, 0.0, 0.0], [0.0, -1.0, 0.0]])
    converted_vector = np.dot(rot_mat, raw_vector)
    return converted_vector


def convert_zenithX_to_nadirZ(raw_vector):
    rot_mat = np.matrix([[0.0, 1.0, 0.0], [0.0, 0.0, -1.0], [-1.0, 0.0, 0.0]])
    converted_vector = np.dot(rot_mat, raw_vector)
    return converted_vector


def main():

    initial_states_table = pd.read_csv(filepath_or_buffer="Tools/sat_initial_states.csv", sep=",", header=None)
    initial_states = initial_states_table.values

    file_name = "InOut/SC_Simple_Multi.txt"
    num_sats = len(initial_states[0])
    sat_states = pd.DataFrame(index=[], columns=[])

    for iSats in range(num_sats):
        position = np.array([initial_states[0][iSats], initial_states[1][iSats], initial_states[2][iSats]])
        position = convert_zenithX_to_nadirZ(position)
        pos_x_str = str(position[0, 0])
        pos_y_str = str(position[0, 1])
        pos_z_str = str(position[0, 2])
        position_str = pos_x_str + "  " + pos_y_str + "  " + pos_z_str + " !  Pos wrt Formation (m), expressed in F\n"

        velocity = np.array([initial_states[3][iSats], initial_states[4][iSats], initial_states[5][iSats]])
        velocity = convert_zenithX_to_nadirZ(velocity)
        vel_x_str = str(velocity[0, 0])
        vel_y_str = str(velocity[0, 1])
        vel_z_str = str(velocity[0, 2])
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

        pos_eh = pd.read_csv('InOut/PosEH.42', sep=" ", header=None)
        PX = 'SC-' + str(iSats) + '-px'
        PY = 'SC-' + str(iSats) + '-py'
        PZ = 'SC-' + str(iSats) + '-pz'
        pos_eh.columns = [PX, PY, PZ]

        for iData in range(len(pos_eh)):
            pos = np.array([pos_eh[PX][iData], pos_eh[PY][iData], pos_eh[PZ][iData]])
            pos_converted = convert_nadirZ_to_zenithX(pos)
            pos_eh[PX][iData] = pos_converted[0, 0]
            pos_eh[PY][iData] = pos_converted[0, 1]
            pos_eh[PZ][iData] = pos_converted[0, 2]

        vel_eh = pd.read_csv('InOut/VelEH.42', sep=" ", header=None)
        VX = 'SC-' + str(iSats) + '-vx'
        VY = 'SC-' + str(iSats) + '-vy'
        VZ = 'SC-' + str(iSats) + '-vz'
        vel_eh.columns = [VX, VY, VZ]
        state_eh = pd.concat([pos_eh, vel_eh], axis='columns')

        for iData in range(len(vel_eh)):
            vel = np.array([vel_eh[VX][iData], vel_eh[VY][iData], vel_eh[VZ][iData]])
            vel_converted = convert_nadirZ_to_zenithX(vel)
            vel_eh[VX][iData] = vel_converted[0, 0]
            vel_eh[VY][iData] = vel_converted[0, 1]
            vel_eh[VZ][iData] = vel_converted[0, 2]

        if sat_states.empty:
            sat_states = state_eh
        else:
            sat_states = pd.concat([sat_states, state_eh], axis='columns')

    inp_sim = open("InOut/Inp_Sim.txt", "r")
    inp_sim_lines = inp_sim.readlines()
    inp_sim.close()
    temp = inp_sim_lines[4].split()
    delta_time = float(temp[0])

    time_index = sat_states.index
    time_table = []
    for iTime in range(len(sat_states)):
        time = delta_time * float(time_index.values[iTime])
        time_table.append(time)
    sat_states.index = time_table
    print(sat_states)

    sat_states.to_csv('Tools/sat_states_lvlh.csv')


if __name__ == '__main__':
    main()
