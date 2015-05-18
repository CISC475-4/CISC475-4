-- Test data for use in the tests/ test cases.

-- Insertion is done in the order of the schema:
-- Session ( child_id numeric(5) not null,
--           session_id numeric(2) not null )
insert into Session values (12345, 00);
insert into Session values (12345, 01);
insert into Session values (54321, 99);
insert into Session values (33333, 29);
insert into Session values (44444, 31);
insert into Session values (55555, 37);
insert into Session values (    3,  1);

-- Chunk ( child_id numeric(5) not null,
--         session_id numeric(2) not null,
--         time real not null,
--         behavior_id numeric (3),
--         behavior_lvl numeric (1) )
insert into Chunk values (12345, 00, 99.667, 1, 5);
insert into Chunk values (12345, 00, 141.414, 1, 3);
insert into Chunk values (12345, 00, 18.5, 2, 3);
insert into Chunk values (12345, 01, 0.0, 4, 4);
insert into Chunk values (12345, 01, 11, 1, 4);

-- GroupData ( child_id numeric(5) not null,
--             session_id numeric(2) not null,
--             combo_index numeric(3),
--             duration real not null,
--             num_chunks numeric(3) not null,
--             chunk_avg_dur real not null,
--             chunk_max_dur real not null,
--             rate_per_chunk real not null,
--             rate_per_session real not null )
insert into GroupData values (12345, 00, 020, 1.33, 8, 0.66, 2,    4.33, 5.67);
insert into GroupData values (12345, 00, 209, 0.67, 4, 1.33, 4.02, 5.12, 3.18);
insert into GroupData values (12345, 00, 147, 0.33, 2, 0.67, 1.11, 4.89, 0.11);
insert into GroupData values (12345, 01, 111, 1.11, 1, 1.11, 1.11, 1.11, 1.11);

-- SessionMeta ( child_id numeric(3) not null,
--               session_id numeric(2) not null,
--               time_loaded numeric(10) not null,
--               time_modified numeric(10) not null,
--               filename varchar(255) not null );
insert into Session_Meta values (12345, 00, 12345, 12346, 'filename1.xls');
insert into Session_Meta values (12345, 00, 22222, 33333, 'fn2.sql');
insert into Session_Meta values (12345, 00, 21314, 51617, 'meta.meta');
insert into Session_Meta values (12345, 01, 33333, 88888, 'information.xlsx');
