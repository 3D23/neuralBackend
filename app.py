import uuid
from fastapi import FastAPI, status
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from models import ModelPredictData, InitManifestData, AbrMetrics
from fastapi.concurrency import run_in_threadpool
from neural import AI
from prometheus_client import CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST, Gauge

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai : AI = None

registry = CollectorRegistry()

THROUGHPUT = Gauge('network_throughput', 'Текущая пропускная сопсобность сети', ['algorithm'], registry=registry)
QOE_SCORE = Gauge('qoe', 'QoE', ['algorithm'], registry=registry)
BUFFER_LEVEL = Gauge('buffer_level', "Уровеь буфера", ['algorithm'], registry=registry)
BITRATE = Gauge('bitrate', 'Выбранный битрейт', ['algorithm'], registry=registry)
REBUFFERING_TIME = Gauge('rebuffering_time', 'Время ребаферинга', ['algorithm'], registry=registry)


def set_metrics(metrics: AbrMetrics):
    THROUGHPUT.labels(algorithm=metrics.algorithm).set(metrics.throughput)
    QOE_SCORE.labels(algorithm=metrics.algorithm).set(metrics.qoe)
    BUFFER_LEVEL.labels(algorithm=metrics.algorithm).set(metrics.buffer_level)
    BITRATE.labels(algorithm=metrics.algorithm).set(metrics.bitrate)
    REBUFFERING_TIME.labels(algorithm=metrics.algorithm).set(metrics.rebuffering_time)


@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(registry),
        media_type=CONTENT_TYPE_LATEST
    )


@app.post('/update_metrics', status_code=status.HTTP_200_OK)
async def update_metrics(metrics: AbrMetrics):
    await run_in_threadpool(set_metrics, metrics)
    return {
        'info': 'metrics updated'
    }


# @app.get('/init_id')
# async def init_id():
#    return {
#            'uuid': uuid.uuid4()
#        }


@app.post('/predict')
async def predict(data: ModelPredictData):
    global ai
    bit_rate = ai.predict(data)
    return {'predicted': bit_rate}


@app.post('/init_manifest', status_code=status.HTTP_200_OK)
async def init_manifest(data: InitManifestData):
    global ai
    ai = AI(file='epoch_50000.pth', bitrates=data.bitrates, total_video_chunk=data.total_video_chunk)
    return {'info': 'manifest init success'}