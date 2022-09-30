class CodeHuffmanError:
    def __init__(self, text, type):
        self.text = text
        self.type = type

    @staticmethod
    def createHuffmanError(text, type):
        return CodeHuffmanError(text, type)


class CodeHuffman:
    def __init__(self):
        pass

    def __init__(self, text):
        self.codeTable = dict()
        try:
            self.alphabet = []
            for let in text:
                if let not in self.alphabet:
                    self.alphabet.append(let)  # a, b, r, c, d

            self.weights = []
            for letter in self.alphabet:
                self.weights.append(text.count(letter))  # 5, 2, 2, 1, 1

            nodes = {}
            for i in range(len(self.alphabet)):
                nodes[self.alphabet[i]] = self.weights[i]

            start_tree = []  # [(a, 5), (b, 2), (r, 2), (c, 1), (d, 1)]
            for i in range(len(self.alphabet)):
                start_tree.append([self.alphabet[i], self.weights[i]])

            all_ways = []  # здесь дерево
            while len(start_tree) > 0:  # т.е. мы нашли корень дерева
                # по алгоритму берем 2 символа с наименьшей частотой
                first = start_tree[-1]  # [d, 1]
                second = start_tree[-2]  # [c, 1]
                all_ways.append(
                    [first[0], second[0]])  # d, c  в итоге получим => [[d, c], [dc, r], [b, dcr], [a, bdcr]]
                del start_tree[-1]
                del start_tree[-1]
                new_node = [first[0] + second[0], first[1] + second[1]]  # [dc, 2]
                # новый узел вставляем в список не просто в конец, а так, чтобы узлы были по убыванию
                for index, nod in enumerate(start_tree):
                    if nod[1] < new_node[1]:
                        start_tree.insert(index, new_node)
                        break
                    elif nod[1] == new_node[1]:
                        start_tree.insert(index + 2, new_node)  # если веса одинаковы, то просто вставляем как некст звено
                        break

            self.dict_tree = {}  # a=0, b=10, r=111, c=1101, d=1100
            current_line = ''
            for count, pair in enumerate(reversed(all_ways), start=1):
                symbol_1 = pair[0]
                symbol_2 = pair[1]

                if len(symbol_2) > 1:
                    self.dict_tree[symbol_1] = current_line + '0'
                    current_line += '1'
                elif len(symbol_1) > len(symbol_2):
                    self.dict_tree[symbol_2] = current_line + '1'
                    current_line += '0'
                elif len(symbol_1) == len(symbol_2):
                    self.dict_tree[symbol_2] = current_line + '1'
                    self.dict_tree[symbol_1] = current_line + '0'
            for symbol, code_text in self.dict_tree.items():
                self.codeTable[symbol] = (len(code_text), int(code_text, 2))
        except Exception:
            CodeHuffmanError.createHuffmanError("Unable to find codeword", 101)

    def code(self, text):
        try:
            self.array_bytes = []

            bytes_text = ""
            dict_bytes = {}
            for symbol, tuple_lenInTwice_TwiceNumber in self.codeTable.items():
                num_in_twice = bin(tuple_lenInTwice_TwiceNumber[1])[2:]
                dict_bytes[symbol] = num_in_twice

            for letter in text:
                bytes_text += dict_bytes[letter]

            length_secure_text = len(bytes_text)
            length_secure_text_INTWICE = bin(length_secure_text)[2:]
            length_secure_text_INTWICE = length_secure_text_INTWICE.rjust(32, "0")

            start, finish = 0, 8
            for i in range(4):
                self.array_bytes.append(length_secure_text_INTWICE[start:finish])
                start += 8
                finish += 8

            if len(bytes_text) > 0:
                while len(bytes_text) > 0:
                    line = bytes_text[:8]
                    bytes_text = bytes_text[8:]
                    if len(line) < 8:
                        line = line.rjust(8, '0')
                    self.array_bytes.append(line)
            return list(map(int, self.array_bytes))
        except Exception:
            CodeHuffmanError.createHuffmanError("Unable to find codeword", 101)

    def decode(self, codeSequence):
        try:
            # узнаем длину кодового слова из первых четырех байт
            codeSequence = list(map(str, codeSequence))
            for index, elem in enumerate(codeSequence, start=1):
                if index >= 4:
                    codeSequence[index - 1] = elem.rjust(8, '0')
            line = ''.join(codeSequence[:4])
            codeSequence = ''.join(codeSequence[4:])
            line = int(line, 2)

            bytes_before_last = codeSequence[:len(codeSequence) - 8]
            last_byte_str = codeSequence[len(codeSequence) - 8:]
            summary_count_before_last_byte = len(codeSequence) - line
            if summary_count_before_last_byte > 0:
                last_byte_str = last_byte_str[summary_count_before_last_byte:]
                codeSequence = bytes_before_last + last_byte_str

            res = ""
            while codeSequence:
                for k, v in self.dict_tree.items():
                    if codeSequence.startswith(v):
                        res += k
                        codeSequence = codeSequence[len(v):]
            return res
        except Exception:
            CodeHuffmanError.createHuffmanError("Unable to recognize codeword", 102)


if __name__ == '__main__':
    codeHuffman = CodeHuffman("abracadabra")
    codedSequence = codeHuffman.code("abracadabra")
    print(f"Закодированное сообщение в массиве байт: {codedSequence}")
    decodedSequence = codeHuffman.decode(codedSequence)
    print(f"Раскодированная строка из массива байт: {decodedSequence}")

    # Закодированное сообщение в массиве байт: [0, 0, 0, 10111, 1011101, 10101100, 101110]
    # Раскодированная строка из массива байт: abracadabra
