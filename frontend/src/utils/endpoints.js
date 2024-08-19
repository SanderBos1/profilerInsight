export const API_ENDPOINTS = {
    GET_CONNECTIONS: 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT +   '/api/get_connections',
    DELETE_CONNECTION: connection_id => `http://` + process.env.VUE_APP_FLASK_HOST + ':' +process.env.VUE_APP_FLASK_PORT + `/api/delete_connection/${connection_id}`,
    load_tables: connetion_id => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/load_tables/${connetion_id}`,
    get_table_connection_id: table_id => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/get_connection_id/${table_id}`,
    ingest_connection_tables: connection_id => 'http://' + process.env.VUE_APP_FLASK_HOST +':' + process.env.VUE_APP_FLASK_PORT +  `/api/ingest_connected_tables/${connection_id}`,
    GET_CSV_FILES: 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + '/api/get_all_files',
    DELETE_CSV_FILE: file => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/delete_file/${file}`,
    GET_CSV_COLUMNS: file => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/get_columns_file/${file}`,
    GET_COLUMN_OVERRVIEW: (file, column) => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/file_column_overview/${file}/${column}`,
    UPLOAD_CSV: 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + '/api/upload_file',
    GET_CONNECTED_TABLES: 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + '/api/get_connected_tables',
    get_table_columns: table_id => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/get_columns/${table_id}`,
    get_ingestion_data: (column, table_id) => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/ingest/${table_id}/${column}`,
    get_overview_data: (table, column) => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/profile_column/${table}/${column}`,
    ADD_POSTGRES_CONNECTION: 'http://' + process.env.VUE_APP_FLASK_HOST +  ':' + process.env.VUE_APP_FLASK_PORT + '/api/add_connection',
};