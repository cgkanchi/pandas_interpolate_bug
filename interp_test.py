import numpy
import pandas
from matplotlib import pyplot
import scipy.interpolate

def pandas_interpolate(df, interp_column, method='cubic'):
    df = df.set_index(interp_column)
    df = df.reindex(numpy.arange(df.index.min(), df.index.max(), 0.0005))
    df = df.interpolate(method=method)
    df = df.reset_index()
    df = df.rename(columns={'index': interp_column})
    return df

def scipy_interpolate(df, interp_column, method='cubic'):
    series = {}
    new_x = numpy.arange(df[interp_column].min(), df[interp_column].max(), 0.0005)

    for column in df:
        if column == interp_column: 
            series[column] = new_x
        else:
            interp_f = scipy.interpolate.interp1d(df[interp_column], df[column], kind=method)
            series[column] = interp_f(new_x)

    return pandas.DataFrame(series)


if __name__ == '__main__':
    df = pandas.read_csv('interp_test.csv')
    pd_interp = pandas_interpolate(df, 'distance_km', 'cubic')
    scipy_interp = scipy_interpolate(df, 'distance_km', 'cubic')

    #pyplot.plot(df['lon'], df['lat'], label='raw data')
    pyplot.plot(pd_interp['lon'], pd_interp['lat'], label='pandas')
    pyplot.plot(scipy_interp['lon'], scipy_interp['lat'], label='scipy interp1d')
    pyplot.legend(loc='best')

    pyplot.figure()
    df2 = pandas.DataFrame({'x': numpy.arange(10), 'sin(x)': numpy.sin(numpy.arange(10))})
    pd_interp2 = pandas_interpolate(df2, 'x', 'cubic')
    scipy_interp2 = scipy_interpolate(df2, 'x', 'cubic')
    pyplot.plot(pd_interp2['x'], pd_interp2['sin(x)'], label='pandas')
    pyplot.plot(scipy_interp2['x'], scipy_interp2['sin(x)'], label='scipy interp1d')
    pyplot.legend(loc='best')

    pyplot.show()





    

