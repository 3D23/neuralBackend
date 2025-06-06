from pydantic import BaseModel

class ModelPredictData(BaseModel):
    bitrate: int # quality number
    buffer_level: float # seconds
    video_chunk_size: int # byte
    delay: int # milliseconds
    next_video_chunk_sizes: list # bytes
    video_chunk_remain: int # points

class InitManifestData(BaseModel):
    bitrates: list
    total_video_chunk: int


class AbrMetrics(BaseModel):
    algorithm: str
    qoe: float
    throughput: float
    buffer_level: float
    bitrate: float
    rebuffering_time: float