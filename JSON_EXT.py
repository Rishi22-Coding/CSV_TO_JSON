import json
import csv
from numpy import true_divide
import pandas
path = 'data.csv'
data = pandas.read_csv(path, index_col=0)
# print(data)

labDatas = {}

def parametersData(parameter):
    return  {
                "Parameter Code": parameter["Parameter Code"] if parameter["Parameter Code"]!="NaN" else 'NULL',
                "Parameter Name": parameter["Parameter Name"] if parameter["Parameter Name"]!="NaN" else 'NULL',
                "Units": parameter["Units"] if parameter["Units"]!="NaN" else 'NULL',
                "Result": parameter["Result"] if parameter["Result"]!="NaN" else 'NULL',
                "Low Range": parameter["Low Range"] if parameter["Low Range"]!="NaN" else 'NULL',
                "High Range": parameter["High Range"] if parameter["High Range"]!="NaN" else 'NULL'
    }


for indx, row in data.iterrows():
    # print("Index:-", indx)
    # print("row:-", row)
    if not labDatas.get(indx):
        labDatas[indx] = {   
                            "Lab Number": indx, 
                            "age": row['age'],
                            "Panels": [{   
                                "panel_code": row['panel_code'], 
                                "panel_name": row["panel_name"],
                                "Parameters": [parametersData(row)]
                            }],
                        }
    else:
        for panel in labDatas[indx]["Panels"]: 
            if panel.get("panel_code")!=row["panel_code"]:
                labDatas[indx]["Panels"].append({
                    "panel_code": row['panel_code'], 
                    "panel_name": row["panel_name"],
                    "Parameters": [parametersData(row)]
                })
                break
            else:
                is_panel_code_parameter_code_unique=True
                for parameter in panel["Parameters"]:
                    if parameter.get("Parameter Code")==row["Parameter Code"]:
                        is_panel_code_parameter_code_unique=False
                        break
                if is_panel_code_parameter_code_unique:
                    panel["Parameters"].append(parametersData(row))
    # print(row)
    # if row["Parameter Code"]==29322:
    #     break

# print(labDatas)

for labDataKey, labDataValue in labDatas.items():
    with open(str(labDataKey)+'.json', 'w') as f:
        json.dump(labDataValue, f, indent=2)
        print("New json file is created from data.json file")
