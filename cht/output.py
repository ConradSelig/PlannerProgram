def print_table_data(headers, values, w):

    # create the formatting string here, as it cannot be done in-place
    format_string = '{:>' + str(w) + '}'

    # if there is no data, output that
    if not values:
        print('No data found.')
    # else data exists
    else:
        # for each column of data
        for col in headers:
            # output the header row
            print(format_string.format(col + ":"), end="")
        # output newline
        print("")
        # for each line of each event
        for row in values:
            # for each column in that events data
            for col in row:
                # output with the same formatting as the header row
                print(format_string.format(col), end="")
            # output newline
            print("")
    return
