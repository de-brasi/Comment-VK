# Действия конопок первого уровня______________________________________________________________________________________________
def click_enter():  # пусть станет серой при нажатии
    '''
    Действие кнопки верхнего уровня для ввода времени.
    Меняет значения hour_input, minute_input, second_input,
        если они были введены в поля Entry.
    Генерирует при первом нажатии такую же кнопку, как и кнопку вызова, но темную.
    '''
    global default_start_time_hour, default_start_time_minute, default_start_time_second
    if time_hour.get(): default_start_time_hour = int(time_hour.get())  # изменение стандартного значения
    if time_minute.get(): default_start_time_minute = int(time_minute.get())  # времени в модуле autocomment_work_module
    if time_second.get(): default_start_time_second = int(time_second.get())
    enter_lvl_1 = Button(window, text="ввести", command=click_enter,
                         bg='light grey', font=font)
    enter_lvl_1.grid(column=4, row=0)

    LOG_FILE.write('Введенное время - {}:{}:{}'.format(default_start_time_hour, default_start_time_minute,
                                                  default_start_time_second) +
    '\n')


# Действия конопок второго уровня_______________________________________________________________________________________________
def else_photo():
    '''
    Действие кнопки второго уровня для добавления ссылки.
    Генерирует поля ввода для ссылки и приглашающую надпись.
    Вызывает функцию вызова кнопки ввода с параметром 'else'.
    "Красит" вызывающую кнопку и меняет геометрию окна window.
    '''
    global link_invintation, link_enter  # !
    link_invintation = Label(window, text='Вставьте ссылку',
                             font=font)
    link_invintation.grid(column=0, row=3)

    link_enter = Entry(window, width=15, font=font)
    link_enter.grid(column=4, row=3)

    enter('else')

    black_grey_else()
    grey_del()
    window.geometry('370x320')


def del_photo():
    '''
    Действие кнопки второго уровня для удаления ссылки.
    Генерирует поля ввода для ссылки и приглашающую надпись.
    Вызывает функцию вызова кнопки ввода с параметром 'delete'.
    "Красит" вызывающую кнопку.
    '''
    global link_invintation, link_enter  # !
    link_invintation = Label(window, text='Вставьте ссылку',
                             font=font)
    link_invintation.grid(column=0, row=3)

    link_enter = Entry(window, width=15, font=font)
    link_enter.grid(column=4, row=3)

    enter('delete')

    black_grey_del()
    grey_else()


def enter(mod):
    '''
    Вызывается из else_photo или del_photo.
    Функция вызова кнопки для ввода с двумя возможными модификациями:
        'else' - создает кнопку с добавлением ссылки на фото в качестве действия нажатия;
        'delete' - создает кнопку с удалением, если возможно, ссылки на фото в качестве действия нажатия;
    Кнопка с именем enter_lvl_2 - глобальная для объемлющего модуля переменная.
    '''
    global enter_lvl_2
    if mod == 'else':
        enter_lvl_2 = Button(window, text="     Ввод      ",
                             command=pop_link, font=font)
        enter_lvl_2.grid(column=0, row=4)
    if mod == 'delete':
        enter_lvl_2 = Button(window, text="     Ввод      ",
                             command=del_link, font=font)
        enter_lvl_2.grid(column=0, row=4)


