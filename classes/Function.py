# # from app import app,mysql



# # def getJumiaProducts():
# #         with app.app_context():
# #             cursor = mysql.connection.cursor()
# #             cursor.execute('SELECT name from product order by date desc LIMIT 1')
# #             # product = get_results(cursor)

# #             product = cursor.fetchall()
# #             # res = product
# #             # res = str(res)
        
# #             query = str(product)

# #         char_to_replace = {
# #                 ',': '',
# #                 '(' : '',
# #                 ')' : '',
# #                 '\'': ''}

# #         def getQuery(text):
# #             for key, value in char_to_replace.items():
# #                 text = text.replace(key, value)
# #             return str(text)

# #         query = getQuery(query)
# #         return query



# import atexit
# import os
# import subprocess
# from app import app,mysql



# def getJumiaProducts():
#         with app.app_context():
#             cursor = mysql.connection.cursor()
#             cursor.execute('SELECT name from product order by date desc LIMIT 1')
#             # product = get_results(cursor)

#             product = cursor.fetchall()
#             # res = product
#             # res = str(res)
        
#             query = str(product)

#         char_to_replace = {
#                 ',': '',
#                 '(' : '',
#                 ')' : '',
#                 '\'': ''}

#         def getQuery(text):
#             for key, value in char_to_replace.items():
#                 text = text.replace(key, value)
#             return str(text)

#         query = getQuery(query)
#         return query




# def get_flask_env():
#     flask_env = os.environ.copy()
#     if "FLASK_APP" not in flask_env:
#         flask_env["env"] = "./app.py"
#     if "FLASK_ENV" not in flask_env:
#         flask_env["FLASK_ENV"] = "development"
#     return flask_env


# def teardown(process_handle):
#     process_handle.terminate() #kill the sub process clean
#     process_handle.wait()# wait for graceful exit.


# def runSpiders():
#     with app.app_context():
#         flask_env = get_flask_env()
#         command = []
#         command.append("scrapy")
#         command.append("runspider")
#         command.append("usdToMad.py")
#         monitor = subprocess.Popen(command, env=flask_env)
#         atexit.register(teardown, monitor)

#         command = []
#         command.append("scrapy")
#         command.append("runspider")
#         command.append("jumiaSpider.py")
#         monitor = subprocess.Popen(command, env=flask_env)
#         atexit.register(teardown, monitor)

# # threading.Thread(target=fun).start()

#         # thread.start_new_thread(handle_sub_view, (request))
    
#     command = []
#     command.append("scrapy")
#     command.append("runspider")
#     command.append("amazonSpider.py")
#     monitor = subprocess.Popen(command, env=flask_env)
#     atexit.register(teardown, monitor)