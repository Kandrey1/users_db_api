
Используется версия Python 3.7.5

Для установки необходимых модулей необходимо выполнить команду:

`pip install -r requirements.txt`

Для запуска приложения необходимо запустить run.py в корне приложения 

`python run.py`

При переходе в браузере по адресу  `http://127.0.0.1:5000/` будет редирект на страницу `http://127.0.0.1:5000/user/`

После в корне приложения выполнить команду(установка в БД тестовых данных)

`python set_test_data.py`

На ней можно добавить нового User в БД и посмотреть всех существующих.

##ENDPOINTS
- ###1 endpoint 


    http://127.0.0.1:3000/'/POST/api/parameters/<string:user_name>/<string:param_name>/<string:param_type>/<string:param_value>
    
    tests:
        good:
            127.0.0.1:5000/POST/api/parameters/user1/name1/str/car
            127.0.0.1:5000/POST/api/parameters/user4/name6/int/1234
            127.0.0.1:5000/POST/api/parameters/user6/name4/str/bird
            127.0.0.1:5000/POST/api/parameters/user1/name1/str/cat
            127.0.0.1:5000/POST/api/parameters/user4/name6/int/dog
        error:
            127.0.0.1:5000/POST/api/parameters/user2/name1/str/1234
            127.0.0.1:5000/POST/api/parameters/user4/name1/int/value1
            127.0.0.1:5000/POST/api/parameters/user6/name1/test/value5
            127.0.0.1:5000/POST/api/parameters/user21/name1/str/value7

- ###2 endpoint 


    http://127.0.0.1:3000/GET/api/parameters/<string:user_name>
    
    tests:
        good:
            127.0.0.1:5000/GET/api/parameters/user1?name=name1&type=str
            127.0.0.1:5000/GET/api/parameters/user6?name=&type=str
            127.0.0.1:5000/GET/api/parameters/user9?name=&type=int
        error:
            127.0.0.1:5000/GET/api/parameters/user39?name=&type=
            127.0.0.1:5000/GET/api/parameters/user9?name=&type=
            127.0.0.1:5000/GET/api/parameters/user9?name=name1&type=
- ###3 endpoint 


    http://127.0.0.1:3000//GET/api/parameters/<string:user_name>/
    
    tests:
        good:
            127.0.0.1:5000/GET/api/parameters?user=user3
            127.0.0.1:5000/GET/api/parameters?user=user6
        error:
            127.0.0.1:5000/GET/api/parameters?user=user43
    

- ###4 endpoint 


    http://127.0.0.1:3000/POST/api/<string:user_name>

    tests:
        good:
        ---------------------------------------------------
            data = {"Query": [{ "Operation":"SetParam", 
                                "Name":"name6", 
                                "Type":"str", 
                                "Value":"car" }]}
            127.0.0.1:5000/POST/api/user4
            
        ---------------------------------------------------    
            data = {"Query": [{ "Operation":"SetParam", 
                                "Name":"name6", 
                                "Type":"str", 
                                "Value":"window" },
                              { "Operation":"SetParam", 
                                "Name":"name7", 
                                "Type":"int", 
                                "Value":"856" }]}

            127.0.0.1:5000/POST/api/user7

        error:
         ---------------------------------------------------    
            data = {"Query": [{ "Operation":"SetParam", 
                                "Name":"name6", 
                                "Type":"type6", 
                                "Value":"258" }]}
            127.0.0.1:5000/POST/api/user21
    