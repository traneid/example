from tkinter import *
from tkinter.ttk import *
import json
from tkinter import ttk


class Checker:

    @staticmethod
    def is_int_positive(value: str) -> bool:
        return value.isnumeric()

    @staticmethod
    def is_int_negative(value: str) -> bool:
        return value.startswith('-') and value[1:].isnumeric()

    @staticmethod
    def is_float_positive(value: str) -> bool:
        return value.replace('.', '', 1).isnumeric()

    @staticmethod
    def is_float_negative(value: str) -> bool:
        return value.startswith('-') and value[1:].replace('.', '', 1).isnumeric()

    @classmethod
    def is_int(cls, value: str) -> bool:
        return cls.is_int_positive(value) or cls.is_int_negative(value)

    @classmethod
    def is_float(cls, value: str) -> bool:
        return cls.is_float_positive(value) or cls.is_float_negative(value)

    @staticmethod
    def is_number_positive(value: str) -> bool:
        return value.replace('.', '', 1).isnumeric()

    @staticmethod
    def is_number_negative(value: str) -> bool:
        return value.startswith('-') and value[1:].replace('.', '', 1).isnumeric()

    @classmethod
    def is_number(cls, value: str):
        return cls.is_int(value) or cls.is_float(value)

    @classmethod
    def is_zero(cls, value: str):
        return cls.is_number(value) and not value.replace('.', '', 1).replace('0', '').replace('-', '', 1)


class Line:
    def __init__(self, parent: Frame, elements: list, number: int = 0, ):
        self.__result = 0
        self.__text = ''
        self.__key_elements = ["wights", "text", "row", "column"]
        self.__style_add()

        self.__parent = parent
        self.__line_number = number

        self.__array_entry_line = []

        self.__set_elements_line(elements)
        self.__create_line()

        self.__label_alarm = []

    @property
    def label_text(self) -> str:
        return self.__text

    @staticmethod
    def __style_add() -> None:
        style = ttk.Style()
        style.configure("BW.TLabel", bd=10, background="white")

        style_1 = ttk.Style()
        style_1.configure("BR.TLabel", bd=10, background="red")

    def __create_line(self) -> None:
        """ кнопку блокировать если есть ошибки в полях """
        for element in self.__elements_line:
            row = element["row"] + int(self.__line_number)
            if element["wights"] == 'Entry':
                self.entry = Entry(self.__parent)
                self.entry.bind('<Key>', self.__alarms)
                self.entry.grid(row=row, column=element['column'])
                self.__array_entry_line.append(self.entry)
            elif element["wights"] == 'Button':
                self.button = Button(self.__parent, text=element['text'], state="disabled", command=self.__calculate)
                self.button.grid(row=row, column=element['column'])

    @staticmethod
    def __normalize(line) -> None:
        for element in line[1:-1]:
            normalize = element.get().strip().replace(',', '.').replace(' ', '')
            element.delete(0, END)
            element.insert(END, normalize)

    def __alarms(self, event) -> None:
        if self.__change_product_cell_color() and self.__check_numbers():
            self.__text = 'it is impossible to divide by 0'
            self.button.config(state='enable')
        else:
            self.button.config(state='disabled')

    def __change_product_cell_color(self) -> bool:
        self.button.config(state='disabled')
        entry = self.__array_entry_line[0]
        if len(entry.get()) <= 3 and entry.get() != '':
            entry.configure(style="BR.TLabel")
            self.__text = 'length less than 4 characters'
            return False
        elif entry.get() == '':
            self.button.config(state='disabled')
            return False
        else:
            entry.configure(style="BW.TLabel")
            return True

    def __check_numbers(self) -> bool:
        counter = 0

        if Checker.is_zero(self.__array_entry_line[3].get()):
            self.__text = 'it is impossible to divide by 0'
            return False
        else:
            for element in self.__array_entry_line[1:-1]:
                if element.get() != '' and Checker.is_float_positive(element.get()):
                    counter += 1
                if counter == len(self.__array_entry_line[1:-1]):
                    return True

    def check_empty_lines(self) -> bool:
        counter = 0
        for element in self.__array_entry_line:
            if element.get() == '':
                counter += 1
        if counter == len(self.__array_entry_line):
            return True

    def delete_line(self) -> None:
        for entry in self.__array_entry_line:
            entry.grid_forget()
        self.button.grid_forget()

    def __calculate(self):
        if not self.check_empty_lines():
            line = self.__array_entry_line
            self.__normalize(line)
            if self.__check_numbers():
                line[-1].delete(0, END)
                answer = float(line[1].get()) * float(line[2].get()) / float(line[3].get())
                line[-1].insert(END, answer)
                self.__result = answer
                self.__change_data()
            else:
                line[-1].delete(0, END)
                line[-1].insert(END, 'error')

    def get_answer(self) -> str:
        self.__calculate()
        return self.__array_entry_line[-1].get()

    def __change_data(self):
        for _, element in enumerate(self.__elements_line[:-2]):
            if element["column"] == _:
                element["text"] = self.__array_entry_line[_].get()
        self.__elements_line[-1]['text'] = self.__array_entry_line[-1].get()

    def __set_elements_line(self, elements: list) -> None:

        for element_list in elements:
            if type(element_list) != dict:
                raise TypeError("Waiting for a type: dict ")
            else:
                for key in self.__key_elements:
                    for line_key in elements:
                        if key not in line_key.keys():
                            raise KeyError(f"Key: '{key}' not found in '{element_list}' in label dict ")
        self.__elements_line = elements


