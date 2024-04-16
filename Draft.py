class Adder:
    def __init__(self, list_indices_of_registers: list) -> None:
        self.list_indices_of_registers = list_indices_of_registers
        return None
    def get_result(self, list_current_word_in_registers: list) -> int:
        '''Возвращение результата работы сумматора'''
        int_result_bit = 0
        for int_current_bit_index in self.list_indices_of_registers:
            int_result_bit = int(ord(str(int_result_bit)) ^ ord(str(list_current_word_in_registers[int_current_bit_index])))
        return int_result_bit
class Coder:
    def __init__(self) -> None:
        self.int_count_of_registers = 3
        self.list_of_adders = []
        for int_current_number_of_adder in range(int(input('Введите количество сумматоров: '))):
            self.list_of_adders.append(Adder(list(map(int, input('Введите индексы для сумматора № {}: '.format(int_current_number_of_adder
                                                                                                              + 1)).split()))))
        return None
    def encode_information_word(self, string_information_word: str) -> str:
        '''Кодирование информационного слова'''
        list_information_word = [int(string_current_symbol) for string_current_symbol in string_information_word]
        list_registers, list_code_word = [0] * (self.int_count_of_registers - 1), []
        for int_current_bit in list_information_word:
            list_registers = [int_current_bit] + list_registers[:self.int_count_of_registers - 1]
            for adder_current in self.list_of_adders:
                list_code_word.append(adder_current.get_result(list_registers))
        return ''.join(list(map(str, list_code_word)))

sum = Coder()
string_input_text_real = input('\nВведите текст для кодирования: ')
string_input_text_binary = bin(int.from_bytes(string_input_text_real.encode(), 'big'))[2:]
print('Входное сообщение в бинарном виде:', string_input_text_binary)
string_code_word = sum.encode_information_word(string_input_text_binary)
print('Кодовое слово:', string_code_word)
