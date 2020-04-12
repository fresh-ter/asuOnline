import os
import requests
import ast
import json
 
numberAT = '' # Здесь должно быть число at
cookies = '' # Здесь должны быть куки

path_to_asursoUsers = 'asursoUsers.json'
path_to_asursoUsersOnline = 'asursoUsersOnline.json'


registeredData = list()
userRegisteredIdList = list()
onlineUsersList = list()

# Создаем пустой список для ASURSO_id пользователей, которые online во время нового запуска скрипта,
# а также их счетчик
onlineUsers = list()
newOnlineUsers = list()
counterNewUsersOnline = 0

def updateUserRegisteredList():
    global userRegisteredIdList

    userRegisteredIdList = list()

    # Создаем список с ASURSO_id из локальной базы
    for userData in registeredData:
        userRegisteredIdList.append(userData['userId'])

def updateUserRegisteredIdList_sorted():
    global userRegisteredIdList_sorted

    # Создаем группу списков для сортировки ASURSO_id из локальной базы по сотням тысяч...
    userRegisteredIdList_sorted = list() # 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | <=9 | >1 (hundred thousand)
    for x in range(0, 10):
        userRegisteredIdList_sorted.append(list())

    # ...теперь сортируем ASURSO_id
    for x in userRegisteredIdList:
        if x >= 100000 and x< 200000:
            userRegisteredIdList_sorted[0].append(x)
        elif x >= 200000 and x < 300000:
            userRegisteredIdList_sorted[1].append(x)
        elif x >= 300000 and x < 400000:
            userRegisteredIdList_sorted[2].append(x)
        elif x >= 400000 and x < 500000:
            userRegisteredIdList_sorted[3].append(x)
        elif x >= 500000 and x < 600000:
            userRegisteredIdList_sorted[4].append(x)
        elif x >= 600000 and x < 700000:
            userRegisteredIdList_sorted[5].append(x)
        elif x >= 700000 and x < 800000:
            userRegisteredIdList_sorted[6].append(x)
        elif x >= 800000 and x < 900000:
            userRegisteredIdList_sorted[7].append(x)
        elif x >= 900000:
            userRegisteredIdList_sorted[8].append(x)
        else:
            userRegisteredIdList_sorted[9].append(x)


if not os.path.isfile(path_to_asursoUsers):
    print("Файл локальной базы не найден!!!")
    print("Создаем новый...")
    f = open(path_to_asursoUsers, 'a+')
    f.close()
    print("Файл локальной базы успешно создан.")
else:
    print("Загружаем файл локальной базы...")
    # Копируем локальную базу в переменную
    with open(path_to_asursoUsers, "r") as read_file:
        registeredData = json.load(read_file)

    updateUserRegisteredList()

    print("Файл локальной базы успешно загружен.")


if not os.path.isfile(path_to_asursoUsersOnline):
    print("Файл с сохраненными online-пользователями не найден!!!")
    print("Создаем новый...")
    f = open(path_to_asursoUsersOnline, 'a+')
    f.close()
    print("Файл для сохранения online-пользователей успешно создан.")
else:
    print("Загружаем файл с сохраненными online-пользователями...")
    # Копируем JSON с ASURSO_id, которые были online при предыдущем запуске скрипта
    with open(path_to_asursoUsersOnline, "r") as read_file:
        onlineUsers = json.load(read_file)

    # Создаем список с ASURSO_id из скопированного JSON
    for userData in onlineUsers:
        onlineUsersList.append(userData['userId'])
    print("Файл с сохраненными online-пользователями успешно загружен.")


updateUserRegisteredIdList_sorted()


# Узнаем количество пользователей в локальной базе
numberUsersRegister = len(registeredData)

# Узнаем количество пользователей, которые были online при предыдущем запуске скрипта
numberUsersOnline = len(onlineUsers)

# --------------------------------------------------------------------------------------------

# Создаем и отправляем запрос на сервер ASURSO для получения списка пользователей онлайн
response = requests.get(
    'https://asurso.ru/webapi/context/activeSessions',
    headers={'GET': '/webapi/context/activeSessions HTTP/1.1',
    		'Host': 'asurso.ru',
    		'Connection': 'keep-alive',
    		'Accept': 'application/json, text/javascript, */*; q=0.01',
    		'Sec-Fetch-Dest': 'empty',
    		'X-Requested-With': 'XMLHttpRequest',
    		'at': numberAT,
    		'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36',
    		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    		'Sec-Fetch-Site': 'same-origin',
    		'Sec-Fetch-Mode': 'cors',
    		'Referer': 'https://asurso.ru/angular/school/announcements/',
    		'Accept-Encoding': 'gzip, deflate, br',
    		'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    		'Cookie': cookies
    },
)

print()
print("Ответ сервера: " + str(response))
print()

# Преобразуем данные от сервера в более читаемый вид
loadedData = ast.literal_eval(str(response.json()))

# Узнаем количество пользователей online по версии сервера ASURSO
numberLoadedRegister = len(loadedData)

