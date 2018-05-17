drop table items;
CREATE TABLE items (
	id SERIAL NOT NULL CONSTRAINT items_pkey PRIMARY KEY
	,upc INT
	,name TEXT
	,size TEXT
	,price FLOAT
	,taxable BOOLEAN
	,sold_by TEXT
	);

CREATE UNIQUE INDEX items_id_uindex ON items (id);


INSERT INTO items (id, upc, name, size, price, taxable, sold_by)
VALUES (4, 30273, 'Apple', 'per	lb', 0.99, false, 'weight');

INSERT INTO items (id, upc, name, size, price, taxable, sold_by)
VALUES (1, 4738561, 'Milk', '1	gallon', 2.89, false, 'count');

INSERT INTO items (id, upc, name, size, price, taxable, sold_by)
VALUES (2, 8897585, 'Bread', '1	loaf', 3.5, false, 'count');

INSERT INTO items (id, upc, name, size, price, taxable, sold_by)
VALUES (5, 3342, 'Banana', '1	each', 0.69, false, 'count');

INSERT INTO items (id, upc, name, size, price, taxable, sold_by)
VALUES (6, 908345, 'Cashews', '16	oz', 6.99, false, 'count');

INSERT INTO items (id, upc, name, size, price, taxable, sold_by)
VALUES (3, 908347, 'Yogurt', '1	container', 1.25, true, 'count');

INSERT INTO items (id, upc, name, size, price, taxable, sold_by)
VALUES (7, 30273, 'Apple', 'per	lb', 1.09, false, 'weight');

INSERT INTO items (id, upc, name, size, price, taxable, sold_by)
VALUES (8, 3342, 'Banana', 'per	lb', 0.56, true, 'weight');

select from items;

drop table orders;
CREATE TABLE orders (
	id SERIAL NOT NULL CONSTRAINT orders_pkey PRIMARY KEY
	,order_id INT
	,customer_id INT
	,item_id INT CONSTRAINT orders_items_id_fk REFERENCES items
	,name TEXT
	,phone TEXT
	,address TEXT
	,delivered BOOLEAN
	,quantity FLOAT
	);

CREATE UNIQUE INDEX orders_id_uindex ON orders (id);



INSERT INTO orders (id, order_id, customer_id, item_id, name, phone, address, delivered, quantity)
VALUES (3, 23, 3456, 1, 'Bob', NULL, NULL, false, 2);

INSERT INTO orders (id, order_id, customer_id, item_id, name, phone, address, delivered, quantity)
VALUES (4, 23, 3456, 2, 'Bob', NULL, NULL, false, 1);

INSERT INTO orders (id, order_id, customer_id, item_id, name, phone, address, delivered, quantity)
VALUES (5, 23, 3456, 3, 'Bob', NULL, NULL, false, 6);

INSERT INTO orders (id, order_id, customer_id, item_id, name, phone, address, delivered, quantity)
VALUES (6, 23, 3456, 5, 'Bob', NULL, NULL, false, 3);

INSERT INTO orders (id, order_id, customer_id, item_id, name, phone, address, delivered, quantity)
VALUES (7, 89, 2239, 4, 'Alice', NULL, NULL, false, 2);

INSERT INTO orders (id, order_id, customer_id, item_id, name, phone, address, delivered, quantity)
VALUES (8, 89, 2239, 6, 'Alice', NULL, NULL, false, 1);

INSERT INTO orders (id, order_id, customer_id, item_id, name, phone, address, delivered, quantity)
VALUES (9, 65, 2239, 1, 'Alice', NULL, NULL, true, 1);

INSERT INTO orders (id, order_id, customer_id, item_id, name, phone, address, delivered, quantity)
VALUES (10, 65, 2239, 3, 'Alice', NULL, NULL, true, 4);

INSERT INTO orders (id, order_id, customer_id, item_id, name, phone, address, delivered, quantity)
VALUES (11, 65, 2239, 2, 'Alice', NULL, NULL, true, 1);


select * from orders;
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
--Question1--
----------------------------------------------------
--------DROP CREATE FOR TO GET ORIGINAL ------------
----------------------------------------------------
with undelivered_orders as (
	select *
	from orders
	where delivered is false
), order_prices as (
	select order_id, item_id, quantity, price, taxable, 0.0925::double precision as tax_rate
	from undelivered_orders as orders
	left join items as items
		on orders.item_id = items.id
)--, cost_calcuation as (
	select order_id, item_id, quantity, price, taxable, tax_rate,
		case when taxable is true
			then (quantity * price) + (quantity * price * tax_rate)
			else quantity * price
		end as item_cost
	from order_prices
;--)


--Question2--
--See above for find the order total
with undelivered_orders as (
	select *
	from orders
	where delivered is false
), order_prices as (
	select order_id, item_id, quantity, price, taxable, 0.0925::double precision as tax_rate
	from undelivered_orders as orders
	left join items as items
		on orders.item_id = items.id
), cost_calcuation as (
	select order_id, item_id, quantity, price, taxable, tax_rate,
		case when taxable is true
			then (quantity * price) + (quantity * price * tax_rate)
			else quantity * price
		end as item_cost
	from order_prices
)
select order_id, sum(item_cost) as order_total, avg(item_cost) as average_order_total
from cost_calcuation
group by order_id
order by order_id asc;

--Question 3--
select * from items order by upc asc;
select * from orders order by item_id asc;

--assuming we want to keep id=8 and id=7 then
update orders
set item_id = 8
where item_id = 5; --alternative can do "where id=6"

update orders
set item_id = 7
where item_id = 4; --alternative can do "where id=7";

delete from items where id in (5, 4);

--It looks like duplicate items are created as the price changes. I made the assumption that as new records
--are inserted into the items table the id increments by 1. So the newest record would have the larger id #
--That being said, a more resonable apporach to this would be to update the size, price, and sold_by
--data for item if they change with an update query
--alternatively we could as a flag for deactivated products e.g., is_current and we can filter on that
--or include date_added in the table and we know to pick the more recent one
--update is best, but performance could be an issue with larger tables
--flag is the easiest to filter on and isn't that much more work
--dates are cumbersome in this case since we'd have write window functions and use group bys to select the latest date

select * from orders order by item_id;

select * from items order by id;







