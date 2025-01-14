import pandas as pd
import numpy as np
import os

from ..base import BaseRaw


class RawAWD(BaseRaw):
    r"""Raw object from .AWD file (recorded by ActiWatches)

    Parameters
    ----------
    input_fname: str
        Path to the AWD file.
    header_size: int
        Header size (i.e. number of lines) of the raw data file. Default is 7.
    frequency: str
        Data acquisition frequency.
        Cf. #timeseries-offset-aliases in
        <https://pandas.pydata.org/pandas-docs/stable/timeseries.html>.
        Default is '1T'.
    dtype: dtype
        The dtype of the raw data. Default is np.int.
    """

    def __init__(
        self,
        input_fname,
        header_size=7,
        frequency='1min',
        start_time=None,
        period=None,
        dtype=np.int
    ):

        # get absolute file path
        input_fname = os.path.abspath(input_fname)
        # [TO-DO] check if file exists
        # [TO-DO] check it is has the right file extension .awd

        # extract header and data size
        with open(input_fname) as f:
            header = [next(f) for x in range(header_size)]
            data = [line.split(' ')[0] for line in f]

        # extract informations from the header
        name = self.__extract_awd_name(header)
        uuid = self.__extract_awd_uuid(header)
        start = self.__extract_awd_start_time(header)

        index_data = pd.Series(
            data=data,
            index=pd.date_range(
                start=start,
                periods=len(data),
                freq='1min'
            ),
            dtype=np.int
        )

        if start_time is not None:
            start_time = pd.to_datetime(start_time)
        else:
            start_time = start

        if period is not None:
            period = pd.Timedelta(period)
            stop_time = start_time+period
        else:
            stop_time = index_data.index[-1]
            period = stop_time - start_time

        index_data = index_data[start_time:stop_time]

        # call __init__ function of the base class
        super().__init__(
            name=name,
            uuid=uuid,
            format='AWD',
            axial_mode='mono-axial',
            start_time=start_time,
            period=period,
            frequency=pd.Timedelta(frequency),
            data=index_data,
            light=None
        )

    def __extract_awd_name(self, header):
        return header[0].replace('\n', '')

    def __extract_awd_uuid(self, header):
        return header[5].replace('\n', '')

    def __extract_awd_start_time(self, header):
        return pd.to_datetime(header[1] + ' ' + header[2])


def read_raw_awd(
    input_fname,
    header_size=7,
    frequency='1min',
    start_time=None,
    period=None,
    dtype=np.int
):
    r"""Reader function for raw AWD file.

    Parameters
    ----------
    input_fname: str
        Path to the AWD file.
    header_size: int
        Header size (i.e. number of lines) of the raw data file. Default is 7.
    frequency: str
        Data acquisition frequency.
        Cf. #timeseries-offset-aliases in
        <https://pandas.pydata.org/pandas-docs/stable/timeseries.html>.
        Default is '1T'.
    start_time: str
        Default is None.
    period: str
        Default is None.
    dtype: dtype
        The dtype of the raw data. Default is np.int.

    Returns
    -------
    raw : Instance of RawAWD
        An object containing raw AWD data
    """

    return RawAWD(
        input_fname=input_fname,
        header_size=header_size,
        frequency=frequency,
        start_time=start_time,
        period=period,
        dtype=dtype
    )
