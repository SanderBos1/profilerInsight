from src.data_quality import EmptyValuesRule, PatternRule


def test_get_data_qualtiy_rules(client):
    """
    Test the get_quality_rules function.
    """
    response = client.get("/api/get_quality_rules")
    assert response.status_code == 200
    assert response.json == { \
        "Answer": [EmptyValuesRule().get_rule_description(), PatternRule().get_rule_description()
    ]}


def test_get_data_quality_rules_table(client):
    """
    Test the get_quality_rules_table function.
    """
    table_id = 1
    response = client.get(f"/api/get_quality_rules/{table_id}")
    assert response.status_code == 200
    assert response.json == {"Answer": [
            {
                'rule_id': 1, 
                'table_id': 1, 
                'connection_id': 'conn123', 
                'quality_rule': 'No Empty Rule', 
                'column_name': 'testColumn', 
                'threshold': 1.0, 
                'extra_info': None,
                'calculated_threshold': None, 
                'succeded': False
            }]
        }
    
def test_add_quality_rule(client):
    """
    Test the add_quality_rule function.
    """
    data = {
        "table_id": 1,
        "rule_name": "No Empty Rule",
        "column_name": "testColumn",
        "threshold": 1.0
    }
    response = client.post("/api/add_rule", json=data)
    assert response.status_code == 200
    assert response.json == {"Message": "Quality rule added successfully"}

def test_delete_quality_rule(client):
    """
    Test the delete_quality_rule function.
    """
    rule_id = 1
    response = client.delete(f"/api/delete_rule/{rule_id}")
    assert response.status_code == 200
    assert response.json == {"Message": "Quality rule deleted successfully"}

def test_delete_quality_rule_not_found(client):
    """
    Test the delete_quality_rule function when the rule is not found.
    """
    rule_id = 100
    response = client.delete(f"/api/delete_rule/{rule_id}")
    assert response.status_code == 404
    assert response.json == {"Error": "Rule not found"}