from datetime import datetime, timedelta
import random

def curr5Env(farmID):
    falseSerializers = []
    start = datetime.now() - timedelta(hours=10)
    interval = timedelta(hours=2)
    for i in range(5):
        start += interval
        # rand = random.uniform(0, 5)

        falseData = {
            "farmID": farmID,
            "timestamp": start,
            "N": 79.89+random.uniform(-5, 5), "P": 47.58+random.uniform(0, 5), "K": 39.87+random.uniform(0, 5),
            "temperature": 23.689332+random.uniform(0, 5),
            "humidity": 82.272822+random.uniform(0, 5),
            "ph": 6.425471+random.uniform(0, 5),
            "rainfall": 236.181114+random.uniform(0, 5)
        }
        falseSerializers.append(falseData)

    return falseSerializers


def profileEnv(farmID):
    start = datetime.now()

    falseData = {
        "farmID": farmID,
        "timestamp": start,
        "N": 79.89 + random.uniform(-5, 5), "P": 47.58 + random.uniform(0, 5), "K": 39.87 + random.uniform(0, 5),
        "temperature": 23.689332 + random.uniform(0, 5),
        "humidity": 82.272822 + random.uniform(0, 5),
        "ph": 6.425471 + random.uniform(0, 5),
        "rainfall": 236.181114 + random.uniform(0, 5)
    }

    return falseData