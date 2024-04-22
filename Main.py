import sys
import random
from PyQt5.QtWidgets import QMessageBox
from GUI import *

class Adder:
    def __init__(self, list_indices_of_registers: list) -> None:
        '''Запись списка регистров, принадлежащих сумматору'''
        self.list_indices_of_registers = list_indices_of_registers
        return None
    def get_result(self, list_current_word_in_registers: list) -> int:
        '''Возвращение результата работы сумматора'''
        int_result_bit = 0
        for int_current_bit_index in self.list_indices_of_registers:
            int_result_bit = int(ord(str(int_result_bit)) ^ ord(str(list_current_word_in_registers[int_current_bit_index])))
        return int_result_bit
class Codec:
    def __init__(self, int_count_of_adders: int, list_adders_registers: list) -> None:
        '''Запоминание количества регистров и сумматоров, создание списка сумматоров, создание словаря переходов состояний'''
        self.int_count_of_registers, self.int_count_of_adders = 3, int_count_of_adders
        self.list_of_adders = []
        for list_current_adder_registers in list_adders_registers:
            self.list_of_adders.append(Adder(list_current_adder_registers))
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
        ui.TableWidgetDictionaryTrellisDiagram.setRowCount(len(dictionary_trellis_diagram))
        ui.TableWidgetDictionaryTrellisDiagram.setColumnCount(len(dictionary_trellis_diagram[1]))
        ui.TableWidgetDictionaryTrellisDiagram.horizontalHeader().setVisible(False)
        for int_current_iteration in dictionary_trellis_diagram.keys():
            int_current_column_index = 0
            for string_current_state in dictionary_trellis_diagram[int_current_iteration].keys():
                string_current_output_text = "'{}': {}".format(string_current_state,
                                                             dictionary_trellis_diagram[int_current_iteration][string_current_state])
                ui.TableWidgetDictionaryTrellisDiagram.setItem(int_current_iteration, int_current_column_index,
                                                           QtWidgets.QTableWidgetItem(string_current_output_text))
                int_current_column_index += 1
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
def show_error_message(int_error_key: int, string_error_message: str) -> None:
    '''Вывод ошибок'''
    dictionary_errors = {6: 'Некорректное создание кодека', 13: 'Ошибка процесса декодирования'}
    message_error = QMessageBox()
    message_error.setIcon(QMessageBox.Critical)
    message_error.setText(dictionary_errors[int_error_key])
    message_error.setInformativeText(string_error_message)
    message_error.setWindowTitle("Ошибка!")
    message_error.exec_()
    return None
def create_codec() -> None:
    '''Создание нового кодека'''
    global codec
    int_count_of_adders = int(ui.SpinBoxCountOfAdders.value())
    list_adders_registers, list_input_adders_registers_text = [], ui.TextEditAddersRegisters.toPlainText().split('\n')
    if len(list_input_adders_registers_text) != int_count_of_adders:
        show_error_message(6, 'Количество сумматоров не совпадает с присвоенными регистрами.')
        return None
    for string_current_row_input in list_input_adders_registers_text:
        int_length_of_row = len(string_current_row_input)
        if 1 <= int_length_of_row <= int_length_of_row * 2 -1 and int_length_of_row % 2 != 0:
            list_workspace = []
            for string_current_number in string_current_row_input.split(' '):
                int_current_number = int(string_current_number)
                if not 0 <= int_current_number <= 2 or int_current_number in list_workspace:
                    show_error_message(6, 'Некорректный ввод списка регистров для сумматора.')
                    return None
                list_workspace.append(int_current_number)
            list_adders_registers.append(list_workspace)
        else:
            show_error_message(6, 'Некорректная длина списка регистров для сумматора.')
            return None
    codec = Codec(int_count_of_adders, list_adders_registers)
    ui.SpinBoxCountOfAdders.setEnabled(False)
    ui.TextEditAddersRegisters.setEnabled(False)
    ui.PushButtonCreateCodec.setEnabled(False)
    ui.TableWidgetDictionaryTransition.setEnabled(True)
    ui.PushButtonResetCodec.setEnabled(True)
    ui.LabelMessageWord.setEnabled(True)
    ui.LabelInputTextReal.setEnabled(True)
    ui.LabelOutputTextReal.setEnabled(True)
    ui.LabelCodeWord.setEnabled(True)
    ui.TextEditMessageWord.setEnabled(True)
    ui.TextEditCodeWord.setEnabled(True)
    ui.TextEditInputTextReal.setEnabled(True)
    ui.TextEditOutputTextReal.setEnabled(True)
    ui.PushButtonStartCodecWork.setEnabled(True)
    ui.TableWidgetDictionaryTrellisDiagram.setEnabled(True)
    int_current_iteration = 0
    ui.TableWidgetDictionaryTransition.setRowCount(len(codec.dictionary_transition))
    ui.TableWidgetDictionaryTransition.setVerticalHeaderLabels(codec.dictionary_transition.keys())
    for string_current_state in codec.dictionary_transition.keys():
        list_current_state_values = list(codec.dictionary_transition[string_current_state].values())
        ui.TableWidgetDictionaryTransition.setItem(int_current_iteration, 0, QtWidgets.QTableWidgetItem("'{}'".format(str(list_current_state_values[0]))))
        ui.TableWidgetDictionaryTransition.setItem(int_current_iteration, 1, QtWidgets.QTableWidgetItem("'{}'".format(str(list_current_state_values[1]))))
        int_current_iteration += 1
    return None
