CREATE EXTERNAL TABLE transactions_v2 (
    transaction_id INT,
    user_id INT,
    amount DOUBLE,
    currency STRING,
    transaction_date DATE,
    is_fraud INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',' 
STORED AS TEXTFILE
LOCATION 's3a://ваш-бакет/transactions/'
TBLPROPERTIES ('skip.header.line.count'='1'); 

CREATE EXTERNAL TABLE logs_v2 (
    log_id INT,
    transaction_id INT,
    category STRING,
    log_time TIMESTAMP
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t' 
STORED AS TEXTFILE
LOCATION '';