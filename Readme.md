
Используется версия Python 3.7

Для установки необходимых модулей необходимо выполнить команду:

`pip install -r requirements.txt`

Для создания БД перейти в консоль Python в корне приложения выполнить следующие команды:

`from run import db`

`db.create_all()`


- ###1 endpoint 


    http://127.0.0.1:3000/'/POST/api/parameters/<string:user_name>/<string:param_name>/<string:param_type>/<string:param_value>
    

- ###2 endpoint 


    http://127.0.0.1:3000/GET/api/parameters/<string:user_name>/<string:param_name>/<string:param_type>
    
 
- ###3 endpoint 


    http://127.0.0.1:3000//GET/api/parameters/<string:user_name>/
    

- ###4 endpoint 


    http://127.0.0.1:3000/POST/api/<string:user_name>
    