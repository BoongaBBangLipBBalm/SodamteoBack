import os
import pandas as pd
from Sodamteo import settings
from neuralforecast import NeuralForecast
import datetime
from .models import CropPricePredict


def price_prediction():
    data_df = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'Rice_Price_data.csv'))

    neural_df = data_df.melt(id_vars=['date'], var_name='unique_id', value_name='y')
    neural_df = neural_df.rename(columns={'date': 'ds'})
    neural_df['ds'] = pd.to_datetime(neural_df['ds'])

    horizon = 3

    saved_model = NeuralForecast.load(os.path.join(settings.MEDIA_ROOT, 'ckpt'))
    predict_insample = saved_model.predict_insample(step_size=horizon).reset_index()

    before = predict_insample[predict_insample['ds'] >= datetime.datetime(2024, 1, 1)]
    before = before[before['unique_id'] == 'price'][['ds', 'NHITS']]

    predict = saved_model.predict().reset_index()
    predict = predict[predict['unique_id'] == 'price'][['ds', 'NHITS']]
    predict = pd.concat([before, predict])
    predict.reset_index(drop=True, inplace=True)

    # 저장 코드 추가
    predicted_values = predict[-3:][['ds', 'NHITS']].to_dict('records')

    for entry in predicted_values:
        date = entry['ds'].date()  # 날짜 추출
        price = entry['NHITS']  # 예측 가격
        CropPricePredict.objects.update_or_create(
            crop='Rice',  # 고정된 작물명 사용, 필요에 따라 변경 가능
            date=date,
            defaults={'price': price}
        )
