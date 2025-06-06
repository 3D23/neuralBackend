import numpy as np
import torch
from model import Actor
from models import ModelPredictData

dtype = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor
BUFFER_NORM_FACTOR = 10.0
S_INFO = 6
S_LEN = 8
M_IN_K = 1000.0

class AI():
    def __init__(self, file: str, bitrates, total_video_chunk: int):
        self.a_dim = len(bitrates)
        checkpoint_data = torch.load(file)
        self.model = Actor(6).type(dtype)
        self.model.load_state_dict(checkpoint_data['actor_model_state_dict'])
        self.model.eval()
        self.bitrates = bitrates
        self.total_video_chunk = total_video_chunk
        self.state = np.zeros((S_INFO, S_LEN))
        self.state = torch.from_numpy(self.state)
    

    def predict(self, data: ModelPredictData):
        self.state = np.roll(self.state, -1, axis=1)
        self.state[0, -1] = self.bitrates[data.bitrate] / float(np.max(self.bitrates))
        self.state[1, -1] = data.buffer_level / BUFFER_NORM_FACTOR
        self.state[2, -1] = float(data.video_chunk_size) / float(data.delay + 0.1) / M_IN_K
        self.state[3, -1] = float(data.delay) / M_IN_K / BUFFER_NORM_FACTOR
        self.state[4, :6] = np.array(data.next_video_chunk_sizes) / M_IN_K / M_IN_K
        self.state[5, -1] = np.minimum(data.video_chunk_remain, self.total_video_chunk) / float(self.total_video_chunk)
        self.state = torch.from_numpy(self.state)

        with torch.no_grad():
            prob = self.model(self.state.unsqueeze(0).type(dtype=dtype))
        action = prob.multinomial(num_samples=1).detach()
        bit_rate = int(action.squeeze().cpu().numpy())
        return bit_rate
