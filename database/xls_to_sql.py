import pandas as pd

# Define the Excel file path
excel_file = '../backend/Input.xlsx'

# Read the Excel file
excel_data = pd.read_excel(excel_file, sheet_name=None)

# Define the SQL file path
sql_file = 'smartcharge.sql'

# Open the SQL file in write mode
with open(sql_file, 'w') as f:
    # Iterate over each sheet in the Excel file
    for sheet_name, sheet_data in excel_data.items():
        # Get the column names
        columns = sheet_data.columns.tolist()

        # Generate the CREATE TABLE statement
        create_table_statement = f"CREATE TABLE {sheet_name} (\n"
        for column in columns:
            create_table_statement += f"    {column} VARCHAR,\n"
        create_table_statement = create_table_statement.rstrip(",\n") + "\n);"

        # Write the CREATE TABLE statement to the SQL file
        f.write(create_table_statement)
        f.write("\n\n")

        # Generate the INSERT INTO statements
        insert_into_statements = []
        for _, row in sheet_data.iterrows():
            values = row.tolist()
            if any(pd.notnull(values)):
                insert_into_statement = f"INSERT INTO {sheet_name} VALUES ({', '.join(map(str, values))});"
                insert_into_statements.append(insert_into_statement)

        # Write the INSERT INTO statements to the SQL file
        f.write("\n".join(insert_into_statements))
        f.write("\n\n")