def pop_link():  # отсылает полученную ссылку как строковый элемент в функцию для получения id фото?
    finish_button()

    link = link_enter.get()
    owner_id = tools.get_owners_id(LOG_FILE, log_out, link)
    photos_id = tools.get_photos_id(link)
    if link and owner_id and (photos_id not in variables.photo_stack):
        if not variables.set_owner_id:
            variables.photo_stack.append(photos_id)  # пропихнуть ссылку
            variables.set_owner_id.add(owner_id)  # owner_id в сет хозяев групп
            variables.photos_link.append(link)  # добавить введенную ССЫЛКУ в список ссылок
        elif owner_id in variables.set_owner_id:
            variables.photo_stack.append(photos_id)  # пропихнуть ссылку
            variables.photos_link.append(link)  # добавить введенную ССЫЛКУ в список ссылок
        elif owner_id not in variables.set_owner_id:
            log_out.insert(INSERT,
                           '!Добавленны фото из нескольких групп. Пожалуйста, добавляйте фото только из одной группы' + 17 * ' ')
            LOG_FILE.write('!Добавленны фото из нескольких групп. Пожалуйста, добавляйте фото только из одной группы' +
    '\n')
    elif not link:
        log_out.insert(INSERT, 'Вставьте ссылку!' + (35 - len('Вставьте ссылку!')) * ' ')
        LOG_FILE.write('Вставьте ссылку!' +
    '\n')
    link_enter.delete(0, END)

    window.geometry('370x370')

    print('photo_stack is {}'.format(variables.photo_stack))
    log_out.insert(INSERT, 'Добавленно {} фото'.format(len(variables.photo_stack)) + (
            35 - len('Добавленно {} фото'.format(len(variables.photo_stack)))) * ' ')
    LOG_FILE.write('Добавленно {} фото'.format(len(variables.photo_stack)) +
    '\n')


def del_link():
    link = link_enter.get()
    if link:
        photos_id = tools.get_photos_id(link)
        if photos_id in variables.photo_stack:
            variables.photo_stack.remove(photos_id)
            try:
                variables.photos_link.remove(link)  # удалить, если можно, введенную ССЫЛКУ из списка ссылок
            except:
                pass
        else:
            print('!Невозможно удалить из списка - Вы еще не добавляли такого фото.')  # в вывод пользователю
            log_out.insert(INSERT, '!Невозможно удалить из списка - Вы еще не добавляли такого фото.' + (
                    70 - len('!Невозможно удалить из списка - Вы еще не добавляли такого фото.')))
            LOG_FILE.write('!Невозможно удалить из списка - Вы еще не добавляли такого фото.' +
    '\n')
    else:
        log_out.insert(INSERT, 'Вставьте ссылку!' + (35 - len('Вставьте ссылку!')) * ' ')
        LOG_FILE.write('Вставьте ссылку!' +
    '\n')

    link_enter.delete(0, END)


# Действия конопок третьего уровня______________________________________________________________________________________________
def finish_button():
    global flag, start

    nothing = Label(window, text=' ', font=font)
    nothing.grid(column=0, row=5)

    start = Button(window, text="Начало работы", command=main_start,
                   font=font)
    start.grid(column=0, row=6)


def main_start():
    '''
    Действия кнопки начала работы.
    Сначала запускает поток th_main с выполнением функции main(главная функция программы),
        потом в логи выводит ссылки, которые должен был откомментить.
    '''
    th_main.start()

    LOG_FILE.write('-Введенные для комментирования ссылки:-' +
    '\n')
    for link in variables.photos_link:
        LOG_FILE.write(link +
    '\n')
    LOG_FILE.write('-Конец списка ссылок-' +
    '\n')


# Состояния конопок второго уровня_______________________________________________________________________________________________

def grey_else():
    global switch_photo_else
    switch_photo_else = Button(window, text="Добавить к списку",
                               command=else_photo, font=font)
    switch_photo_else.grid(column=0, row=2)


def black_grey_else():
    global switch_photo_else
    switch_photo_else = Button(window, text="Добавить к списку",
                               bg='light grey', command=else_photo, font=font)
    switch_photo_else.grid(column=0, row=2)


def grey_del():
    global switch_photo_del
    switch_photo_del = Button(window, text="Удалить из списка",
                              command=del_photo, font=font)
    switch_photo_del.grid(column=4, row=2)


def black_grey_del():
    global switch_photo_del
    switch_photo_del = Button(window, text="Удалить из списка",
                              bg='light grey', command=del_photo, font=font)
    switch_photo_del.grid(column=4, row=2)