class Table:
    def __init__(self, root: Tk, elements: dict, footer: dict):
        root.bind('<Key>', self.__add_remove_lines)

        self.__array_label = ["wights", "text", "row", "column", "columnspan"]
        self.__array_line = ["wights", "text", "row", "column"]
        self.__set_headers(elements["header"])
        self.__set_line(elements["line"])

        self.table_lines = []

        self.__frame = Frame()
        self.__frame.pack()
        self.__create_label()
        self.__create_line()

        self.footer = footer
        self.__create_footer()

    def __create_label(self) -> None:
        for elem in self.__header:
            Label(self.__frame, text=elem['text']).grid(row=elem["row"], column=elem['column'],
                                                        columnspan=elem['columnspan'])

    def __create_line(self, count=0) -> None:
        self.line = Line(self.__frame, self.__line, count)
        self.table_lines.append(self.line)

    def __create_footer(self) -> None:
        Footer(self.__frame, self.footer, self.table_lines)

    def __add_remove_lines(self, event) -> None:
        count = 0
        if not self.table_lines[-1:][-1].check_empty_lines():
            self.__create_line(len(self.table_lines))
        for line in self.table_lines[-2:]:
            if line.check_empty_lines():
                count += 1

            if count == 2:
                line.delete_line()
                self.table_lines = self.table_lines[:-1]

    def __set_headers(self, header: list) -> None:
        if type(header) != list:

            raise TypeError("Waiting for a type: list ")
        else:
            for key in self.__array_label:
                for header_key in header:
                    if key not in header_key.keys():
                        raise KeyError(f"Key: '{key}' not found in '{header}' in label list ")
        self.__header = header

    def __set_line(self, line: list) -> None:
        if type(line) != list:
            raise TypeError("Waiting for a type: list ")
        else:
            for key in self.__array_line:
                for header_key in line:
                    if key not in header_key.keys():
                        raise KeyError(f"Key: '{key}' not found in '{line}' in label list ")
        self.__line = line


class Footer:
    def __init__(self, parent: Frame, elements: dict, lines_array: list):
        self.parent = parent
        self.row = len(lines_array)
        self.data_lines = lines_array
        self.array_var = []
        self.__set_elements(elements)
        self.__element = []

        self.create_line(self.__elements[0], self.__answer_year)
        self.create_line(self.__elements[1])
        self.create_line(self.__elements[2], self.__answer_total)

    @property
    def elements(self) -> list:
        return self.__elements

    def __set_elements(self, elements) -> None:
        if type(elements) != list:
            raise TypeError("Waiting for a type: list ")
        else:
            for element in elements:
                if type(element) != list:
                    raise TypeError("Waiting for a type: list ")
                else:
                    for element_list in element:
                        if type(element_list) != dict:
                            raise TypeError("Waiting for a type: dict ")
                        else:
                            for element_dict in element_list:
                                if type(element_dict) != str:
                                    raise TypeError("Waiting for a type: str ")
                                else:
                                    for elem in element_dict:
                                        if type(elem) != str:
                                            raise TypeError("Waiting for a type: str ")
                                        else:
                                            self.__elements = elements

    def create_line(self, line, command_button=None) -> None:
        for widget in line:
            if widget["wights"] == 'Entry':
                number = StringVar()
                Entry(self.parent, textvariable=number).grid(row=widget["row"] + self.row, column=widget['column'])
                self.array_var.append(number)
            elif widget["wights"] == 'Label':
                _ = Label(self.parent, text=widget['text'])
                _.grid(row=widget["row"] + self.row, column=widget['column'], columnspan=widget['columnspan'])
            elif widget["wights"] == 'Button':
                Button(self.parent, text=widget['text'], command=command_button).grid(row=widget["row"] + self.row,
                                                                                      column=widget['column'])

    def __answer_year(self) -> bool:
        total = 0
        for data in self.data_lines:
            if Checker.is_float_positive(data.get_answer()):
                total += float(data.get_answer())
            elif data.get_answer() == 'error':
                self.array_var[0].set('error')
            else:
                self.array_var[0].set(total * 365)
                return True

    def __answer_total(self) -> None:

        if self.__answer_year():

            if self.array_var[1].get().strip() == '':
                self.array_var[1].set(1)
            if Checker.is_float_positive(self.array_var[1].get().strip()):
                self.array_var[-1].set(float(self.array_var[1].get()) * float(self.array_var[0].get()))
            else:
                self.array_var[-1].set('ERROR')
        else:
            self.array_var[-1].set('ERROR')

    @property
    def footer_answer(self) -> str:
        return self.__elements


class Data:
    def __init__(self, path_file: str):
        self.__data = ["table", "footer"]
        self.__set_data(path_file)

    @property
    def table(self) -> dict:
        return self.__table

    @property
    def footer(self) -> dict:
        return self.__footer

    def __get_elements(self, data_file) -> None:
        for key in self.__data:
            if key not in data_file.keys():
                raise KeyError(f"Key: '{key}' not found in '{data_file}' ")
            else:
                self.__table = data_file["table"]
                self.__footer = data_file["footer"]

    def __set_data(self, path_file: str) -> None:
        if type(path_file) != str:
            raise TypeError("Waiting for a element of type: str ")
        with open(path_file, "r", encoding='utf-8') as read_file:
            data_file = json.load(read_file)

            if type(data_file) == dict:
                self.__get_elements(data_file)
            else:
                raise TypeError("Waiting for the file structure: dict")


class App:
    def __init__(self, data: Data):
        self.__set_data(data)
        self.__create_app()

    def __create_app(self) -> None:
        root = Tk()
        Table(root, self.__data.table, self.__data.footer)
        root.mainloop()

    def __set_data(self, data: Data) -> None:
        if type(data) == Data:
            self.__data = data
        else:
            raise TypeError("Waiting for a element of type: Data")


if __name__ == "__main__":
    data_app = Data("json_cat.json")

    App(data_app)
