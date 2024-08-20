
def test_get_data_qualtiy_rules(client):
    """
    Test the get_quality_rules function.
    """
    response = client.get("/api/get_quality_rules")
    assert response.status_code == 200
    assert response.json == { \
        "Answer": [{
            "name":  "No Empty Rule",
            "description": "Calculates the percantage of empty values in the column.\
            If the percantage is higher than the treshold, the rule is not satisfied.\
            "
            }
    ]}


def test_get_data_quality_rules_table(client):
    """
    Test the get_quality_rules_table function.
    """
    response = client.get("/api/get_quality_rules/1")
    assert response.status_code == 200
    assert response.json == [
        {
            "table_id": 1,
            "connection_id":"conn123",
            "quality_rule": "No Empty Rule",
            "column_name":"testColumn",
            "threshold": "0" 
        }
    ]