import json
from datetime import datetime, timedelta
import random

from CropSelection.models import FarmEnvironment
from CropSelection.serializers import CurrEnvSerializer
from Farm.models import FarmProfile


def saveFalseData(farmID):
    start = datetime.now() - timedelta(hours=11)
    interval = timedelta(hours=2)

    farm = FarmProfile.objects.get(farmID=farmID)
    environmentList = []
    for i in range(5):
        start += interval
        environment = CurrEnvSerializer(FarmEnvironment.objects.create(
            farmID=farm,
            N=79.89+random.uniform(-5, 5),
            P=47.58+random.uniform(-5, 5),
            K=39.87+random.uniform(-5, 5),
            temperature=23.689332+random.uniform(-5, 5),
            humidity=82.272822+random.uniform(-5, 5),
            ph=6.425471+random.uniform(-5, 5),
            rainfall=236.181114+random.uniform(-5, 5)
        )).data

        environment['timestamp'] = start
        environmentList.append(environment)

    return environmentList
