create table users (
    id serial primary key,
    username varchar(255) not null,
    user_id bigint not null unique,
    created_at timestamp default now(),
    updated_at timestamp default now()
);

create table fee (
    id serial primary key,
    fee float not null,
    created_at timestamp default now(),
    updated_at timestamp default now()
);

create table orders (
    id serial primary key,
    link varchar(10000) not null,
    user_id bigint not null,
    price float not null,
    fee int not null,
    size varchar(3) null,
    ready boolean default false,

    created_at timestamp default now(),
    updated_at timestamp default now()
);