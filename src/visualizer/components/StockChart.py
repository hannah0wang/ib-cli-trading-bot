import json
from streamlit_lightweight_charts import renderLightweightCharts
import pandas_ta as ta

class StockChart:

    @staticmethod
    def show_chart(df, symbol):
        COLOR_BULL = 'rgba(38,166,154,0.9)'  # #26a69a
        COLOR_BEAR = 'rgba(239,83,80,0.9)'  # #ef5350 

        df.rename(columns={'date': 'time'}, inplace=True)
        df['time'] = df['time'].astype('str')
        df.ta.sma(close='close', length=50, append=True)

        df = df.tail(200)

        candles = json.loads(df.to_json(orient='records'))
        volume = json.loads(df.rename(columns={'volume': 'value', }).to_json(orient='records'))
        sma = json.loads(df.rename(columns={'SMA_50': 'value', }).to_json(orient='records'))

        chartMultipaneOptions = [
            {
                "width": 1200,
                "height": 400,  
                "layout": {
                    "background": {  
                        "type": "solid",
                        "color": 'black'  
                    },
                    "textColor": "white"
                },
                "grid": {
                    "vertLines": {
                        "color": "rgba(197, 203, 206, 0.5)"
                    },
                    "horzLines": {
                        "color": "rgba(197, 203, 206, 0.5)"
                    }
                },
                "crosshair": {
                    "mode": 0 
                },
                "priceScale": {
                    "borderColor": "rgba(197, 203, 206, 0.8)"
                },
                "timeScale": {
                    "borderColor": "rgba(197, 203, 206, 0.8)",
                    "barSpacing": 15
                },
                "watermark": {
                    "visible": False,
                    "fontSize": 48,
                    "horzAlign": 'center',
                    "vertAlign": 'center',  
                    "color": 'white',
                    "text": symbol,
                }
            }
        ]

        seriesCandlestickChart = [
            {
                "type": 'Candlestick',
                "data": candles,
                "options": {
                    "upColor": COLOR_BULL,
                    "downColor": COLOR_BEAR,
                    "borderVisible": False
                }
            }
        ]

        seriesVolumeChart = [
            {
                "type": 'Histogram',
                "data": volume,
                "options": {
                    "priceFormat": {
                        "type": 'volume',
                    },
                    "priceScaleId": ""
                },
                "priceScale": {
                    "scaleMargins": {
                        "top": 0.7,
                        "bottom": 0,
                    },
                    "alignLabels": False
                }
            }
        ]

        renderLightweightCharts([
            {
                "chart": chartMultipaneOptions[0],
                "series": seriesCandlestickChart + seriesVolumeChart
            }
        ], f'multipane{symbol}')