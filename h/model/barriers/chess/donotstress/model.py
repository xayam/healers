import os
import random

import torch
from torch_geometric.data import Data
from torch_geometric.nn import GATConv, global_mean_pool, global_max_pool
import chess


class ChessDataGenerator:
    def __init__(self, num_samples=1000):
        self.epd_eval = "../dataset.epdeval"
        self.random = random.SystemRandom(0)
        self.num_samples = num_samples
        self.piece_values = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 100}

    def get_fen_epd(self):
        with open(self.epd_eval, mode="r") as f:
            dataevals = f.readlines()
        fens, scores = [], []
        for _ in range(self.num_samples):
            dataeval = str(self.random.choice(dataevals)).strip()
            spl = dataeval.split(" ")
            fen = " ".join(spl[:-1])
            fens.append(fen)
            scores.append(float(spl[-1]))
        return fens, scores

    def board_to_graph(self, board, score):
        """Безопасное преобразование позиции в граф с проверкой индексов."""
        node_features = []
        square_to_index = {}

        # 1. Собираем узлы (только для фигур, которые есть на доске)
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                # Генерируем признаки для фигуры
                features = [
                    self.piece_to_id(piece.symbol()),
                    0.0 if piece.color == chess.WHITE else 1.0,
                    (square % 8) / 7.0,
                    (square // 8) / 7.0,
                    len(list(board.legal_moves)) / 20.0
                ]
                node_features.append(features)
                square_to_index[square] = len(node_features) - 1  # Индексация с 0

        # 2. Проверяем, что есть хотя бы два узла для создания рёбер
        if len(node_features) < 1:
            return None

        # 3. Собираем рёбра с проверкой валидности индексов
        edge_index = []
        for square in chess.SQUARES:
            if square not in square_to_index:
                continue

            # Получаем всех атакующих текущий квадрат
            attackers = board.attackers(chess.WHITE, square) | board.attackers(
                chess.BLACK, square)

            for attacker_sq in attackers:
                # Критически важная проверка!
                if attacker_sq not in square_to_index:
                    continue

                src = square_to_index[attacker_sq]
                dst = square_to_index[square]

                # Дополнительная проверка индексов
                if src < len(node_features) and dst < len(node_features):
                    edge_index.append([src, dst])
                else:
                    print(
                        f"Invalid edge: ({src}->{dst}) for {len(node_features)}"
                        f" nodes"
                    )
                    continue

        # 4. Проверяем целостность графа
        if not edge_index:
            return None

        return Data(
            x=torch.tensor(node_features, dtype=torch.float),
            edge_index=torch.tensor(edge_index, dtype=torch.long).t().contiguous(),
            y=torch.tensor([[score]], dtype=torch.float)
        )

    def piece_to_id(self, symbol):
        """Преобразует символ фигуры в числовой ID."""
        return list(self.piece_values.keys()).index(symbol.lower())

    def generate_dataset(self):
        """Генерирует набор данных."""
        dataset = []
        fens, scores = self.get_fen_epd()
        for i in range(len(fens)):
            board = chess.Board()
            board.set_fen(fens[i])
            graph = self.board_to_graph(board, scores[i])
            if graph.num_nodes > 0:
                dataset.append(graph)
        return dataset

    def predict(self, model, board):
        graph = self.board_to_graph(board, 0.0)
        if graph.num_nodes > 0:
            return model(graph)[0][0]
        else:
            return None


class ChessGNN(torch.nn.Module):
    def __init__(self, node_dim=5, hidden_dim=64):
        super().__init__()
        self.file_model = "model.pth"
        self.node_embed = torch.nn.Linear(node_dim, hidden_dim)
        self.gat1 = GATConv(hidden_dim, hidden_dim)
        self.gat2 = GATConv(hidden_dim, hidden_dim)
        self.fc = torch.nn.Sequential(
            torch.nn.Linear(2 * hidden_dim, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 32),
            torch.nn.ReLU(),
            torch.nn.Linear(32, 1))
        self.model_load()

    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch
        x = self.node_embed(x)
        x = self.gat1(x, edge_index)
        x = torch.relu(x)
        x = self.gat2(x, edge_index)
        x = torch.cat([global_mean_pool(x, batch), global_max_pool(x, batch)], dim=1)
        return self.fc(x)

    def model_save(self):
        torch.save(self.state_dict(), self.file_model)

    def model_load(self):
        if os.path.exists(self.file_model):
            self.load_state_dict(torch.load(self.file_model))


def train():
    generator = ChessDataGenerator(num_samples=1000)
    dataset = generator.generate_dataset()
    model = ChessGNN()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0005)
    criterion = torch.nn.MSELoss()

    for epoch in range(500):
        total_loss = 0
        for batch in dataset:
            optimizer.zero_grad()
            out = model(batch)
            loss = criterion(out, batch.y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f'Epoch {epoch + 1}, Loss: {total_loss / len(dataset):.4f}')
    model.model_save()
    result = model(dataset[0])
    print(result)
    print(dataset[0].y)


if __name__ == "__main__":
    train()
