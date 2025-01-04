import json
import requests
import pandas as pd

# Define global variables
server = ''  # Replace with your actual server URL. for example: https://url.sisense.com
token = ''
path = ''

"""
    Define the path variable according to your operating system and file location
    Example for Windows:
    path = r'C:\\Users\demo.demo\Desktop\sisense_users.csv'
    Example for Mac:
    path = '/Users/demo.demo/Desktop/sisense_users.csv'
"""

# Fixed variables: `user_columns`, `params`, and `headers` are fixed and should not be updated.
user_columns = ['_id','active','roleId','created','tenantId','email','firstName','lastName','userName','lastLogin','lastActivity'] # Define the fields to be retrieved for users
params = {
    "fields": ",".join(user_columns)
}
headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

# Retrieves user data from the specified server endpoint, filters it based on provided user_columns, and returns a DataFrame.
def get_users(server, token, headers, user_columns, params):
    endpoint = '/api/v1/users'
    url = f'{server}{endpoint}'
    try:
        request = requests.get(url=url, headers=headers, params=params)
        request.raise_for_status()  # Check for request success
        respond = request.json()
        user_data = []
        for user in respond:
            user_dict = {}
            for key, value in user.items():
                if key in user_columns:
                    user_dict[key] = value
            user_data.append(user_dict)  # Append dictionary containing all attributes
        return pd.DataFrame(user_data)
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None  # Return None or handle error appropriately


# Modifies the input DataFrame by converting specific columns to datetime format, renaming certain columns, and saving the DataFrame to a CSV file
def modify_df(df_users):
    # Convert columns to datetime format
    df_users["created"] = pd.to_datetime(df_users["created"])
    df_users["lastLogin"] = pd.to_datetime(df_users["lastLogin"])
    df_users["lastActivity"] = pd.to_datetime(df_users["lastActivity"])

    # Rename specific columns in the DataFrame
    df_users.rename(columns={'_id': 'user_id',
                             'userName': 'user_name',
                             'firstName': 'first_name',
                             'lastName': 'last_name',
                             'active': 'is_active',
                             'roleId': 'role_id',
                             'created': 'created_date',
                             'tenantId': 'tenant_id',
                             'lastLogin': 'last_login',
                             'lastActivity': 'last_activity'}, inplace=True)

    # Reorder columns
    ordered_columns = [
        'user_id', 'user_name', 'first_name', 'last_name', 'is_active',
        'role_id', 'created_date', 'tenant_id', 'last_login', 'last_activity'
    ]
    df_users = df_users[ordered_columns]

    # Save the DataFrame to a CSV file without including the index
    df_users.to_csv(path, index=False)
    return df_users

# Retrieve users data using the get_users function
df_users = get_users(server, token, headers, user_columns, params)

# Modify df_users data frame into the final output
df_result = modify_df(df_users)

# Print the first few rows of the modified DataFrame
print(df_result.head())

# Print a message indicating the end of the program
print("program completed")

