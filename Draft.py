class Adder:
    def __init__(self, list_indices_of_registers): self.list_indices_of_registers = list_indices_of_registers
    def get_result(self, list_current_word_in_registers: list) -> int:
        '''Возвращение результата работы сумматора'''
        int_result_bit = 0
        for int_current_bit_index in self.list_indices_of_registers:
            int_result_bit = int(ord(str(int_result_bit)) ^ ord(str(list_current_word_in_registers[int_current_bit_index])))
        return int_result_bit