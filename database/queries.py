

class CreateQuery:

    federal_projects = """
    CREATE TABLE IF NOT EXISTS federal_projects (
    id SERIAL PRIMARY KEY,
    name TEXT
    );
"""
    federal_orgs = """
    CREATE TABLE IF NOT EXISTS federal_organizations (
    id SERIAL PRIMARY KEY,
    name TEXT
    );
    """

    fed_prj_del = """
    CREATE TABLE IF NOT EXISTS federal_projects_delayed (
    id SERIAL PRIMARY KEY,
    federal_prj_id INT REFERENCES federal_projects (id),
    federal_org_id INT REFERENCES federal_organizations (id),
    prj_date TIMESTAMPTZ,
    year_no INT,
    year_plan INT,
    year_achieved_cnt INT,
    year_achieved_percent FLOAT,
    year_left_cnt INT,
    year_left_percent FLOAT,
    year_delayed_cnt INT,
    year_delayed_percent FLOAT,
    total_delayed_cnt INT,
    total_delayed_percent FLOAT,
    created_from TIMESTAMPTZ,
    created_to TIMESTAMPTZ,
    relevance_dttm TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
    );
    
    """

    init_trigger = """
    CREATE OR REPLACE FUNCTION update_updated_at()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at := NOW();
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    
    CREATE TRIGGER update_updated_at_trigger
    BEFORE UPDATE ON federal_projects_delayed 
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

    """

    check_trigger = """
    SELECT EXISTS (
    SELECT 1
    FROM information_schema.triggers
    WHERE event_object_schema = 'public'
    AND event_object_table = 'federal_projects_delayed'
    AND trigger_name = 'update_updated_at_trigger'
    );

    """


class InsertQueries:

    insert_fed_prj = "INSERT INTO federal_projects (name) VALUES (%s);"

    insert_fed_org = "INSERT INTO federal_organizations (name) VALUES (%s);"

    insert_fed_prf_del = """ 
    INSERT INTO federal_projects_delayed ( 
    federal_prj_id, federal_org_id, prj_date, year_no, year_plan, year_achieved_cnt, year_achieved_percent,
    year_left_cnt, year_left_percent, year_delayed_cnt, year_delayed_percent, total_delayed_cnt,
    total_delayed_percent, created_from, created_to, relevance_dttm ) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
     """


class GetQueries:

    get_fed_prj_id_by_name = """ 
    SELECT id FROM federal_projects
    WHERE name = %s;
    """

    get_fed_org_id_by_name = """
    SELECT id FROM federal_organizations
    WHERE name = %s;
     """

    get_all_fed_prj_del = """ 
    SELECT * FROM federal_projects_delayed;
    """

    get_all_fed_prj = """ 
    SELECT * FROM federal_projects;
    """

    get_all_fed_org = """ 
    SELECT * FROM federal_organizations;
    """
