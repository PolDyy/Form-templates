import psycopg2
from conf import DB_HOST, DB_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
from database.queries import CreateQuery, InsertQueries, GetQueries


def with_db_connection(func):
    def wrapper(*args, **kwargs):
        connection = None
        try:

            connection = psycopg2.connect(
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )

            with connection.cursor() as cursor:
                result = func(*args, **kwargs, connection=connection, cursor=cursor)

            connection.commit()
            connection.close()
            return result

        except Exception as e:
            print(f"Ошибка при подключении к базе данных: {e}")
            if connection:
                connection.close()

    return wrapper


@with_db_connection
def create_tables(connection, cursor):
    try:
        cursor.execute(CreateQuery.check_trigger)
        trigger_status = cursor.fetchone()[0]

        cursor.execute(CreateQuery.federal_projects)
        cursor.execute(CreateQuery.federal_orgs)
        cursor.execute(CreateQuery.fed_prj_del)

        if not trigger_status:
            cursor.execute(CreateQuery.init_trigger)

    except Exception as ex:
        print(f"Ошибка запроса: {ex}")


@with_db_connection
def insert_fed_prjs(fed_prj_list, connection, cursor):
    cursor.executemany(InsertQueries.insert_fed_prj, [
        (fed_prj.name, ) for fed_prj in fed_prj_list
    ])


@with_db_connection
def insert_fed_orgs(fed_org_list, connection, cursor):
    cursor.executemany(InsertQueries.insert_fed_org, [
        (fed_org.name,) for fed_org in fed_org_list
    ])


@with_db_connection
def insert_fed_prj_del(fed_prj_del_list, connection, cursor):
    cursor.executemany(InsertQueries.insert_fed_prf_del, [
        (
            data.federal_prj_id, data.federal_org_id, data.prj_date, data.year_no, data.year_plan,
            data.year_achieved_cnt, data.year_achieved_percent, data.year_left_cnt, data.year_left_percent,
            data.year_delayed_cnt, data.year_delayed_percent, data.total_delayed_cnt, data.total_delayed_percent,
            data.created_from, data.created_to, data.relevance_dttm
        ) for data in fed_prj_del_list
    ])


@with_db_connection
def get_fed_prj_id_by_name(fed_prj_name, connection, cursor):
    cursor.execute(GetQueries.get_fed_prj_id_by_name, (fed_prj_name, ))
    fed_prj_id = cursor.fetchone()
    return fed_prj_id[0]


@with_db_connection
def get_fed_org_id_by_name(fed_org_name, connection, cursor):
    cursor.execute(GetQueries.get_fed_org_id_by_name, (fed_org_name, ))
    fed_org_id = cursor.fetchone()
    return fed_org_id[0]


@with_db_connection
def get_all_fed_org(connection, cursor):
    cursor.execute(GetQueries.get_all_fed_org)
    result = cursor.fetchall()
    return result


@with_db_connection
def get_all_fed_prj(connection, cursor):
    cursor.execute(GetQueries.get_all_fed_prj)
    result = cursor.fetchall()
    return result


@with_db_connection
def get_all_fed_prj_del(connection, cursor):
    cursor.execute(GetQueries.get_all_fed_prj_del)
    result = cursor.fetchall()
    return result
