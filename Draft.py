import random

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
        self.int_count_of_registers, self.int_count_of_adders = 3, int(input('Введите количество сумматоров: '))
        self.list_of_adders = []
        for int_current_number_of_adder in range(self.int_count_of_adders):
            self.list_of_adders.append(Adder(list(map(int, input('Введите индексы для сумматора № {}: '.format(int_current_number_of_adder
                                                                                                              + 1)).split()))))
        self.dictionary_transition = self.create_transition_dictionary()
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
        '''Декодирование кодового слова

        Создание/дополнение словаря решётчатой диаграммы и декодирование на его основе.
        Вид словаря: {итерация: {состояние регистров: метка накопления ошибок, ...}}.'''
        dictionary_trellis_diagram = {}
        list_states_for_processing = ['00']
        string_result = ''
        list_code_subwords = [string_code_word[int_point_of_trimm : int_point_of_trimm + self.int_count_of_adders] for int_point_of_trimm
                              in range(0, len(string_code_word), self.int_count_of_adders)]
        int_iteration = 0
        for string_current_code_subword in list_code_subwords:
            dictionary_workspace = {}
            for string_current_state in list_states_for_processing:
                for string_current_substate in self.dictionary_transition[string_current_state].keys():
                    try:
                        int_current_differences = get_number_of_differences(
                            self.dictionary_transition[string_current_state][string_current_substate],
                            string_current_code_subword) + dictionary_trellis_diagram[int_iteration - 1][string_current_state]
                    except:
                        int_current_differences = get_number_of_differences(self.dictionary_transition[string_current_state][string_current_substate],
                                                                                                  string_current_code_subword)
                    if string_current_substate in dictionary_workspace.keys() and dictionary_workspace[string_current_substate] <= int_current_differences:
                        pass
                    else: dictionary_workspace[string_current_substate] = int_current_differences
            dictionary_trellis_diagram[int_iteration] = dictionary_workspace
            int_iteration += 1
            list_states_for_processing = [string_current_state for string_current_state in dictionary_workspace.keys()]
        print('Словарь решётчатой диаграммы:')
        for string_current_key in dictionary_trellis_diagram.keys():
            print('  {}: {}'.format(string_current_key, dictionary_trellis_diagram[string_current_key]))
        for int_current_iteration in dictionary_trellis_diagram.keys():
            int_current_index_state_minimal_difference = list(dictionary_trellis_diagram[int_current_iteration].keys()).index(min(
                dictionary_trellis_diagram[int_current_iteration], key = dictionary_trellis_diagram[int_current_iteration].get))
            if int_current_index_state_minimal_difference % 2 == 0: string_result += '0'
            else: string_result += '1'
        return string_result

def list_to_string(list_execute: list) -> str:
    '''Перевод строк в список'''
    return ''.join(list(map(str, list_execute)))
def get_number_of_differences(string_first, string_second : str) -> int:
    '''Нахождение количества несовпадений в строках по битам'''
    int_counter_of_differences = 0
    for int_current_index in range(len(string_first)):
        if string_first[int_current_index] != string_second[int_current_index]: int_counter_of_differences += 1
    return int_counter_of_differences
def changing_the_bit(string_bit: str) -> str:
    '''Заменяет бит на противоположный'''
    return str((int(string_bit) + 1) % 2)

codec = Codec()
print('Cловарь переходов между состояниями:')
for string_current_key in codec.dictionary_transition.keys():
    print('  {}: {}'.format(string_current_key, codec.dictionary_transition[string_current_key]))
string_input_text_real = input('\nВведите текст для кодирования: ')
string_input_text_binary = bin(int.from_bytes(string_input_text_real.encode(), 'big'))[2:]
print('Входное сообщение в бинарном виде:', string_input_text_binary)
string_code_word = codec.encode(string_input_text_binary)
print('Кодовое слово:', string_code_word)
int_position_of_error = random.randint(0, len(string_code_word))
string_message_word = (string_code_word[:int_position_of_error] + changing_the_bit(string_code_word[int_position_of_error]) +
                       string_code_word[int_position_of_error + 1:])
string_output_text_binary = codec.decode(string_message_word)
if string_output_text_binary != string_input_text_binary: print('В процессе декодирования произошла ошибка.')
string_output_text_real = int(string_output_text_binary, 2).to_bytes((int(string_output_text_binary, 2).bit_length() + 7) // 8, 'big').decode()
print('Выходное сообщение:\n{}'.format(string_output_text_real))
