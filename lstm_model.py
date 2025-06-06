import torch
import torch.nn as nn


class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LSTM, self).__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.attention = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.Tanh()
        )
        self.attention_combine = nn.Linear(hidden_size * 2, hidden_size)
        self.out = nn.Linear(hidden_size, output_size)


    def attention_forward(self, lstm_output, hidden):
        hidden_transformed = self.attention(hidden)
        hidden_transformed = hidden_transformed.unsqueeze(2) 
        attn_weights = torch.bmm(lstm_output, hidden_transformed)
        attn_weights = torch.softmax(attn_weights.squeeze(2), dim=1)
        attn_applied = torch.bmm(attn_weights.unsqueeze(1), lstm_output)
        return attn_applied.squeeze(1)


    def forward(self, x):
        lstm_out, (hidden, cell) = self.lstm(x) 
        last_hidden = hidden[-1]
        attn_applied = self.attention_forward(lstm_out, last_hidden)
        combined = torch.cat((attn_applied, last_hidden), dim=1)
        combined = torch.relu(self.attention_combine(combined))
        output = self.out(combined)
        return output