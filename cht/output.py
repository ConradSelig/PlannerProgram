def print_table_data(CHT, w):

    # create the formatting string here, as it cannot be done in-place
    format_string = '{:>' + str(w) + '}'

    # if there is no data, output that
    if not CHT.raw_values:
        print('No data found.')
    # else data exists
    else:
        # for each column of data
        for col in CHT.keys:
            # output the header row
            print(format_string.format(col + ":"), end="")
        # output newline
        print("")
        # for each line of each event
        for row in CHT.raw_values:
            # for each column in that events data
            for col in row:
                # output with the same formatting as the header row
                if len(col) > w-5:
                    col = col[:w-5] + "..."
                print(format_string.format(col), end="")
            # output newline
            print("")
    return


def progress_bar(marks: int, total: int):
    print("Current Progress: " + str(marks) + " / " + str(total))
    print("[", end="")
    if total > 0:
        for mark in range(marks - 1):
            print("=", end="")
        if marks > 0 and marks != total:
            print(">", end="")
        elif marks == total:
            print("=", end="")
        for dot in range(total - marks):
            print(".", end="")
    print("]")
    return