# Создаем список ASURSO_id по данным от сервера
userLoadedIdList = list()
for userData in loadedData:
    userLoadedIdList.append(userData['userId'])

# Создаем группу списков для сортировки ASURSO_id из ответа сервера по сотням тысяч...
userLoadedIdList_sorted = list() # 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | <=9 | >1 (hundred thousand)
for x in range(0, 10):
    userLoadedIdList_sorted.append(list())

# ...теперь сортируем ASURSO_id
for x in userLoadedIdList:
    if x >= 100000 and x< 200000:
        userLoadedIdList_sorted[0].append(x)
    elif x >= 200000 and x < 300000:
        userLoadedIdList_sorted[1].append(x)
    elif x >= 300000 and x < 400000:
        userLoadedIdList_sorted[2].append(x)
    elif x >= 400000 and x < 500000:
        userLoadedIdList_sorted[3].append(x)
    elif x >= 500000 and x < 600000:
        userLoadedIdList_sorted[4].append(x)
    elif x >= 600000 and x < 700000:
        userLoadedIdList_sorted[5].append(x)
    elif x >= 700000 and x < 800000:
        userLoadedIdList_sorted[6].append(x)
    elif x >= 800000 and x < 900000:
        userLoadedIdList_sorted[7].append(x)
    elif x >= 900000:
        userLoadedIdList_sorted[8].append(x)
    else:
        userLoadedIdList_sorted[9].append(x)


# Здесь и так все понятно по названию
def registerNewUser(userId):
    global numberUsersRegister
    global counterNewUsersOnline

    id_l = userLoadedIdList.index(userId)

    print("Регистрируем нового пользователя: " + str(userId) + ". Name: " + loadedData[id_l]['nickName'])

    registeredData.append(dict())
    registeredData[numberUsersRegister]['id'] = numberUsersRegister+1
    registeredData[numberUsersRegister]['userId'] = userId
    registeredData[numberUsersRegister]['nickName'] = loadedData[id_l]['nickName']
    registeredData[numberUsersRegister]['roles'] = loadedData[id_l]['roles']
    registeredData[numberUsersRegister]['class'] = None
    registeredData[numberUsersRegister]['letter'] = None
    registeredData[numberUsersRegister]['active'] = True

    numberUsersRegister += 1

    newOnlineUsers.append(dict())
    newOnlineUsers[counterNewUsersOnline]['userId'] = userId
    counterNewUsersOnline += 1

    updateUserRegisteredList()
    updateUserRegisteredIdList_sorted()

def registerActivityUser(userId, active):
    global counterNewUsersOnline

    id_r = userRegisteredIdList.index(userId)

    print("Регистрируем активность пользователя: " + str(userId) + ". Name: " + registeredData[id_r]['nickName'] + ". Activity = " + str(active))
    
    if active:
        newOnlineUsers.append(dict())
        registeredData[id_r]['active'] = True
        newOnlineUsers[counterNewUsersOnline]['userId'] = userId
        counterNewUsersOnline += 1
    else:
        registeredData[id_r]['active'] = False


# Проверяем всех из списка от сервера на наличие в локальной базе (по ASURSO_id):
isRegistered = False
for x in range(0,10):
    for x_l in userLoadedIdList_sorted[x]:
        for x_r in userRegisteredIdList_sorted[x]:
            # если этот ASURSO_id есть в локальной базе, то регистрируем его положительную активность
            if x_l == x_r:
                isRegistered = True
                registerActivityUser(x_r, True)
                break
        # если этот ASURSO_id отсутствует в локальной базе, то регистрируем его в базе
        # (активность становится положительной в момент регистрации в локальной базе)
        if not isRegistered:
            registerNewUser(x_l)
        else:
            isRegistered = False

# Проверяем всех из списка прошлой активности на текущую активность (по ASURSO_id):
# (сравниваем со списком от сервера)
isActive = False
for x_o in onlineUsersList:
    for x in userLoadedIdList:
        # если пользователь активен, то оставляем его в списке
        if x_o == x:
            isActive = True
            break
    # если пользователя нет в списке с сервера, то регистрируем его отрицательную активность
    if not isActive:
        registerActivityUser(x_o, False)
    else:
        isActive = False



# Записываем обновленную локальную базу в файл
with open(path_to_asursoUsers, "w") as write_file:
    json.dump(registeredData, write_file, ensure_ascii=False)

# Записываем новый список online-пользователей в файл (в виде ASURSO_id)
with open(path_to_asursoUsersOnline, "w") as write_file:
    json.dump(newOnlineUsers, write_file, ensure_ascii=False)

print()


print()
print("Количество зарегистрированных в базе: " + str(len(registeredData)))
print()
print("Количество online в ответе сервера: " + str(len(loadedData)))
print()
print("Количество зарегистрированных в старом online-списке: " + str(numberUsersOnline))
print()
print("Количество зарегистрированных в online-списке: " + str(len(newOnlineUsers)))
print()


