import hashlib
import json
import math
import os.path
import pickle
import sys

import torch.nn
from kan import *
from h.model.utils import utils_print


class Model:

    def __init__(self):
        self.range = None
        self.dataset_json = None
        self.input = None
        self.width = None
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
        self.file_formula = None
        self.pre_model_json = None
        self.model_json = None
        self.model_option = None
        self.lib_formula = None
        self.len_input = None
        self.count_limit = None
        self.device = None
        self.dtype = None
        self.formula = None

        self.model_config()

    def model_config(self):
        self.commands = {
            0: {"call": None, "desc": "Exit"},
            1: {"call": self.model_params, "desc": "Search hyperparameters"},
            2: {"call": self.model_finetune, "desc": "Fine-Tune model"},
            3: {"call": self.model_formula, "desc": "Save formula"},
            4: {"call": self.model_test, "desc": "Test model"},
            5: {"call": self.model_predict, "desc": "Make predict"},
        }
        self.stop = False
        self.random = random.SystemRandom(0)
        self.width = 2 ** 14
        self.range = list(range(1, 257))
        self.input = [
            self.random.choice(self.range)
            for _ in range(self.width)
        ]
        self.model_option = {
            "len_input": 40,
            "hidden_layers": [20, 10, 5, 3, 2, 1],
            "len_output": 1,
            "grid": 30,
            "k": 3,
        }
        self.file_model = "model.pth"
        self.file_formula = "model_formula.txt"
        self.pre_model_json = "pre_model.json"
        self.model_json = "model.json"
        self.dataset_json = "dataset.json"
        self.lib_formula = [
            'x', 'x^2', 'x^3', 'x^4', 'exp',
            'log', 'sqrt', 'tanh', 'sin', 'tan', 'abs',
        ]
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu'
        )
        self.dtype = torch.get_default_dtype()

        print(str(self.device).upper(), self.dtype)

        self.formula= self.model_load()

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
        torch.save(
            self.model.state_dict(), self.file_model,
            pickle_protocol=pickle.HIGHEST_PROTOCOL
        )
        d = self.dataset["train_input"].tolist()
        tl = self.dataset["train_label"].tolist()
        for i in range(len(d)):
            d[i].append(tl[i])
        with open(self.dataset_json, "w") as f:
            json.dump(d, f)

    def model_formula(self):
        utils_print("self.model_formula() starting...")
        self.model_finetune(save_formula=True)

    def set_dataset(self, json_data):
        self.dataset = {}
        train_inputs, train_labels = [], []
        for i in range(len(json_data)):
            train_inputs.append([json_data[i][0]])
            train_labels.append(json_data[i][1])
            print(train_inputs[-1], train_labels[-1])
        self.dataset['train_input'] = \
            torch.FloatTensor(train_inputs).type(self.dtype).to(self.device)
        self.dataset['train_label'] = \
            torch.FloatTensor(train_labels).type(self.dtype).to(self.device)
        self.dataset['test_input'] = self.dataset['train_input']
        self.dataset['test_label'] = self.dataset['train_label']

    def model_load(self):
        # print("Loading model...")
        if os.path.exists(self.model_json):
            with open(self.model_json, "r") as f:
                self.model_option = json.load(f)
        else:
            with open(self.model_json, "w") as f:
                json.dump(self.model_option, f)
        if os.path.exists(self.dataset_json):
            with open(self.dataset_json, "r") as f:
                self.set_dataset(json.load(f))
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
        if not os.path.exists(self.file_formula):
            return None
        else:
            with open(self.file_formula, encoding="UTF-8", mode="r") as p:
                f1 = str(p.read()).strip()
            return f1

    def model_finetune(self, save_formula=False):
        if not save_formula:
            utils_print("self.model_finetune() starting...")
        count = 0
        while True:
            count += 1
            utils_print(count)
            self.get_dataset()
            utils_print(self.dataset["train_input"].shape)
            utils_print(self.dataset["train_label"].shape)
            utils_print(self.dataset["test_input"].shape)
            utils_print(self.dataset["test_label"].shape)
            # utils_print(self.dataset["train_input"])
            # utils_print(self.dataset["train_label"].tolist())
            result = self.model.fit(
                self.dataset,
                opt="LBFGS",
                # loss_fn=self.loss_fn,
                lamb=0.01,
                steps=10000,
                update_grid=False,
                # metrics=(
                #      self.train_acc,
                #      self.test_acc
                # )
            )
            # utils_print(result['train_acc'][-1], result['test_acc'][-1])
            model.model_save()
            break
            self.dataset = {}
            if save_formula:
                self.model.auto_symbolic(lib=self.lib_formula)
                formula = self.model.symbolic_formula()[0][0]
                with open(self.file_formula, encoding="UTF-8", mode="w") as p:
                    p.write(str(formula).strip())
                break
            self.model_load()


    def n3transform(self, data):
        transform = {
            "000": [0, 0, 0],
            "001": [1, 0, 1],
            "010": [1, 0, 0],
            "011": [1, 1, 1],
            "100": [0, 0, 1],
            "101": [1, 1, 0],
            "110": [0, 1, 0],
            "111": [0, 1, 1],
        }
        output = data[:]
        for i in range(0, len(data), 3):
            output[i] = transform[
                str(data[i]) + str(data[i + 1]) + str(data[i + 2])
                ][0]
            output[i + 1] = transform[
                str(data[i]) + str(data[i + 1]) + str(data[i + 2])
                ][1]
            output[i + 2] = transform[
                str(data[i]) + str(data[i + 1]) + str(data[i + 2])
                ][2]
        return output


    def get_data(self):
        result_train, result_label = [], []
        s = ""
        for i in range(1, self.width):
            s += chr(self.input[i - 1])
            h = hashlib.sha1(s.encode("utf-8")).hexdigest()
            inp = []
            for c in h:
                inp.append(ord(c))
            result_train.append(inp)
            result_label.append(self.input[i])
        return result_train, result_label

    def get_dataset(self):
        train_inputs, train_labels = self.get_data()
        self.dataset['train_input'] = \
            torch.FloatTensor(train_inputs).type(self.dtype).to(self.device)
        self.dataset['train_label'] = \
            torch.FloatTensor(train_labels).type(self.dtype).to(self.device)
        self.dataset['test_input'] = self.dataset['train_input']
        self.dataset['test_label'] = self.dataset['train_label']

    def model_params(self):
        print("self.model_params() starting...")
        self.get_dataset()
        print(self.dataset['train_input'].shape)
        print(self.dataset['test_input'].shape)
        if os.path.exists(self.pre_model_json):
            with open(self.pre_model_json, "r") as f:
                self.model_option = json.load(f)
        len_input1 = self.model_option["len_input"]
        len_output1 = self.model_option["len_output"]
        grid1 = self.model_option["grid"]
        k1 = self.model_option["k"]
        hidden_layer1 = self.model_option["hidden_layers"]
        maximum_hl = hidden_layer1[:]
        maxi = 10 ** 10
        while True:
            self.model = KAN(
                width=[len_input1, *hidden_layer1, len_output1],
                grid=grid1, k=k1, auto_save=False, seed=0)
            result = self.model.fit(
                self.dataset,
                opt="LBFGS",
                lamb=0.01,
                steps=1,
                update_grid=False,
                # metrics=(
                #     self.train_acc,
                #     self.test_acc
                # )
            )
            if result['train_loss'][-1] < maxi:
                maxi = result['train_loss'][-1]
                maximum_hl = hidden_layer1[:]
                with open(self.pre_model_json, "w") as f:
                    data = {"hidden_layers": hidden_layer1,
                            "grid": grid1,
                            "k": k1}
                    json.dump(data, f)
                self.model_save()

            print(
                f"hidden_layer1={hidden_layer1}, " 
                f"maximum_hl={maximum_hl}, maxi={maxi}"
            )
            for i in range(len(hidden_layer1)):
                hidden_layer1[i] = \
                    self.random.choice(list(range(2, 100)))

    def loss_fn(self, x, y):
        return torch.mean(y - x)

    def train_acc(self):
        return torch.mean(
            torch.abs(
                    self.model(self.dataset['train_input'] -
                    self.dataset['train_label'])
            ).type(self.dtype))

    def test_acc(self):
        return torch.mean(
            torch.abs(
                    self.model(self.dataset['test_input'] -
                    self.dataset['test_label'])
            ).type(self.dtype))

    def model_test(self):
        pass

    def model_predict(self):
        print("self.model_predict() starting...")
        # print(self.dataset['train_input'])
        output = self.model(self.dataset['train_input']).tolist()
        # print(output)
        for i in range(len(output)):
            print(output[i][-5:])
            print(self.dataset['train_input'][i][-5:].tolist())
            print(self.dataset['train_label'][i][-5:].tolist())
            print("")


if __name__ == "__main__":
    model = Model()
    model.start()
