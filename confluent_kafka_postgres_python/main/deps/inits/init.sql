CREATE DATABASE kafka_persistent;

\c kafka_persistent;

CREATE EXTENSION pgcrypto;

CREATE TABLE kafka_persistent_data(
    msg_id UUID NOT NULL DEFAULT gen_random_uuid(),
    date_added TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    kafka_topic_name VARCHAR(100) NOT NULL DEFAULT 'kafka_default',
    kafka_message JSONB,
    UNIQUE(date_added, kafka_topic_name, kafka_message),
    PRIMARY KEY(msg_id)
);
-- ) PARTITION BY LIST(kafka_topic_name);