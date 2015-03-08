-- This file will create the tables we'll use to store the study's data.

-- Notes about the SQLite3 DDL:
--  A column type with the substring "INT" gets -> the integer affinity
--  ("CHAR", "CLOB", "TEXT") -> text
--  "BLOB" -> none
--  ("REAL", "FLOA", "DOUB") -> float
--  else -> numeric

--
--    This schema assumes that the database, tables, and default
--    data do not already exist! If you've already generated your
--    database schema, you don't need to use this file.
--

-- This table will store the Attention Component Codes
-- We should have parts of the GUI allow her to add new columns if needed (e.g. if they
-- measure a new ReplaceCode). 
-- Note that this data is extremely redundant: we could make a new table that maps
-- ReplaceCodes to Levels, for example, since so many of the rows in this table will have
-- the same Level values. However, if she wants to add multiple Levels of (model), for
-- example, that would complicate things, so I left it as one table for now.
create table component (
	Type text not null,
	-- SQLite also supports 'checks', e.g. "check (Code == '\(%\)')"
	Code text default '()',
	ReplaceCode text default '(missing)',
	Level integer default -1,
	-- Column integer default 1, -- Which column in the .xlsx this is.
	-- ^ We can figure that out with the primary key if needed.
	primary key ( Type, ReplaceCode )
);


-- This begins a transaction, which makes inserting a bunch of rows at
-- once a little bit quicker. It just buffers them until it's told to
-- put them into the database.
begin;

-- These are the summary data for each table as given to us by Anjana.
-- They obviously follow a few naming patterns: Codes with 'm' will have 'model' ReplaceCodes,
-- etc.. I don't think she was very explicit about it though. Also, the data columns she gave
-- us all have some combination of Type and ReplaceCode, which is why they're the primary keys.

-- The first bunch are for Attention, i.e. 'Att_' in the .xlsx columns
insert into component (Type, Code, ReplaceCode, Level) values ('Att_','()','(missing)',-1);
insert into component (Type, Code, ReplaceCode, Level) values ('Att_','(n)','(null)',0);
insert into component (Type, Code, ReplaceCode, Level) values ('Att_','(nv)','(null)',0);
insert into component (Type, Code, ReplaceCode, Level) values ('Att_','(a)','(away)',1);
insert into component (Type, Code, ReplaceCode, Level) values ('Att_','(i)','(prop)',2);
insert into component (Type, Code, ReplaceCode, Level) values ('Att_','(r)','(robot)',3);
insert into component (Type, Code, ReplaceCode, Level) values ('Att_','(rr)','(robot)',3);
insert into component (Type, Code, ReplaceCode, Level) values ('Att_','(rs)','(robot)',3);
insert into component (Type, Code, ReplaceCode, Level) values ('Att_','(g)','(group)',4);
insert into component (Type, Code, ReplaceCode, Level) values ('Att_','(gr)','(group)',4);
insert into component (Type, Code, ReplaceCode, Level) values ('Att_','(gs)','(group)',4);
insert into component (Type, Code, ReplaceCode, Level) values ('Att_','(m)','(model)',5);
insert into component (Type, Code, ReplaceCode, Level) values ('Att_','(mr)','(model)',5);
insert into component (Type, Code, ReplaceCode, Level) values ('Att_','(ms)','(model)',5);
insert into component (Type, Code, ReplaceCode, Level) values ('Att_','(t)','(trainer)',5);
insert into component (Type, Code, ReplaceCode, Level) values ('Att_','(tr)','(trainer)',5);
insert into component (Type, Code, ReplaceCode, Level) values ('Att_','(ts)','(trainer)',5);

-- The next bunch are for Affect ('Aff_').
insert into component (Type, Code, ReplaceCode, Level) values ('Aff_','()','(missing)',-1);
insert into component (Type, Code, ReplaceCode, Level) values ('Aff_','(x)','(null)',0);
insert into component (Type, Code, ReplaceCode, Level) values ('Aff_','(r)','(null)',0);
insert into component (Type, Code, ReplaceCode, Level) values ('Aff_','(nv)','(null)',0);
insert into component (Type, Code, ReplaceCode, Level) values ('Aff_','(o)','(negative)',1);
insert into component (Type, Code, ReplaceCode, Level) values ('Aff_','(n)','(negative)',1);
insert into component (Type, Code, ReplaceCode, Level) values ('Aff_','(m)','(neutral)',2);
insert into component (Type, Code, ReplaceCode, Level) values ('Aff_','(i)','(interest)',3);
insert into component (Type, Code, ReplaceCode, Level) values ('Aff_','(s)','(smile)',4);
insert into component (Type, Code, ReplaceCode, Level) values ('Aff_','(ss)','(smile)',4);
insert into component (Type, Code, ReplaceCode, Level) values ('Aff_','(st)','(smile)',4);
insert into component (Type, Code, ReplaceCode, Level) values ('Aff_','(v)','(smile)',4);
insert into component (Type, Code, ReplaceCode, Level) values ('Aff_','(vs)','(smile)',4);
insert into component (Type, Code, ReplaceCode, Level) values ('Aff_','(vc)','(smile)',4);
insert into component (Type, Code, ReplaceCode, Level) values ('Aff_','(vm)','(smile)',4);
insert into component (Type, Code, ReplaceCode, Level) values ('Aff_','(vt)','(smile)',4);

-- This last chunk is for Verbal ('Ver_')
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','()','(missing)',-1);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(n)','(quiet)',0);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(s)','(self)',1);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(er)','(self)',1);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(es)','(self)',1);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(sr)','(self)',1);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(ss)','(self)',1);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(v)','(self)',1);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(vr)','(self)',1);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(vs)','(self)',1);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(css)','(self)',1);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(a)','(self)',1);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(ar)','(self)',1);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(as)','(self)',1);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(r)','(self)',1);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(wss)','(self)',1);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(rr)','(robot)',2);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(rs)','(robot)',2);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(wos)','(robot)',2);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(wor)','(robot)',2);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(cos)','(robot)',2);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(cor)','(robot)',2);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(w)','(trainer)',4);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(wr)','(trainer)',4);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(ws)','(trainer)',4);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(wms)','(model)',3);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(wmr)','(model)',3);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(wts)','(trainer)',4);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(wtr)','(trainer)',4);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(wps)','(caregiver)',3);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(wpr)','(caregiver)',3);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(cms)','(model)',3);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(cmr)','(model)',3);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(cts)','(trainer)',4);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(ctr)','(trainer)',4);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(cps)','(caregiver)',3);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(cpr)','(caregiver)',3);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(o)','(caregiver)',3);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(or)','(caregiver)',3);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(os)','(caregiver)',3);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(c)','(model)',3);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(cr)','(model)',3);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(cs)','(model)',3);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(t)','(trainer)',4);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(tr)','(trainer)',4);
insert into component (Type, Code, ReplaceCode, Level) values ('Ver_','(ts)','(trainer)',4);

-- This executes all of the insert queries above.
commit;
