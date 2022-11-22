import os
from tkinter import *
from tkinter.ttk import *
from tkinter.ttk import Combobox
from tkinter import filedialog
from tkinter import messagebox as mb
from tkinter import ttk
import json
import requests
from typing import Dict
from pprint import pprint


class AddInfoCar:
    def __init__(self, car: str, authorization: dict):
        self.__authorization = authorization
        self.__collect_data_car(car)

    def __collect_data_car(self, car):
        url = f'http://ws.pecom.ru/AvtoPEK_YYR_2/hs/pkUatInfo/v1/car?number={car}'
        res = requests.get(url, auth=(self.__authorization['user_name'], self.__authorization['password']))
        print(res.status_code)
        if res.status_code == 200:
            self.__data_dict = json.loads(res.text)
        else:
            print('ERROR')

    @property
    def get_data(self) -> dict:
        return self.__data_dict


class Line:
    def __init__(self, parent: Frame, element: str, array_info_car: list):
        self.__info = {}
        self.__array = array_info_car
        self.__parent = parent
        self.__element = element
        self.__create_line()

    def __create_line(self) -> None:
        Label(self.__parent, text=self.__element).pack(side=LEFT, fill=X)
        self.__entry = Entry(self.__parent)
        self.__entry.pack(side=RIGHT, fill=X)

    @property
    def info(self):
        self.__info[self.__element] = self.__entry.get()
        return self.__info

    @property
    def element_entry(self):
        return self.__entry

    @property
    def element_name(self):
        return self.__element


class Files:
    def __init__(self, frame: LabelFrame, path_file: str, info_name: str):
        self.__array_path = None
        self.__path_file = path_file
        self.__info_name = info_name
        self.__frame_root = frame
        self.__create_info_doc()

    def __create_info_doc(self) -> None:
        self.__frame = LabelFrame(self.__frame_root)
        self.__frame.pack()
        self.__label_name = Label(self.__frame, text=f'{self.__info_name} | ')
        self.__label_name.pack(side=LEFT)
        self.__label_file = Label(self.__frame, text=self.__path_file.split('/')[-1])
        self.__label_file.pack(side=RIGHT)

    def destroy_line(self) -> None:
        self.__frame.pack_forget()

    @property
    def get_info(self) -> list:
        self.__array_path = [self.__info_name, self.__path_file]
        return self.__array_path


