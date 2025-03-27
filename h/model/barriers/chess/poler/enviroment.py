
import chess
import torch

from h.model.barriers.chess.poler.config import Config


class Enviroment(Config):
    def __init__(self):
        Config.__init__(self)

    def board_to_tensor(self, board):
        """Конвертирует доску в тензор размером 14x8x8"""
        tensor = torch.zeros(14, 8, 8)
        # Каналы 0-11: Фигуры (6 типов × 2 цвета)
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                channel = piece.piece_type - 1 + (6 if piece.color else 0)
                row, col = 7 - square // 8, square % 8
                tensor[channel, row, col] = 1
        # Каналы 12-13: Специальные флаги
        tensor[12] = int(board.has_queenside_castling_rights(chess.WHITE))
        tensor[13] = int(board.has_queenside_castling_rights(chess.BLACK))
        return tensor
