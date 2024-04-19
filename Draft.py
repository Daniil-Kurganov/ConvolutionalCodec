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
class Codec:
    def __init__(self) -> None:
        self.int_count_of_registers = 3
        self.list_of_adders = []
        for int_current_number_of_adder in range(int(input('Введите количество сумматоров: '))):
            self.list_of_adders.append(Adder(list(map(int, input('Введите индексы для сумматора № {}: '.format(int_current_number_of_adder
                                                                                                              + 1)).split()))))
        self.dictionary_transition = self.create_transition_dictionary()
        self.dictionary_trellis_diagram = {}
        return None
    def encode(self, string_information_word: str) -> str:
        '''Кодирование информационного слова'''
        list_information_word = [int(string_current_symbol) for string_current_symbol in string_information_word]
        list_registers, list_code_word = [0] * (self.int_count_of_registers - 1), []
        for int_current_bit in list_information_word:
            list_registers = [int_current_bit] + list_registers[:self.int_count_of_registers - 1]
            list_code_word += self.get_current_coder_result(list_registers)
        return list_to_string(list_code_word)
    def get_current_coder_result(self, list_registers: list) -> list:
        '''Получение текущего результата от состояния регистров'''
        list_result = []
        for adder_current in self.list_of_adders:
            list_result.append(adder_current.get_result(list_registers))
        return list_result
    def create_transition_dictionary(self) -> dict:
        '''Создание словаря переходов

        Вид словаря: {cостояние регистра: {состояние с добавлением 0: вес, состояние с добавлением 1: вес}, ...}
        '''
        dictionary_result = {}
        int_count_watching_registers = self.int_count_of_registers - 1
        list_work_registers = [[0] * self.int_count_of_registers]
        while True:
            list_current_registers = list_work_registers[0]
            list_work_registers.pop(0)
            string_current_registers_cut_name = list_to_string(list_current_registers[:int_count_watching_registers])
            dictionary_current_name = {}
            for int_current_append_bit in range(2):
                list_current_iteration_registers = [int_current_append_bit] + list_current_registers[:-1]
                dictionary_current_name[list_to_string(list_current_iteration_registers[:2])] = list_to_string(
                    self.get_current_coder_result(list_current_iteration_registers))
            dictionary_result[string_current_registers_cut_name] = dictionary_current_name
            for string_current_new_subname in dictionary_current_name.keys():
                if not string_current_new_subname in dictionary_result.keys():
                    list_work_registers.append([int(string_current_symbol) for string_current_symbol in
                                                (string_current_new_subname + string_current_registers_cut_name[
                                                    int_count_watching_registers - 1])])
            if not list_work_registers: return dictionary_result
    def decode(self, string_code_word: str) -> str:
        '''Декодирование кодового слова'''
        if not self.dictionary_trellis_diagram: string_start_dictionary_state = self.dictionary_transition.keys()[0]
        elif len(string_code_word) / len(self.list_of_adders)  <= len(self.dictionary_transition.keys()): pass
        else: pass
    def create_new_version_of_trellis_diagram_dictionary(self, string_start_dictionary_state: str, int_required_depth) -> None:
        '''Создание/дополнение словаря решётчатой диаграммы

        Вид словаря: {итерация: {состояние регистров: метка накопления ошибок, ...}}'''
        return None


def list_to_string(list_execute: list) -> str:
    '''Перевод строк в список'''
    return ''.join(list(map(str, list_execute)))

codec = Codec()
print('Cловарь переходов между состояниями:')
for string_current_key in codec.dictionary_transition.keys():
    print('  {}: {}'.format(string_current_key, codec.dictionary_transition[string_current_key]))
string_input_text_real = input('\nВведите текст для кодирования: ')
string_input_text_binary = bin(int.from_bytes(string_input_text_real.encode(), 'big'))[2:]
print('Входное сообщение в бинарном виде:', string_input_text_binary)
string_code_word = codec.encode(string_input_text_binary)
print('Кодовое слово:', string_code_word)
