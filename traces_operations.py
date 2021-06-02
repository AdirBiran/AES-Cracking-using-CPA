import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr


def plot_trace(vecs):
    """
    Plot the traces in the vecs list
    :param vecs: list of vectors
    """
    for vec in vecs:
        plt.plot([i+1 for i in range(len(vec))], vec, marker='o', color='red')
    plt.show()


def get_traces_from_file(filename):
    """
    Read traces from file
    :param filename: filename containing the traces
    :return: the traces as list
    """
    with open(filename, "r") as f:
        data = json.load(f)
        return data


def get_mean_trace(traces):
    """
    Calculate the mean trace of list
    :param traces: list of traces
    :return: mean trace
    """
    res_trace = []
    tmp_trace = []
    for i in range(len(traces[0]["leaks"])):
        for trace in traces:
            tmp_trace.append(trace["leaks"][i])

        res_trace.append(np.mean(tmp_trace))
        tmp_trace = []

    return res_trace


def add_plainbytes_to_traces(traces):
    """
    Add plaintext bytes to each trace
    :param traces: list of traces
    :return: updated list of traces
    """
    for j in range(len(traces)):
        trace = traces[j]
        plaintext = trace["plaintext"]
        plain_bytes = []
        for i in range(0, len(plaintext), 2):
            b = plaintext[i:i + 2]
            plain_bytes.append(b)

        plain_bytes_casted = [int(b, 16) for b in plain_bytes]
        traces[j]["plaintext_bytes"] = plain_bytes_casted


def get_traces_sliced_by_time(traces, point_of_time):
    """
    Slice the traces by time
    :param traces: traces to slice
    :param point_of_time: point where to slice
    :return: sliced array
    """
    res_trace = []

    for i in range(len(traces)):
        res_trace.append(traces[i]["leaks"][point_of_time])

    return res_trace


def get_correlation(vec_a, vec_b):
    """
    Calculate the correlataion between the two vectors
    :return: the correlataion
    """
    return pearsonr(vec_a, vec_b)[0]
