import pandas as pd
import sqlite3

db = 'nova_sphere.db'

conn = sqlite3.connect(db)
pd.set_option('display.max_columns', None)

# import data, renaming columns
internal = pd.read_csv('NovaSphere_internal_db_Test.csv', encoding='UTF-16-LE', sep='\t')
issued = pd.read_excel('NovaSphere_Issued_Test.xlsx')
leads = pd.read_excel('NovaSphere_Leads_Test.xlsx')
sets = pd.read_excel('NovaSphere_Sets_Test.xlsx')
tasks = pd.read_excel('NovaSphere_Tasks_Test.xlsx')

internal['Created time'] = pd.to_datetime(internal['Created time'], errors='coerce')
internal.rename(columns={'Nova Sphere Id': 'nova_sphere_id', 'Created time': 'form_time', 'Source': 'source',
                         'Landing page': 'landing_page', 'Thank You page': 'thank_you_page'},
                inplace=True)
leads.rename(columns={'Created Time': 'crm_time', '# Call Center Tasks Completed': 'call_center_tasks',
                      'Nova Sphere ID': 'nova_sphere_id', 'Contact ID': 'contact_id', 'Region': 'region'},
             inplace=True)
sets.rename(columns={'Date': 'appointment_date', 'Created Date': 'created_appointment_date',
                     'Created Time': 'appointment_time', 'Status': 'status', 'Contact: Contact ID': 'contact_id'},
            inplace=True)
tasks.rename(columns={'Created Time': 'call_time', 'Call Result': 'call_result', 'Nova Sphere ID': 'nova_sphere_id',
                      'Converted Contact: Contact ID': 'contact_id'},
             inplace=True)
issued.rename(columns={'Net Sales': 'net_sale', 'Gross Sales': 'gross_sale', 'Cancelled Sales': 'cancel_sale',
                       'Date': 'issued_date', 'Created Date': 'created_issued_date', 'Created Time': 'created_time',
                       'Status': 'status', 'Contact: Contact ID': 'contact_id'},
              inplace=True)

internal.to_sql('internal', conn, if_exists='replace', index=False)
leads.to_sql('leads', conn, if_exists='replace', index=False)
sets.to_sql('sets', conn, if_exists='replace', index=False)
tasks.to_sql('tasks', conn, if_exists='replace', index=False)
issued.to_sql('issued', conn, if_exists='replace', index=False)
conn.commit()

# create the single data source with SQL
query = ("""
WITH ranked_calls AS (
    SELECT
        nova_sphere_id,
        i.form_time,
        l.crm_time,
        l.region,
        l.contact_id,
        i.source,
        i.landing_page,
        i.thank_you_page,
        t.call_result,
        t.call_time,
        s.created_appointment_date,
        s.appointment_date,
        g.status,
        g.gross_sale,
        g.net_sale,
        g.cancel_sale,
        ROW_NUMBER() OVER (PARTITION BY nova_sphere_id ORDER BY t.call_time DESC) AS max_rank,
        ROW_NUMBER() OVER (PARTITION BY nova_sphere_id ORDER BY t.call_time ASC) AS min_rank
    FROM internal i 
        LEFT JOIN leads l using (nova_sphere_id) 
        LEFT JOIN tasks t using (nova_sphere_id) 
        LEFT JOIN sets s using (contact_id)
        LEFT JOIN issued g using (contact_id)
)

    SELECT 
        nova_sphere_id,
        form_time,
        crm_time,
        created_appointment_date,
        appointment_date,
        region,
        source,
        landing_page,
        thank_you_page,
        MAX(CASE WHEN min_rank = 1 THEN call_time END) AS first_call_date,
        MAX(CASE WHEN min_rank = 1 THEN call_result END) AS first_call_result,
        MAX(CASE WHEN max_rank = 1 THEN call_time END) AS last_call_date,
        MAX(CASE WHEN max_rank = 1 THEN call_result END) AS last_call_result,
        status as appointment_result,
        gross_sale,
        net_sale,
        cancel_sale
    FROM ranked_calls
    group by nova_sphere_id
;
""")
nova_sphere = pd.read_sql_query(query, conn)
nova_sphere.to_sql('nova_sphere', conn, if_exists='replace', index=False)
nova_sphere.to_csv('nova_sphere.csv', index=False)
print(nova_sphere.columns.tolist())

# create query to answer analytics report
query2 = """
SELECT
    round(sum(net_sale) / 10.0 / count(nova_sphere_id),2) as revenue_x_lead
FROM nova_sphere
where region is not null;"""

result_2 = pd.read_sql_query(query2, conn)
print(result_2)

query3 = """
SELECT
    round(COUNT(appointment_date) / 1.0 / COUNT(region),3) as "Set rate (sum(appointments)/sum(Leads))" 
FROM nova_sphere
;
"""

result_3 = pd.read_sql_query(query3, conn)
print(result_3)

query4 = """
SELECT 
    "n_leads" as step, count(region) as value , 1 as ratio from nova_sphere
    union SELECT "n_leads_called", count(last_call_date) + count(appointment_date),
        round((count(last_call_date) + count(appointment_date))/1.0/count(region),2) from nova_sphere
    union SELECT "n_appointment", count(appointment_date),
        round(count(appointment_date)/1.0/(count(last_call_date) + count(appointment_date)),2)  from nova_sphere
    union SELECT "n_agree_to_sale", SUM(CASE WHEN gross_sale != 0 THEN 1 ELSE 0 END), 
        ROUND(SUM(CASE WHEN gross_sale != 0 THEN 1 ELSE 0 END) / 1.0 / COUNT(appointment_date), 2) from nova_sphere
    union SELECT "n_sale", SUM(CASE WHEN net_sale != 0 THEN 1 ELSE 0 END), 
        ROUND(SUM(CASE WHEN net_sale != 0 THEN 1 ELSE 0 END) / 1.0 / SUM(CASE WHEN gross_sale != 0 THEN 1 ELSE 0 END),2) 
from nova_sphere
order by value desc
"""

result_4 = pd.read_sql_query(query4, conn)
print(result_4)

conn.close()
