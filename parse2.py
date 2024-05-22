import xml.etree.ElementTree as ET
import psycopg2

# Establish connection to your PostgreSQL database
conn = psycopg2.connect("dbname=hackaton user=postgres password=Starmall1977")
cur = conn.cursor()

# Parse the XML file
tree = ET.parse('ФСБЦ_Маш.xml')
root = tree.getroot()

def insert_resource(resource, section_id):
    code = resource.get('Code')
    name = resource.get('Name')
    measure_unit = resource.get('MeasureUnit')
    prices = resource.find('Prices/Price')
    salary_mach = prices.get('SalaryMach') or None
    labour_mach = prices.get('LabourMach') or None
    price_cost_without_salary = prices.get('PriceCostWithoutSalary') or None
    with_relocation = True if prices.get('WithRelocation') == 'true' else False
    driver_code = prices.get('DriverCode') or None
    machinist_category = prices.get('MachinistCategory') or None

    cur.execute("INSERT INTO resources (code, name, measure_unit, salary_mach, labour_mach, price_cost_without_salary, with_relocation, driver_code, machinist_category, section_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                (code, name, measure_unit, salary_mach, labour_mach, price_cost_without_salary, with_relocation, driver_code, machinist_category, section_id))

def insert_sections(section, parent_id=None, category_id=None):
    name = section.get('Name')
    code = section.get('Code')
    type = section.get('Type')
    cur.execute("INSERT INTO sections (name, code, type, parent_id, category_id) VALUES (%s, %s, %s, %s, %s) RETURNING id", 
                (name, code, type, parent_id, category_id))
    section_id = cur.fetchone()[0]
    
    for resource in section.findall('Resource'):
        insert_resource(resource, section_id)
    
    for subsection in section.findall('Section'):
        insert_sections(subsection, section_id, category_id)

def insert_categories(category):
    type = category.get('Type')
    cur.execute("INSERT INTO categories (type) VALUES (%s) RETURNING id", (type,))
    category_id = cur.fetchone()[0]

    for section in category.findall('Section'):
        insert_sections(section, category_id=category_id)

for category in root.findall('.//ResourceCategory'):
    insert_categories(category)

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()