def reset_codec() -> None:
    '''Сброс текущего кодека'''
    global codec
    codec = NotImplemented
    ui.SpinBoxCountOfAdders.setEnabled(True)
    ui.TextEditAddersRegisters.setEnabled(True)
    ui.PushButtonCreateCodec.setEnabled(True)
    ui.TableWidgetDictionaryTransition.setEnabled(False)
    ui.PushButtonResetCodec.setEnabled(False)
    ui.LabelMessageWord.setEnabled(False)
    ui.LabelInputTextReal.setEnabled(False)
    ui.LabelOutputTextReal.setEnabled(False)
    ui.LabelCodeWord.setEnabled(False)
    ui.TextEditMessageWord.setEnabled(False)
    ui.TextEditCodeWord.setEnabled(False)
    ui.TextEditInputTextReal.setEnabled(False)
    ui.TextEditOutputTextReal.setEnabled(False)
    ui.PushButtonStartCodecWork.setEnabled(False)
    ui.TableWidgetDictionaryTrellisDiagram.setEnabled(False)
    ui.TextEditAddersRegisters.clear()
    ui.TextEditMessageWord.clear()
    ui.TextEditCodeWord.clear()
    ui.TextEditInputTextReal.clear()
    ui.TextEditOutputTextReal.clear()
    ui.TableWidgetDictionaryTransition.clearContents()
    ui.TableWidgetDictionaryTrellisDiagram.clearContents()
    return None
def start_codec_work() -> None:
    '''Кодирование и декодирование входного сообщения'''
    global codec
    string_input_text_real = ui.TextEditInputTextReal.toPlainText()
    string_input_text_binary = bin(int.from_bytes(string_input_text_real.encode(), 'big'))[2:]
    string_code_word = codec.encode(string_input_text_binary)
    ui.TextEditCodeWord.setText(string_code_word)
    int_position_of_error = random.randint(0, len(string_code_word) - 1)
    string_message_word = (string_code_word[:int_position_of_error] + changing_the_bit(string_code_word[int_position_of_error]) +
                string_code_word[int_position_of_error + 1:])
    ui.TextEditMessageWord.setText(string_message_word)
    string_output_text_binary = codec.decode(string_message_word)
    if string_output_text_binary != string_input_text_binary: show_error_message(13,
                                                'Длина раскодированного слова не совпадает с длиной информационного слова')
    string_output_text_real = int(string_output_text_binary, 2).to_bytes((int(string_output_text_binary, 2).bit_length() + 7) // 8,
                                                                         'big').decode()
    ui.TextEditOutputTextReal.setText(string_output_text_real)

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
ui.PushButtonCreateCodec.clicked.connect(create_codec)
ui.PushButtonResetCodec.clicked.connect(reset_codec)
ui.PushButtonStartCodecWork.clicked.connect(start_codec_work)
sys.exit(app.exec_())