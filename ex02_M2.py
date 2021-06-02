from aes_operations import *
from traces_operations import *
from Settings import *


def main():

    # CLI argument
    filename = "power_traces"

    # Read traces with specific amount
    traces = get_traces_from_file(filename)[:10000]

    # Traces length
    trace_length = len(traces[0]["leaks"])

    # Cast plaintext to bytes and save for each trace
    add_plainbytes_to_traces(traces)

    # Found key for each byte in the key
    found_key = 0

    # Found final key (16 bytes)
    final_key = ""

    # Foreach byte of the key's length
    for i in range(16):

        bytes_dict = {}

        # Foreach byte guess between 0-255
        for guessed_byte in range(256):

            hamming_vec = []

            # Foreach trace in the traces
            for trace in traces:
                current_byte = trace["plaintext_bytes"][i]

                # XOR operation
                xor_res = xor(guessed_byte, current_byte)

                # S-BOX operation
                s_box_res = s_box(xor_res)

                # Calculating the hamming weight
                res_hamming = calculate_hamming_weight(s_box_res)

                # Adding the HW to the vector
                hamming_vec.append(res_hamming)

            bytes_dict[guessed_byte] = hamming_vec

        # Holding max correlation
        max_corr = 0

        # Holding position in trace
        position_in_trace = 0

        # Foreach key byte between 0-255
        for key in bytes_dict.keys():

            # Foreach time slice of trace (64 points)
            for j in range(trace_length):

                # Getting traces sliced by time, column vector of size len(traces)
                time_fixed_vec = get_traces_sliced_by_time(traces, j)

                # Correlation between vectors
                corr = get_correlation(time_fixed_vec, bytes_dict[key])

                # Saving max correlation and key
                if corr > max_corr:
                    max_corr = corr
                    found_key = key
                    position_in_trace = j

        # Casting key to hex format
        key_hex = hex(found_key).replace("0x", "")

        # Adding zeros in case of 1-digit key
        if len(key_hex) == 1:
            key_hex = "0" + key_hex

        # Final key
        final_key = final_key + key_hex

        if is_print is True:
            print("Key index:", i, "Key found (byte):", found_key, "Key found (hex):", key_hex, "Correlataion:", max_corr, "Position in trace:", position_in_trace)
            print("Key so far:", final_key)
            print()

    if is_print is True:
        print("Final Key:", final_key)


if __name__ == "__main__":
    main()
