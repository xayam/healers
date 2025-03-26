
import os
import random

import chess
import chess.engine
import torch
from torch import optim

from h.model.barriers.chess.poler.model import Model
from h.model.barriers.chess.poler.enviroment import Enviroment


class ChessAgent:
    def __init__(self, is_white=True, model=True):
        self.memory = []
        self.file_model = None
        self.enviroment = Enviroment()
        self.is_white = is_white
        self.model = None
        self.optimizer = None
        if model:
            self.file_model = "white.pth" if self.is_white else "black.pth"
            self.model = Model()
            self.optimizer = optim.Adam(self.model.parameters())
            self.model_load()

    def predict_pos(self, board_sequence):
        with torch.no_grad():
            output = self.model(board_sequence.unsqueeze(0))
            return output.squeeze(0)

    def pos2move(self, board, predicted_pos):
        best_move = None
        min_diff = float('inf')
        for move in board.legal_moves:
            temp_board = board.copy()
            temp_board.push(move)
            new_tensor = self.enviroment.board_to_tensor(temp_board)
            diff = torch.mean((predicted_pos - new_tensor) ** 2)
            if diff < min_diff:
                min_diff = diff
                best_move = move
        return best_move

    def model_save(self):
        torch.save(self.model.state_dict(), self.file_model)

    def model_load(self):
        if self.model is not None:
            if os.path.exists(self.file_model):
                self.model.load_state_dict(torch.load(self.file_model))


class ChessRandomAgent(ChessAgent):
    def __init__(self, is_white=True, model=False):
        ChessAgent.__init__(self, is_white, model)

    def get_random(self, board):
        moves = list(board.legal_moves)
        move = random.choice(moves)
        return move


class ChessEngineAgent(ChessAgent):
    def __init__(self, is_white=True, model=False):
        ChessAgent.__init__(self, is_white, model)
        self.engine_stockfish = \
            'D:/Work2/PyCharm/SmartEval2/github/src/healers/healers/dist' + \
            '/stockfish-windows-x86-64-avx2.exe'
        self.sf = chess.engine.SimpleEngine.popen_uci(self.engine_stockfish)

    def get_move(self, board, best=True, shift=1, depth=10):
        result = self.sf.analyse(
            board,
            chess.engine.Limit(depth=depth),
            multipv=499,
        )
        if best:
            return result[0]['pv'][0]
        else:
            try:
                return result[-shift]['pv'][0]
            except IndexError:
                return result[0]['pv'][0]
