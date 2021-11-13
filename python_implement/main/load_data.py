# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 23:03:29 2021

@author: youle
"""
import pathlib
import numpy as np

def load_HV_log(parent_path):

    p = pathlib.Path(parent_path)
    dirs = p.glob("*design/")

    all_hv_data = {}
    median_hv_data = {}

    for d in dirs:

        hv_files = d.glob("HyperVolume_log*.csv")

        key = str(d.name).split("_")[-1]
        all_hv_data[key] = np.vstack([np.loadtxt(hp, delimiter = ",") for hp in hv_files])
        median_hv_data[key] = np.loadtxt(str(*d.glob("all_HyperVolume_log.csv")), delimiter = ",")

    return all_hv_data, median_hv_data

def load_IGD_log(parent_path):

    p = pathlib.Path(parent_path)
    dirs = p.glob("*design/")

    all_igd_data = {}
    median_igd_data = {}

    for d in dirs:

        igd_files = d.glob("IGD_log*.csv")

        key = str(d.name).split("_")[-1]
        all_igd_data[key] = np.vstack([np.loadtxt(ip, delimiter = ",") for ip in igd_files])

        median_igd_data[key] = np.loadtxt(str(*d.glob("all_IGD_log.csv")), delimiter = ",")

    return all_igd_data, median_igd_data

def load_normalized_IGD_log(parent_path):

    p = pathlib.Path(parent_path)
    dirs = p.glob("*design/")

    all_igd_data = {}
    median_igd_data = {}

    for d in dirs:

        igd_files = d.glob("normalized_IGD_log*.csv")

        key = str(d.name).split("_")[-1]
        all_igd_data[key] = np.vstack([np.loadtxt(ip, delimiter = ",") for ip in igd_files])

        median_igd_data[key] = np.loadtxt(str(*d.glob("all_normalized_IGD_log.csv")), delimiter = ",")
        
    return all_igd_data, median_igd_data