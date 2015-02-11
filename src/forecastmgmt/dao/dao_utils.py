

from forecastmgmt.dao.db_connection import get_db_connection
from forecastmgmt.model.person import Person
import psycopg2.extras

def enum_retrieve_valid_values(enum_type):
    enum_values_list=[]
    cur = get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cur.execute(""" 
            select 
                e.enumlabel as enum_value
            from 
                pg_type t 
            join 
                pg_enum e 
            on 
                t.oid = e.enumtypid  
            join 
                pg_catalog.pg_namespace n 
            ON 
                n.oid = t.typnamespace
            where
	            t.typname='%s'
            """ % enum_type)
    for enum_values in cur.fetchall():
        enum_values_list.append(enum_values.enum_value)
    cur.close()
    return enum_values_list

