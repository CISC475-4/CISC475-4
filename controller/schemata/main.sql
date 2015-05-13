-- This file represents the database schema that we agreed on 03/12/2015

-- Session Table
--
-- Unique combination of child and session ID, with the D- stripped from the beginning
create table if not exists Session(
	child_id numeric(5) not null,
	session_id numeric(2) not null,
	primary key (child_id, session_id)
);
-- Single time records for all Sessions
--
-- behavior_id is something like 1, and behavior_lvl is the amount between 1 and 5
-- The behaviors will have to be translated using the code table later
-- Note: changed individual behavior column to a pair of id and lvl
create table if not exists Chunk(
	child_id numeric(5) not null,
	session_id numeric(2) not null,
	time real not null,
  behavior_id numeric(3),
  behavior_lvl numeric(1),
	primary key(child_id, session_id, time),
	foreign key(child_id, session_id) references Session
);
-- Group Data from the "AllGroupData" sheet
--
-- All the avg- columns are skipped, as they're simple to calculate 
create table if not exists GroupData(
	child_id numeric(5) not null,
	session_id numeric(2) not null,
	combo_index numeric(3),
	duration real not null,
	num_chunks numeric(3) not null,
	chunk_avg_dur real not null,
	chunk_max_dur real not null,
	rate_per_chunk real not null,
	rate_per_session real not null,
	primary key (combo_index, child_id, session_id),
	foreign key(child_id, session_id) references Session
);
-- Metadata about a Session. Includes things like the file it was loaded up from
--
-- Times are stored as numerics because they'll be 10 digit long UNIX timestamps
-- Note: removed session_name from this. No name is assigned to a session beyond ID
create table if not exists Session_Meta(
	child_id numeric(5) not null,
	session_id numeric(2) not null,
	time_loaded numeric(10) not null,
	time_modified numeric(10) not null,
	filename varchar(255) not null,
  primary key (filename, child_id, session_id),
	foreign key(child_id, session_id) references Session
);
