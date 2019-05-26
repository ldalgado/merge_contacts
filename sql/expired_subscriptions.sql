create table t_subscription
(
    subscription_id        INT,
    user_id                INT,
    product_id             INT,
    subscription_startdate TIMESTAMP,
    subscription_enddate   TIMESTAMP
);

create table t_user
(
    user_id     INT,
    login_id    VARCHAR(250),
    email       VARCHAR(250),
    full_name   VARCHAR(250),
    create_date TIMESTAMP
);


create table t_product
(
    product_id          INT,
    product_name        VARCHAR(250),
    product_description VARCHAR(250)
);


insert into t_subscription values (1, 1, 1, '2018-09-01', '2018-09-20'); -- user 1 product 1 active before 3rd quarter
insert into t_subscription values (2, 2, 1, '2018-09-01', '2018-10-20'); -- user 2 product 1 active start of  3rd quarter
insert into t_subscription values (3, 3, 1, '2018-10-20', '2018-11-20'); -- user 3 product 1 active middle of  3rd quarter
insert into t_subscription values (4, 4, 1, '2018-10-20', '2019-01-20'); -- user 4 product 1 active end of  3rd quarter
insert into t_subscription values (5, 5, 1, '2019-01-01', '2019-02-20'); -- user 5 product 1 active after 3rd quarter

-- user 2 and 3 and 4 should be in result because they were active in third quarter but not active now

insert into t_subscription values (1, 1, 2, '2018-09-01', '2018-09-20'); -- user 1 product 1 active before 3rd quarter
insert into t_subscription values (2, 2, 2, '2018-09-01', '2018-10-20'); -- user 2 product 1 active start of  3rd quarter
insert into t_subscription values (3, 3, 2, '2018-10-20', '2018-11-20'); -- user 3 product 1 active middle of  3rd quarter
insert into t_subscription values (4, 4, 2, '2018-10-20', '2019-01-20'); -- user 4 product 1 active end of  3rd quarter
insert into t_subscription values (5, 5, 2, '2019-01-01', '2019-02-20'); -- user 5 product 1 active after 3rd quarter
-- same set of users for product 2

insert into t_subscription values (6, 6, 1, '2018-09-01', '2018-09-20'); -- user 6 product 1 active before 3rd quarter  and active now  SHOULD NOT BE IN RESULT
insert into t_subscription values (7, 6, 1, '2019-01-01', '2019-12-31'); -- user 6 product 1 active before 3rd quarter  and active now  SHOULD NOT BE IN RESULT

insert into t_subscription values (8, 7, 1, '2018-09-01', '2018-10-20'); -- user 7 product 1 active start of  3rd quarter and active now SHOULD NOT BE IN RESULT
insert into t_subscription values (9, 7, 1, '2019-01-01', '2019-12-31'); -- user 7 product 1 active start of  3rd quarter and active now SHOULD NOT BE IN RESULT

insert into t_subscription values (10, 8, 1,  '2018-10-20', '2018-11-20'); -- user 8 product 1 active middle of  3rd quarter and active now SHOULD NOT BE IN RESULT
insert into t_subscription values (11, 8, 1, '2019-01-01', '2019-12-31'); -- user 8 product 1 active middle of  3rd quarter and active now SHOULD NOT BE IN RESULT

insert into t_subscription values (12, 9, 1,  '2018-10-20', '2019-01-20'); -- user 9 product 1 active end of  3rd quarter and active now SHOULD NOT BE IN RESULT
insert into t_subscription values (13, 9, 1, '2019-01-01', '2019-12-31'); -- user 9 product 1 active end of  3rd quarter and active now SHOULD NOT BE IN RESULT


insert into t_subscription values (14, 10, 1, '2019-01-01', '2019-02-20'); -- user 10 product 1 active after   3rd quarter and active now SHOULD NOT BE IN RESULT
insert into t_subscription values (15, 10, 1, '2019-01-01', '2019-12-31'); -- user 10 product 1 activeafter of  3rd quarter and active now SHOULD NOT BE IN RESULT
commit;

-- Given the tables below , for email marketing campaign, can you pull out all usernames of
-- people who had an active subscription during Q4 2018 and are not active now:


-- ASSUMPTION 1: BREAKDOWN BY PRODUCT. IF WE DO NOT WANT BREAKDOWN BY PRODUCT, WE SHOULD REMOVE PRODUCT ID FROM GROUP BY AND HAVING CLAUSE
-- ASSUMPTIOn 2: USER CAN HAVE MULTIPLE SUBSCRIPTIONS TO THE SAME PRODUCT IN OVERLAPPING DATE RANGES

select subscription_aggregate.user_id
--        ,subscription_aggregate.product_id,
--        full_name,
--        product_name,
--        subscriptions_active_in_fourth_quarter,
--       subscriptions_active_now
from (
         select user_id,
                product_id,
                sum(subscription_active_in_fourth_quarter) as subscriptions_active_in_fourth_quarter,
                sum(subscription_active_now)               as subscriptions_active_now
         from (
                  select user_id,
                         product_id,
                         if(subscription_enddate > '2018-10-01' and subscription_startdate < '2018-12-31', 1,0)  as subscription_active_in_fourth_quarter,
                         if(subscription_enddate > now() and subscription_startdate < now(), 1,0) as subscription_active_now
                  from t_subscription
              ) subsriptions
         group by user_id, product_id
         having sum(subscription_active_in_fourth_quarter) > 0
            and sum(subscription_active_now) < 1
     ) subscription_aggregate
         left join t_product on t_product.product_id
         left join t_user on t_user.user_id