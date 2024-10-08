def normalize_coordinates(x_start, y_start, x_end, y_end):
    if x_start > x_end:
        x_start, x_end = x_end, x_start

    if y_start > y_end:
        y_start, y_end = y_end, y_start

    return x_start, y_start, x_end, y_end