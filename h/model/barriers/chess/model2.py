import json
import math
import os.path

import torch.nn

import chess
import chess.engine
import chess.syzygy

from kan import *

from h.model.utils import utils_print


class Model:

    def __init__(self):
        self.sf = None
        self.job = None
        self.params = None
        self.listener = None
        self.process = None
        self.thread = None
        self.commands = None
        self.stop = None
        self.random = None
        self.model = None
        self.dataset = {}
        self.last_fen = None
        self.file_model = None
        self.file_formula1 = None
        self.file_formula2 = None
        self.pre_model_json = None
        self.model_json = None
        self.model_option = None
        self.lib_formula = None
        self.engine_stockfish = None
        self.syzygy_endgame = None
        self.epd_eval = None
        self.len_input = None
        self.count_limit = None
        self.device = None
        self.dtype = None
        self.formula1 = None
        self.formula2 = None

        self.model_config()

    def model_config(self):
        self.engine_stockfish = \
            'D:/Work2/PyCharm/SmartEval2/github/src/healers/healers/dist' + \
            '/stockfish-windows-x86-64-avx2.exe'
        self.syzygy_endgame = {
            "wdl345": "E:/Chess/syzygy/3-4-5-wdl",
            "wdl6": "E:/Chess/syzygy/6-wdl",
        }
        self.commands = {
            0: {"call": None, "desc": "Exit"},
            1: {"call": self.model_params, "desc": "Search hyperparameters"},
            2: {"call": self.model_finetune, "desc": "Fine-Tune model"},
            3: {"call": self.save_formula, "desc": "Save formula"},
            4: {"call": self.model_test, "desc": "Test model"},
            5: {"call": self.make_predict, "desc": "Make predict"},
        }
        self.stop = False
        self.random = random.SystemRandom(0)
        self.model_option = {
            "len_input": 68,
            "hidden_layers": [68, 34, 17, 9, 5, 3, 1],
            "len_output": 1,
            "grid": 5,
            "k": 3,
        }
        self.file_model = "model2.pth"
        self.file_formula1 = "model2_formula1.txt"
        self.file_formula2 = "model2_formula2.txt"
        self.pre_model_json = "pre_model2.json"
        self.model_json = "model2.json"
        self.lib_formula = [
            'x', 'x^2', 'x^3', 'x^4', 'exp',
            'log', 'sqrt', 'tanh', 'sin', 'tan', 'abs',
        ]
        self.epd_eval = "dataset.epdeval"
        # self.count_limit = 48
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu'
        )
        self.dtype = torch.get_default_dtype()

        print(str(self.device).upper(), self.dtype)

        self.formula1, self.formula2 = self.model_load()

    def start(self):
        while True:
            print("Available commands:")
            for key, value in self.commands.items():
                print(f"   {key}. {value['desc']}")
            try:
                command = int(input("Input command [default 0]: "))
            except ValueError:
                command = 0
            if command not in self.commands.keys():
                print("Error: Command not found")
                continue
            if command == 0:
                break
            self.job = self.commands[command]["call"]
            self.params = {}
            self.job()

    def model_save(self):
        torch.save(self.model.state_dict(), self.file_model)
        d = self.dataset["train_input"].tolist()
        tl = self.dataset["train_label"].tolist()
        for i in range(len(d)):
            d[i].append(tl[i])
        with open("dataset.json", "w") as f:
            json.dump(d, f)

    def save_formula(self):
        utils_print("self.save_formula() starting...")
        self.model_finetune(save_formula=True)

    def model_load(self):
        # print("Loading model...")
        if os.path.exists(self.model_json):
            with open(self.model_json, "r") as f:
                self.model_option = json.load(f)
        else:
            with open(self.model_json, "w") as f:
                json.dump(self.model_option, f)
        self.model = KAN(
            width=[
                self.model_option["len_input"],
                *self.model_option["hidden_layers"],
                self.model_option["len_output"]
            ],
            grid=self.model_option["grid"],
            k=self.model_option["k"], auto_save=False, seed=0,
            noise_scale=0.1,
            sp_trainable=False,
            sb_trainable=False,
        )
        if os.path.exists(self.file_model):
            self.model.load_state_dict(torch.load(self.file_model))
        if not os.path.exists(self.file_formula1) or \
           not os.path.exists(self.file_formula2):
            return None, None
        else:
            with open(self.file_formula1, encoding="UTF-8", mode="r") as p:
                f1 = str(p.read()).strip()
            with open(self.file_formula2, encoding="UTF-8", mode="r") as p:
                f2 = str(p.read()).strip()
            return f1, f2

    def model_finetune(self, save_formula=False):
        if not save_formula:
            utils_print("self.model_finetune() starting...")
        count = 0
        while True:
            count += 1
            utils_print(count)
            self.load_data(nums=1000, epoch=500)
            utils_print(self.dataset["train_input"].shape)
            utils_print(self.dataset["train_label"].shape)
            utils_print(self.dataset["test_input"].shape)
            utils_print(self.dataset["test_label"].shape)
            result = self.model.fit(
                self.dataset,
                opt="LBFGS",
                # loss_fn=torch.nn.,
                lamb=0.001,
                steps=2,
                update_grid=False,
                metrics=(
                     self.train_acc,
                     self.test_acc
                )
            )
            utils_print(result['train_acc'][-1], result['test_acc'][-1])
            model.model_save()
            self.dataset = {}
            if save_formula:
                self.model.auto_symbolic(lib=self.lib_formula)
                formula1 = self.model.symbolic_formula()[0][0]
                with open(self.file_formula1, encoding="UTF-8", mode="w") as p:
                    p.write(str(formula1).strip())
                break
            self.model_load()

    def get_best(self, state):
        moves = list(state.legal_moves)
        best_move = None
        best_value = - 10 ** 10
        for move in moves:
            state.push(move)
            inputs = torch.FloatTensor(
                [self.get_input(state)]
            ).type(self.dtype).to(self.device)
            score = self.model(inputs).detach().tolist()[0][0]
            if score > best_value:
                best_value = score
                best_move = move
            state.pop()
        return best_move

    def get_data(self, nums=10, epoch=10):
        result_train = []
        result_label = []
        board = chess.Board()
        for num in range(nums):
            result = 0.
            board_copy = board.copy()
            inputs = self.get_input(board)
            for ep in range(epoch):
                while not board_copy.is_game_over():
                    moves = list(board_copy.legal_moves)
                    best_move = self.random.choice(moves)
                    # best_move = self.get_best(board_copy)
                    board_copy.push(best_move)
                if board_copy.result() == "1-0":
                    result += 1.
                elif board_copy.result() == "0-1":
                    result += -1.
                else:
                    pass
            result_train.append(inputs)
            result_label.append(result / epoch)
            if board.is_game_over():
                board = chess.Board()
            else:
                moves = list(board.legal_moves)
                best_move = self.random.choice(moves)
                board.push(best_move)
        return result_train, result_label

    def load_data(self, nums=10, epoch=10):
        train_inputs, train_labels = self.get_data(nums=nums, epoch=epoch)
        self.dataset['train_input'] = \
            torch.FloatTensor(train_inputs).type(self.dtype).to(self.device)
        self.dataset['train_label'] = \
            torch.FloatTensor(train_labels).type(self.dtype).to(self.device)
        test_inputs, test_labels = self.get_data(nums=nums, epoch=epoch)
        # test_inputs, test_labels = train_inputs, train_labels
        self.dataset['test_input'] = \
            torch.FloatTensor(test_inputs).type(self.dtype).to(self.device)
        self.dataset['test_label'] = \
            torch.FloatTensor(test_labels).type(self.dtype).to(self.device)

    def model_params(self):
        print("self.model_params() starting...")
        self.load_data()
        print(self.dataset['train_input'].shape)
        print(self.dataset['test_input'].shape)
        if os.path.exists(self.pre_model_json):
            with open(self.pre_model_json, "r") as f:
                self.model_option = json.load(f)
        hidden_layer1 = self.model_option["hidden_layer"]
        grid1 = self.model_option["grid"]
        k1 = self.model_option["k"]
        maxi = 10 ** 10
        maximum_layer = 10 ** 10
        maximum_grid = 10 ** 10
        maximum_k = 10 ** 10
        while True:
            self.model = KAN(
                width=[self.len_input, *hidden_layer1, 1],
                grid=grid1, k=k1, auto_save=False, seed=0)
            result = self.model.fit(
                self.dataset,
                opt="LBFGS",
                steps=5,
                metrics=(
                    self.train_acc,
                    self.test_acc
                )
            )
            if result['test_acc'][-1] < maxi:
                maxi = result['test_acc'][-1]
                maximum_layer = hidden_layer1
                maximum_grid = grid1
                maximum_k = k1
                with open(self.pre_model_json, "w") as f:
                    data = {"hidden_layer": maximum_layer,
                            "grid": maximum_grid,
                            "k": maximum_k}
                    json.dump(data, f)

            print(result['train_acc'], result['test_acc'])
            print(f"hidden_layer={maximum_layer}, grid={maximum_grid}, " +
                  f"k={maximum_k}, maxi_test_acc={maxi}")
            print(f"hidden_layer={hidden_layer1}, grid={grid1}, " +
                  f"k={k1}, test_loss={result['test_loss'][0]}")
            # if self.stop:
            #     self.model_save()
            break
            # hidden_layer1 = self.random.choice(list(range(5, 101)))
            # grid1 = self.random.choice(list(range(5, 51)))
            # k1 = self.random.choice(list(range(3, 26)))

    def train_acc(self):
        return torch.mean((torch.round(self.model(self.dataset['train_input'])) ==
                           self.dataset['train_label']).type(self.dtype))

    def test_acc(self):
        return torch.mean((torch.round(self.model(self.dataset['test_input'])) ==
                           self.dataset['test_label']).type(self.dtype))

    @staticmethod
    def get_input(state):
        train_input = [0. for _ in range(64)]
        for piece in chess.PIECE_TYPES:
            for square in state.pieces(piece, chess.BLACK):
                train_input[square] = \
                    - math.sin(2 * math.pi * piece + math.pi / 63 * square)
        for piece in chess.PIECE_TYPES:
            for square in state.pieces(piece, chess.WHITE):
                train_input[square] = \
                    math.sin(2 * math.pi * piece + math.pi / 63 * square)
        if state.has_kingside_castling_rights(state.turn):
            train_input = [1.] + train_input
        else:
            train_input = [0.] + train_input
        if state.has_kingside_castling_rights(state.turn):
            train_input = [1.] + train_input
        else:
            train_input = [0.] + train_input
        if state.ep_square is None:
            train_input = [0.] + train_input
        else:
            train_input = [state.ep_square] + train_input
        train_input = [int(state.turn)] + train_input
        return train_input

    def model_test(self):
        print("self.model_test() starting...")
        self.load_data()
        y_pred = self.model(self.dataset['test_input'])
        for i in range(len(self.dataset["test_input"])):
            print(
                y_pred[i], self.dataset["test_label"][i]
            )
        # formula1, formula2 = self.model.symbolic_formula()[0]
        # print('train acc of the formula:',
        #       self.acc(
        #           formula1, formula2, self.dataset['train_input'],
        #           self.dataset['train_label'])
        #       )
        # print('test acc of the formula:',
        #       self.acc(
        #           formula1, formula2, self.dataset['test_input'],
        #           self.dataset['test_label'])
        #       )
        # y_true = self.dataset["train_label"]
        # variables = []
        # for data in self.dataset["train_input"]:
        #     variables.append({
        #         f"x_{i}": data[i - 1].numpy().item(0)
        #         for i in range(self.len_input, 0, -1)
        #     })
        # y_pred = []
        # for data in variables:
        #     formula1 = str(self.formula1)
        #     for key, value in data.items():
        #         formula1 = str(formula1).replace(key, str(value))
            # formula2 = str(self.formula2)
            # for key, value in data.items():
            #     formula2 = str(formula2).replace(key, str(value))
            # y_pred.append(eval(formula1))
        # print(y_pred)
        #
        # regmet.RegressionMetrics(y_true, y_pred)

    def make_predict(self):
        print("self.make_predict() starting...")
        fen_start = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        board1 = chess.Board()
        board1.set_fen(fen_start)
        print(board1)
        while True:
            moves = list(board1.legal_moves)
            index = 0
            bestmove = index
            score = 10 ** 6
            for move in moves:
                board1.push(move)
                board2 = chess.Board()
                board2.set_fen(board1.fen())
                board1.pop()
                inputs = self.get_input(state=board1)
                variable_values = {
                    f"x_{i}": inputs[i - 1]
                    for i in range(self.len_input, 0, -1)
                }
                formula = self.model_load()
                for _var, _val in variable_values.items():
                    formula = str(formula).replace(_var, str(_val))
                evaluate1 = eval(formula)
                if evaluate1 < score:
                    bestmove = index
                    score = evaluate1
                index += 1
            board1.push(moves[bestmove])
            print(board1)
            print("")
            if board1.is_game_over():
                break
            board1.push(random.choice(list(board1.legal_moves)))
            print(board1)
            print("")
            if board1.is_game_over():
                break
        print(board1.result())


if __name__ == "__main__":
    model = Model()
    model.start()
