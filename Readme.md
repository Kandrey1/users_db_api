
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
            127.0.0.1:5000/POST/api/parameters/user1/name1/type1/value1
            127.0.0.1:5000/POST/api/parameters/user2/name2/type2/value2
            127.0.0.1:5000/POST/api/parameters/user1/name1/type3/value3
        error:
            127.0.0.1:5000/POST/api/parameters/user21/name1/type3/value3

- ###2 endpoint 


    http://127.0.0.1:3000/GET/api/parameters/<string:user_name>/<path:path_url>
    
    tests:
        good:
            127.0.0.1:5000/GET/api/parameters/user2/name2/type2
            127.0.0.1:5000/GET/api/parameters/user1/name1/type3
            127.0.0.1:5000/GET/api/parameters/user1/name1/type1
        error:
            127.0.0.1:5000/GET/api/parameters/user21/name1/type3
            127.0.0.1:5000/GET/api/parameters/user2/name1
- ###3 endpoint 


    http://127.0.0.1:3000//GET/api/parameters/<string:user_name>/
    
    tests:
        good:
            127.0.0.1:5000/GET/api/parameters/user4
            127.0.0.1:5000/GET/api/parameters/user7
            127.0.0.1:5000/GET/api/parameters/user1
        error:
            127.0.0.1:5000/GET/api/parameters/user21
            127.0.0.1:5000/GET/api/parameters/userqw
    

- ###4 endpoint 


    http://127.0.0.1:3000/POST/api/<string:user_name>

    tests:
        good:
        ---------------------------------------------------
            data = {"Query": [{ "Operation":"SetParam", 
                                "Name":"name6", 
                                "Type":"type6", 
                                "Value":"258" }]}
            127.0.0.1:5000/POST/api/user4
            
        ---------------------------------------------------    
            data = {"Query": [{ "Operation":"SetParam", 
                                "Name":"name6", 
                                "Type":"type6", 
                                "Value":"258" },
                              { "Operation":"SetParam", 
                                "Name":"name7", 
                                "Type":"type7", 
                                "Value":"856" }]}

            127.0.0.1:5000/POST/api/user7

        error:
         ---------------------------------------------------    
            data = {"Query": [{ "Operation":"SetParam", 
                                "Name":"name6", 
                                "Type":"type6", 
                                "Value":"258" }]}
            127.0.0.1:5000/POST/api/user21
    