from sqlalchemy import create_engine

def dtype_mapping():
    return {'object' : 'TEXT',
        'int64' : 'INT',
        'float64' : 'FLOAT',
        'datetime64' : 'DATETIME',
        'bool' : 'TINYINT',
        'category' : 'TEXT',
        'timedelta[ns]' : 'TEXT'}

def mysql_engine(user, password, host, port, database):
    engine = create_engine(f"mysql://{user}:{password}@{host}:{port}/{database}?charset=utf8")
    return engine

def mysql_conn(engine):
    conn = engine.raw_connection()
    return conn

def genarate_table_cols_sql(df):
    dmap = dtype_mapping()
    sql = ""
    headers = df.dtypes.index
    headers_list = [(header, str(df[header].dtypes)) for header in headers]
    for x in headers_list:
        sql += f"{x[0]} {dmap[x[1]]}, "
    return sql[:-2]

def create_mysql_table_schema(df, conn, db, table):
    table_cols_sql = generate_table_cols_sql(df)
    sql = f"USE {db}; CREATE TABLE {table} ({table_cols_sql});"
    cur = conn.cursor()
    cur.execute(sql)
    cur.close()
    conn.commit()

def insert_row(df):
    db_name = 'opgg_ocr'
    table_name = 'lck_2020'
    engine = mysql_engine(user='root', password='', host='localhost', port='3306' database=db_name)
    try :
        create_mysql_table_schema(df=df, conn=mysql_conn(engine), db=db_name, table=table_name)
    except :
        pass
    
    df.to_sql(table_name, con=mysql_conn(engine), if_exists='append', index=False)