class Table:
    def __init__(self, frame_root: Frame, car: list, congruence: dict, login_pass: dict, info_document: list):

        self.__frame_root = frame_root
        self.__car = car
        self.__congruence = congruence
        self.__login_pass = login_pass
        self.__info_document = info_document

        self.__array_info_car = []
        self.__array_files = []

        self.__create_label_frame()
        self.__create_line_car()
        self.__create_documents()
        self.__create_radiobutton()
        self.__add_mos_ru()

    def __create_label_frame(self) -> None:
        self.__frame_car = LabelFrame(self.__frame_root, text='car')
        self.__frame_car.pack(side=LEFT, expand=1, fill=Y)

        self.__frame_radiobutton = LabelFrame(self.__frame_root)
        self.__frame_radiobutton.pack(side=LEFT, expand=1, fill=Y)

        self.__frame_vehicle_car = LabelFrame(self.__frame_radiobutton, width=7, height=1,
                                              text='Собственник тс совпадает с правообладателем (заявителем)')
        self.__frame_vehicle_car.pack(side=TOP)

        self.__frame_documents = LabelFrame(self.__frame_radiobutton, width=7, height=1, text='добавить документ')
        self.__frame_documents.pack(anchor=N, expand=1, fill=X)

        self.__frame_documents_info = LabelFrame(self.__frame_radiobutton, text=' документ')
        self.__frame_documents_info.pack(anchor=N, expand=1, fill=X)

    def __add_file(self) -> None:
        self.__top_lvl = Toplevel()
        self.__top_lvl.attributes("-topmost", True)

        Label(self.__top_lvl, text='Укажите тип').pack(side=TOP)

        self.__combobox = Combobox(self.__top_lvl, values=self.__info_document, width=40, state='readonly')
        self.__combobox.set('выбрать......')
        self.__combobox.pack()

        Button(self.__top_lvl, text='Добавить файл', command=self.__set_file).pack()
        Button(self.__top_lvl, text='Закрыть', command=self.__top_lvl.destroy).pack()

    def __set_file(self) -> None:
        if self.__combobox.get() == 'выбрать......':
            mb.showerror("Ошибка", "Не выбран тип документа")
        else:
            self.__document_open = filedialog.askopenfilename()
            self.__create_info_doc()
            self.__top_lvl.destroy()

    def __create_line_car(self) -> None:
        for element in self.__car:
            frame = Frame(self.__frame_car)
            frame.pack(fill=X, expand=True)
            self.__line = Line(frame, element, self.__array_info_car)
            self.__array_info_car.append(self.__line)
        Button(self.__frame_car, text='получить данные по тс', command=self.__fullness_car).pack(side=RIGHT)

    def __fullness_car(self) -> None:
        for element in self.__congruence:
            for line in self.__array_info_car:
                if line.element_name == self.__congruence[element]:
                    line.element_entry.delete(0, 'end')
                    line.element_entry.insert(END, AddInfoCar(self.__get_car(), self.__login_pass).get_data[element])
        self.__collect_document()
        pprint(self.__info_car)

    def __create_radiobutton(self) -> None:
        self.__vehicle_owner = BooleanVar()

        rb_1 = Radiobutton(self.__frame_vehicle_car, text='Да', variable=self.__vehicle_owner, value=0)
        rb_1.bind('<Button-1>', self.__event_vehicle_car)
        rb_1.pack(expand=1, fill=X)
        rb_2 = Radiobutton(self.__frame_vehicle_car, text='Нет', variable=self.__vehicle_owner, value=1)
        rb_2.bind('<Button-1>', self.__event_vehicle_car)
        rb_2.pack(expand=1, fill=X)

        self.__applicant_entry = Entry(self.__frame_vehicle_car, state="readonly")
        self.__applicant_entry.pack(expand=1, fill=X, side=TOP)

    def __event_vehicle_car(self, event) -> None:
        if self.__vehicle_owner.get() == 0:
            self.__applicant_entry.config(state='normal')
        else:
            self.__applicant_entry.delete(0, END)
            self.__applicant_entry.config(state="readonly")

    def __create_info_doc(self) -> None:
        self.__file = Files(self.__frame_documents_info, str(self.__document_open), self.__combobox.get())
        if len(self.__array_files) < 1:
            self.__button_delete = Button(self.__frame_documents, text='Удалить', command=self.__delete_document)
            self.__button_delete.pack(side=BOTTOM)
        self.__array_files.append(self.__file)

    def __create_documents(self) -> None:
        Button(self.__frame_documents, text='добавить документ', command=self.__add_file).pack(side=LEFT)

    def __add_mos_ru(self) -> None:
        Button(text='заполнить информацию на сйте ', command=self.__collect_document).pack()

    def __get_car(self) -> str:
        self.__collect_document()
        return self.__info_car['ГРЗ']

    def __collect_document(self) -> None:
        self.__info_car = {}
        for i in self.__array_info_car:
            self.__info_car.update(i.info)
        self.__info_car['vehicle'] = [self.__vehicle_owner.get(), self.__applicant_entry.get()]  ### владелец
        files = []
        for i in self.__array_files:  ### файлы
            files.append(i.get_info)
        self.__info_car['files'] = files

        pprint(self.__info_car)

    def __delete_document(self) -> None:
        if not len(self.__array_files) == 0:
            self.__array_files[-1].destroy_line()
            self.__array_files = self.__array_files[:-1]
            if len(self.__array_files) == 0:
                # self.__frame_documents_info.pack_forget()  ### bags
                self.__button_delete.pack_forget()


class App:
    def __init__(self, car: list, congruence: dict, login_pass: dict, info_document_name: list):
        self.__car = car
        self.__congruence = congruence
        self.__login_pass = login_pass
        self.__login_pass = login_pass
        self.__info_document_name = info_document_name

        self.__create_app()

    def __create_app(self) -> None:
        root = Tk()
        self.root_frame = Frame()
        self.root_frame.pack()
        Table(self.root_frame, self.__car, self.__congruence, self.__login_pass, self.__info_document_name)
        root.mainloop()


if __name__ == '__main__':
    conformity = {'VIN': 'VIN',
                  'Model': 'Марка модель АМ',
                  'DateOfMake': 'Год выпуска',
                  'STS': 'Серия номер СТС',
                  'STSIssueDate': 'Дата выдачи СТС',
                  'DiagCard': 'Номер диагностической карты',
                  'DiagCardExpireDate': 'Срок действия | До какого числа действует',
                  'EcoClass': 'Экологический класс',
                  'OwnMass': 'Масса без нагрузки',
                  'MaxMass': 'Максимальная допустимая масса'}
    label_car = ['ГРЗ', 'Серия номер СТС', 'Дата выдачи СТС', 'VIN', 'Масса без нагрузки',
                 'Максимальная допустимая масса', 'Год выпуска', 'Номер диагностической карты',
                 'Срок действия | До какого числа действует', 'Марка модель АМ', 'Экологический класс', 'Категория ТС']
    documents_name = ['Иные документы', 'Свидетельство о регистрации ТС', 'Документ, подтверждающее вещное право',
                      'Паспорт ТС_10367',
                      'Карточка доступа на международное ТС', 'Диагоностическая карта (Талон техосмотра)']

    authorization = {'user_name': 'uatInfo',
                     'password': 'P6nUZxkWmK'}

    App(label_car, conformity, authorization, documents_name)
