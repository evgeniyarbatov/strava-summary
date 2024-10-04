import gpxpy

import pandas as pd

from geopy.distance import geodesic
  
def get_distance(row1, row2):
    return geodesic((row1['lat'], row1['lon']), (row2['lat'], row2['lon'])).meters

def get_gpx_info(filepath):
    gpx_file = open(filepath, 'r')
    gpx = gpxpy.parse(gpx_file)

    data = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                data.append({
                  'time': point.time,
                  'type': track.type,
                  'lat': point.latitude, 
                  'lon': point.longitude,
                  'elevation': point.elevation,
                })

    df = pd.DataFrame(data)
    if df is None or df.empty:
        return None
    
    df['distance_to_next'] = df.shift().apply(
        lambda row: get_distance(row, df.loc[row.name]) if row.name > 0 else 0, axis=1
    )
    distance = df['distance_to_next'].sum()
    
    df['time'] = pd.to_datetime(df['time'])
    df['time_str'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    df['duration'] = df['time'].diff().dt.total_seconds()
    duration = df['duration'].dropna().sum()
    
    try:
        df['elevation_diff'] = df['elevation'].diff()
        elevation_gain = df['elevation_diff'].where(df['elevation_diff'] > 0, 0).sum()
    except TypeError:
        elevation_gain = None
    
    return (
        df.iloc[0]['time_str'],
        df.iloc[0]['type'],
        duration,
        distance,
        elevation_gain,
    )