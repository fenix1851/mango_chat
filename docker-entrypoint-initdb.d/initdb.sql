CREATE TABLE IF NOT EXISTS message_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    mime VARCHAR(255) NOT NULL
);
INSERT INTO message_type (id, name, mime) VALUES (1, 'text', 'text/plain');
INSERT INTO message_type (id, name, mime) VALUES (2, 'html', 'text/html');
INSERT INTO message_type (id, name, mime) VALUES (3, 'json', 'application/json');
INSERT INTO message_type (id, name, mime) VALUES (4, 'xml', 'application/xml');
INSERT INTO message_type (id, name, mime) VALUES (5, 'binary', 'application/octet-stream');
INSERT INTO message_type (id, name, mime) VALUES (6, 'image', 'image/jpeg');
INSERT INTO message_type (id, name, mime) VALUES (7, 'pdf', 'application/pdf');
INSERT INTO message_type (id, name, mime) VALUES (8, 'csv', 'text/csv');
INSERT INTO message_type (id, name, mime) VALUES (9, 'excel', 'application/vnd.ms-excel');
INSERT INTO message_type (id, name, mime) VALUES (10, 'word', 'application/msword');
INSERT INTO message_type (id, name, mime) VALUES (11, 'zip', 'application/zip');
INSERT INTO message_type (id, name, mime) VALUES (12, 'gzip', 'application/gzip');
INSERT INTO message_type (id, name, mime) VALUES (13, 'tar', 'application/tar');
INSERT INTO message_type (id, name, mime) VALUES (14, 'audio', 'audio/mpeg');
INSERT INTO message_type (id, name, mime) VALUES (15, 'video', 'video/mp4');
INSERT INTO message_type (id, name, mime) VALUES (16, 'rtf', 'application/rtf');
INSERT INTO message_type (id, name, mime) VALUES (17, 'yaml', 'application/x-yaml');
INSERT INTO message_type (id, name, mime) VALUES (18, 'javascript', 'application/javascript');
INSERT INTO message_type (id, name, mime) VALUES (19, 'css', 'text/css');
INSERT INTO message_type (id, name, mime) VALUES (20, 'svg', 'image/svg+xml');
INSERT INTO message_type (id, name, mime) VALUES (21, 'markdown', 'text/markdown');
INSERT INTO message_type (id, name, mime) VALUES (22, 'protobuf', 'application/protobuf');
INSERT INTO message_type (id, name, mime) VALUES (23, 'avro', 'application/avro');
INSERT INTO message_type (id, name, mime) VALUES (24, 'parquet', 'application/parquet');
INSERT INTO message_type (id, name, mime) VALUES (25, 'orc', 'application/orc');



