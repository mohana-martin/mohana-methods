import pandas as pd
import datetime as dt
from copy import deepcopy


def get_segments(filter_series, complete=True) -> list:
    """Get the start and end index of consecutive True's in a Pandas Series.

    Parameters
    ----------
    filter_series : pandas Series
        The pandas Series to retrieve the segments from.
    complete : bool, optional
        Only return full segments (segments which have a start and end within
        the context of the Pandas Series).
        Default True.

    Returns
    -------
    segments : list
        List of dictionaries with two keys "start" and "end", whose values correspond to the index of the Pandas Series.
    """
    # Convert the booleans to int and calculate the difference
    filter_series = filter_series.astype(int).diff()
    # Get all the indexes where a switch over between True and False happens
    points = filter_series.index[filter_series.isin([-1, 1])].tolist()
    # Initialize the segments list
    retlist = []
    # Run until there are no more points left
    while len(points) > 0:
        # If the point is False -> True (potential start)
        if filter_series[points[0]] == 1:
            # If there are no more points left
            if len(points) == 1:
                # then there is no end position
                if not complete:
                    # If not complete segments wanted, take the last point
                    retlist.append({"start": points.pop(0), "end": filter_series.index[-1]})
                else:
                    # If complete segments wanted, then ignore it.
                    points.pop(0)
            # otherwise, check if the next point is an end.
            elif filter_series[points[1]] == -1:
                retlist.append({"start": points.pop(0), "end": points.pop(0)})
        # If the point is True -> False (potential end)
        elif filter_series[points[0]] == -1:
            # Then this could only happen at the beginning
            if not complete:
                # If not complete segments wanted, take the first point
                retlist.append({"start": filter_series.index[0], "end": points.pop(0)})
            else:
                # If complete segments wanted, then ignore it.
                points.pop(0)
    return retlist


def get_delayed_segments(segments, delay) -> list:
    """Get the delayed start and end segments.
    
    This function takes a list of segments and checks whether their length is
    valid given the delays. The delays can be both negative and positive.
    Negative delay shift the start/end back in time with respect to the original boundary
    (start or end). This function does not check the validity of boundaries
    with respect to the original Pandas Series (e.g. a large delay could
    result in an ending time after the actual last point of the Pandas Series).

    Parameters
    ----------
    segments : list
        List of dictionary with two keys "start" and "end", whose values correspond to the index of the Pandas Series.
    delay : dict
        a dictionary with two keys: "end" and "start", containing a dictionary with the input
        arguments to dt.timedelta method or simply int or floats.
         e.g. {"start":{"minutes":30},"end":{"seconds":-5}} or {"start":30 ,"end":-5}}

    Returns
    -------
    filtered_segments : list
        List of dictionaries with two keys "start" and "end", whose values correspond to the index of the Pandas Series.
    """
    if type(delay["start"]) == dict and type(delay["end"]) == dict:

        delay["start"] = dt.timedelta(**delay["start"])
        delay["end"] = dt.timedelta(**delay["end"])

    filtered_segments = []
    for iSegment in segments:
        # take only the segments which are longer than the delay
        if iSegment["end"] - iSegment["start"] + delay["end"] > delay["start"]:
            filtered_segments.append(deepcopy(iSegment))
            filtered_segments[-1]["start"] += delay["start"]
            filtered_segments[-1]["end"] += delay["end"]
            # print(iSegment)
            # print(filtered_segments[-1])
    return filtered_segments


def get_combined_dataframe(dataframe, segments):
    """Get a dataframe filtered based on the list of time segments provided to it.

    Parameters
    ----------
    dataframe : pandas DataFrame
        DataFrame to filter based on the segments provided.
    segments : list
        List of dictionaries with two keys "start" and "end", whose values correspond to the index of the Pandas Series.

    Returns
    -------
    pandas DataFrame
        Filtered DataFrame
    """
    a = pd.IntervalIndex.from_tuples([tuple(i.values()) for i in segments]).get_indexer(dataframe.index)
    index_mask = pd.Series(a, index=dataframe.index) >= 0
    return dataframe[index_mask]


def get_delayed_filtered_dataframe(dataframe, filter_series, delay, complete=True):
    """Convenience function combining the complete functionality of getting segments

    Parameters
    ----------
    dataframe: pandas DataFrame
        see function get_combined_dataframe
    filter_series: pandas Series
        see function get_segments
    delay: dict
        see function get_delayed_segments
    complete: bool
        see get_segments

    Returns
    -------
    pandas DataFrame
        see function get_combined_dataframe
    """
    # print("filterSeries = {}".format(filterSeries))
    dfs = get_delayed_segments(get_segments(filter_series, complete), delay)
    # print("delayedfilterSeries = {}".format(filterSeries))
    return get_combined_dataframe(dataframe, dfs)
