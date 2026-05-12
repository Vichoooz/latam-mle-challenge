from datetime import datetime


top_10_features = [
    "OPERA_Latin American Wings", 
    "MES_7",
    "MES_10",
    "OPERA_Grupo LATAM",
    "MES_12",
    "TIPOVUELO_I",
    "MES_4",
    "MES_11",
    "OPERA_Sky Airline",
    "OPERA_Copa Air"
]

def get_period_day(date):
    hour = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').hour
    if 5 <= hour < 12:
        return 'mañana'
    elif 12 <= hour < 19:
        return 'tarde'
    else:
        return 'noche'

def is_high_season(fecha):
    fecha_dt = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
    año = fecha_dt.year
    
    ranges = [
        (datetime(año, 12, 15), datetime(año, 12, 31)),
        (datetime(año, 1, 1), datetime(año, 3, 3)),
        (datetime(año, 7, 15), datetime(año, 7, 31)),
        (datetime(año, 9, 11), datetime(año, 9, 30)),
    ]
    
    return 1 if any(min_d <= fecha_dt <= max_d for min_d, max_d in ranges) else 0

    
def get_min_diff(data):
    fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
    fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
    min_diff = ((fecha_o - fecha_i).total_seconds())/60
    return min_diff

