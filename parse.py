import xml.etree.ElementTree as ET
import psycopg2

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect("dbname=hackaton user=postgres password=Starmall1977")
cur = conn.cursor()

# Function to parse and insert data
def parse_and_insert(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for category in root.findall('.//ResourceCategory'):
        type = category.get('Type')
        code_prefix = category.get('CodePrefix')
        cur.execute("INSERT INTO ResourceCategory (type, code_prefix) VALUES (%s, %s) RETURNING category_id", (type, code_prefix))
        category_id = cur.fetchone()[0]

        for section in category.findall('.//Section'):
            name = section.get('Name')
            sect_type = section.get('Type')
            code = section.get('Code')
            cur.execute("INSERT INTO Section (category_id, name, type, code) VALUES (%s, %s, %s, %s) RETURNING section_id", (category_id, name, sect_type, code))
            section_id = cur.fetchone()[0]

            for work in section.findall('.//Work'):
                end_name = work.get('EndName')
                measure_unit = work.get('MeasureUnit')
                work_code = work.get('Code')
                cur.execute("INSERT INTO Work (section_id, end_name, measure_unit, code) VALUES (%s, %s, %s, %s) RETURNING work_id", (section_id, end_name, measure_unit, work_code))
                work_id = cur.fetchone()[0]

                for resource in work.findall('.//Resource'):
                    resource_code = resource.get('Code')
                    end_name = resource.get('EndName')
                    quantity = resource.get('Quantity') or '0'
                    # Convert 'П' to '0' in quantity
                    if quantity == 'П':
                        quantity = '0'
                    cur.execute("INSERT INTO Resource (work_id, code, end_name, quantity) VALUES (%s, %s, %s, %s)", (work_id, resource_code, end_name, float(quantity)))

                for reason in work.findall('.//NrSp'):
                    nr = reason.get('Nr')
                    sp = reason.get('Sp')
                    cur.execute("INSERT INTO ReasonItem (work_id, nr, sp) VALUES (%s, %s, %s)", (work_id, nr, sp))

    # Commit the changes
    conn.commit()

# Call the function with your XML file path
parse_and_insert('ГЭСН.xml')

# Close the cursor and connection
cur.close()
conn.close()
