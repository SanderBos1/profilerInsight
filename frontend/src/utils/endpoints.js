export const API_ENDPOINTS = {
    DELETE_CONNECTION: connection_id => `http://` + process.env.VUE_APP_FLASK_HOST + ':' +process.env.VUE_APP_FLASK_PORT + `/api/delete_connection/${connection_id}`,
    get_table_connection_id: table_id => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/get_connection_id/${table_id}`,
    ingest_connection_tables: connection_id => 'http://' + process.env.VUE_APP_FLASK_HOST +':' + process.env.VUE_APP_FLASK_PORT +  `/api/ingest_connected_tables/${connection_id}`,
    GET_CSV_FILES: 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + '/api/get_all_files',
    DELETE_CSV_FILE: file => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/delete_file/${file}`,
    GET_CSV_COLUMNS: file => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/get_columns_file/${file}`,
    GET_COLUMN_OVERRVIEW: (file, column) => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/file_column_overview/${file}/${column}`,
    UPLOAD_CSV: 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + '/api/upload_file',
    get_table_columns: table_id => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/get_columns/${table_id}`,
    get_ingestion_data: (column, table_id) => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/ingest/${table_id}/${column}`,
    get_overview_data: (table, column) => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/profile_column/${table}/${column}`,
    

    //db_connetions_component
    GET_CONNECTIONS: 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT +   '/api/get_connections',
    ADD_CONNECTION: 'http://' + process.env.VUE_APP_FLASK_HOST +  ':' + process.env.VUE_APP_FLASK_PORT + '/api/add_connection',

    //connection_tabels_component
    GET_CONNECTED_TABLES: 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + '/api/get_connected_tables',
    LOAD_TABLES: connection_id => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/load_tables/${connection_id}`,
    GET_TABLE_INFO: table_id => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/get_table_info/${table_id}`,

    //qualityRuleComponent
    GET_QUALITY_RULES: 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + '/api/get_quality_rules',
    ADD_QUALITY_RULE: 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + '/api/add_rule',
    DELETE_QUALITY_RULE: rule_id => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/delete_rule/${rule_id}`,
    GET_QUALITY_RULES_TABLE: table_id => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/get_quality_rules/${table_id}`,
    CALCULATE_QUALITY: table_id => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/calculate_quality/${table_id}`,
};