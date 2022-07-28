from App import app,mysql



def getProduct():
        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT name from product order by date desc LIMIT 1')
            # product = get_results(cursor)

            product = cursor.fetchall()
            # res = product
            # res = str(res)
        
            query = str(product)

        char_to_replace = {
                ',': '',
                '(' : '',
                ')' : '',
                '\'': ''}

        def getQuery(text):
            for key, value in char_to_replace.items():
                text = text.replace(key, value)
            return str(text)

        query = getQuery(query)
        return query