#!/usr/bin/env python
# -*- coding: utf-8 -*-


def main():

    file_name = "../InOut/SC_Simple_Multi.txt"

    pos_x_str = "0.0"
    pos_y_str = "0.0"
    pos_z_str = "0.0"
    position_str = pos_x_str + "  " + pos_y_str + "  " + pos_z_str + " !  Pos wrt Formation (m), expressed in F\n"

    vel_x_str = "0.0"
    vel_y_str = "0.0"
    vel_z_str = "0.0"
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


if __name__ == '__main__':
    main()
