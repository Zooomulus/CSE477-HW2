import mysql.connector
from collections import defaultdict
import csv
import os

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'

        self.feedback_data = []


    def insert_feedback(self, name, email, comment):
        feedback_entry = {"name": name, "email": email, "comment": comment}
        self.feedback_data.append(feedback_entry)

    def get_all_feedback(self):
        return self.feedback_data

    def query(self, query = "SELECT CURDATE()", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if cur.lastrowid:
            return cur.lastrowid

        cur.close()
        cnx.close()
        return row

    def about(self, nested=False):    
        query = """select concat(col.table_schema, '.', col.table_name) as 'table',
                          col.column_name                               as column_name,
                          col.column_key                                as is_key,
                          col.column_comment                            as column_comment,
                          kcu.referenced_column_name                    as fk_column_name,
                          kcu.referenced_table_name                     as fk_table_name
                    from information_schema.columns col
                    join information_schema.tables tab on col.table_schema = tab.table_schema and col.table_name = tab.table_name
                    left join information_schema.key_column_usage kcu on col.table_schema = kcu.table_schema
                                                                     and col.table_name = kcu.table_name
                                                                     and col.column_name = kcu.column_name
                                                                     and kcu.referenced_table_schema is not null
                    where col.table_schema not in('information_schema','sys', 'mysql', 'performance_schema')
                                              and tab.table_type = 'BASE TABLE'
                    order by col.table_schema, col.table_name, col.ordinal_position;"""
        results = self.query(query)
        if nested == False:
            return results

        table_info = {}
        for row in results:
            table_info[row['table']] = {} if table_info.get(row['table']) is None else table_info[row['table']]
            table_info[row['table']][row['column_name']] = {} if table_info.get(row['table']).get(row['column_name']) is None else table_info[row['table']][row['column_name']]
            table_info[row['table']][row['column_name']]['column_comment']     = row['column_comment']
            table_info[row['table']][row['column_name']]['fk_column_name']     = row['fk_column_name']
            table_info[row['table']][row['column_name']]['fk_table_name']      = row['fk_table_name']
            table_info[row['table']][row['column_name']]['is_key']             = row['is_key']
            table_info[row['table']][row['column_name']]['table']              = row['table']
        return table_info

    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        print('I create and populate database tables.')

        table_creation_order = ['institutions', 'positions', 'experiences', 'skills']
    
        sql_folder = os.path.join(data_path, 'create_tables')

        sql_files = []
        # Loop through the table names and check if the corresponding SQL file exists
        for table in table_creation_order:
            sql_file_path = os.path.join(sql_folder, f"{table}.sql")
            if os.path.exists(sql_file_path):
                sql_files.append(sql_file_path)
            else:
                print(f"Warning: {table} not found in {sql_folder}")

        for sql_file in sql_files:
            with open(sql_file, 'r') as file:
                sql_query = file.read()

                try:
                    self.query(sql_query)
                    print(f"Successfully executed {sql_file}")

                except Exception as e:
                    print(f"Error executing {sql_file}: {str(e)}")
        
        csv_folder = os.path.join(data_path, 'initial_data')  

        # Loop through each table and insert data from corresponding CSV file
        for table in table_creation_order:
            print(table_creation_order)
            csv_file_path = os.path.join(csv_folder, f"{table}.csv")
            if not os.path.exists(csv_file_path):
                print(f"Warning: {table}.csv not found in {csv_folder}")
                continue

            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                columns = next(reader)  
                parameters = [row for row in reader] 

            # Insert data into the corresponding table if the CSV contains data
            if parameters:
                self.insertRows(table=table, columns=columns, parameters=parameters)
            else:
                print(f"Warning: No data found in {table}.csv")

    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        print('I insert things into the database.')

        if not table or not columns:
            print('Error: Table name or columns are missing.')
            return

        # Prepare the SQL query for inserting data into the table. 
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(columns))

        insert_query = f"""
        INSERT IGNORE INTO `{table}` ({columns_str})
        VALUES ({placeholders})
        """
        
        parameters = [
            tuple(None if value == 'NULL' else value for value in row)
            for row in parameters
        ]

        # Execute the insert query for each row in the parameters
        for row in parameters:
            try:
                self.query(insert_query, row)
            except Exception as e:
                print(f"Error inserting into {table}: {str(e)}")

        print('Data inserted successfully!')

    def getResumeData(self):        
        resume_data = defaultdict(lambda: {'positions': {}})

        # Queries below to retrieve data for the tables
        institutions = self.query("""
            SELECT inst_id, type, name, department, address, city, state, zip
            FROM institutions
        """)

        positions = self.query("""
            SELECT position_id, inst_id, title, responsibilities, start_date, end_date
            FROM positions
        """)

        experiences = self.query("""
            SELECT experience_id, position_id, name, description, start_date, end_date, hyperlink
            FROM experiences
        """)

        skills = self.query("""
            SELECT skill_id, experience_id, name, skill_level
            FROM skills
        """)

        # Organize institutions and their details
        for inst in institutions:
            resume_data[inst['inst_id']].update({
                'type': inst['type'],
                'name': inst['name'],
                'department': inst['department'],
                'address': inst['address'],
                'city': inst['city'],
                'state': inst['state'],
                'zip': inst['zip'],
                'positions': {}
            })

        # Organize positions for each institution
        for pos in positions:
            inst_id = pos['inst_id']
            pos_id = pos['position_id']
            resume_data[inst_id]['positions'][pos_id] = {
                'title': pos['title'],
                'responsibilities': pos['responsibilities'],
                'start_date': pos['start_date'],
                'end_date': pos['end_date'],
                'experiences': {}  
            }

        # Organize experiences for each position
        for exp in experiences:
            pos_id = exp['position_id']
            for inst_id in resume_data:
                if pos_id in resume_data[inst_id]['positions']:
                    exp_id = exp['experience_id']
                    resume_data[inst_id]['positions'][pos_id]['experiences'][exp_id] = {
                        'name': exp['name'],
                        'description': exp['description'],
                        'start_date': exp['start_date'],
                        'end_date': exp['end_date'],
                        'hyperlink': exp['hyperlink'],
                        'skills': {}  
                    }
                    break  

        # Organize skills for each experience
        for skill in skills:
            exp_id = skill['experience_id']
            for inst_id in resume_data:
                for pos_id in resume_data[inst_id]['positions']:
                    if exp_id in resume_data[inst_id]['positions'][pos_id]['experiences']:
                        skill_id = skill['skill_id']
                        resume_data[inst_id]['positions'][pos_id]['experiences'][exp_id]['skills'][skill_id] = {
                            'name': skill['name'],
                            'skill_level': skill['skill_level']
                        }
                        break 

        return dict(resume_data) 