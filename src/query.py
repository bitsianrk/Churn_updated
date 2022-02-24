class Queries:

    def __init__(self):
        pass

    def get_train_queries(self):
        return {
            "metadata_query_curr": """with base as (select bs.businessid 
                                     , date(bs.onboarddatenew) as onboarddate
                                     , bs.businesstype 
            from 
            business_snapshot bs 
            where date(bs.onboarddatenew) <= '2022-02-18')
    
            select b.businessid, b.onboarddate, b.businesstype, 
    
            max(date(ord.src_created_time)) as max_order_dt,
            count(distinct ord.order_id) as total_orders,
            count(distinct(date(ord.src_created_time))) as distinct_order_dates
    
    
            from base b
            left join customer_snapshot_ c  on b.businessid = c.businessid
            left join(
                      select * from  bolt_order_item_snapshot_ bos
                      where date(bos.src_created_time) <= '2022-02-18'
                      and bos.boltordertype = 'MARKETPLACE'
                      ) as ord
                      on c.customerid = ord.buyer_id
            left join address_snapshot_ ads ON ads.addressentityid = b.businessid
            left join listing_snapshot ls on ls.listing_id = ord.listing_id
            left join sellerproduct_snapshot sps on sps.sp_id = ls.sp_id
            left join product_snapshot_ prod on prod.jpin = sps.jpin
            left join category cat on cat.pvid = prod.pvid
    
            where 
    
            b.businessid not in ('BZID-testPuja'
                            , 'BZID-tech'
                            , 'BZID-sajal'
                            , 'BZID-merchCatalog'
                            , 'BZID-1304457254'
                            , 'BZID-1304463418')
    
            AND c.istestcustomer IS FALSE
            --and ads.addresstype = 'SHIPPING'
    
    
            --AND date(ord.src_created_time) <= '2021-01-14'
    
    
            group by 1,2,3
    
    
            """,
            "metadata_query_curr2": """with base as (select bs.businessid 
                                     , date(bs.onboarddatenew) as onboarddate
                                     , bs.businesstype 
            from 
            business_snapshot bs 
            where date(bs.onboarddatenew) <= '2021-12-18')
    
            select b.businessid, 
    
            max(date(ord.src_created_time)) as prev_max_order_dt,
            count(distinct ord.order_id) as prev_total_orders,
            count(distinct(date(ord.src_created_time))) as prev_distinct_order_dates
    
    
            from base b
            left join customer_snapshot_ c  on b.businessid = c.businessid
            left join(
                      select * from  bolt_order_item_snapshot_ bos
                      where date(bos.src_created_time) <= '2021-12-18'
                      and bos.boltordertype = 'MARKETPLACE'
                      ) as ord
                      on c.customerid = ord.buyer_id
            left join address_snapshot_ ads ON ads.addressentityid = b.businessid
            left join listing_snapshot ls on ls.listing_id = ord.listing_id
            left join sellerproduct_snapshot sps on sps.sp_id = ls.sp_id
            left join product_snapshot_ prod on prod.jpin = sps.jpin
            left join category cat on cat.pvid = prod.pvid
    
            where 
    
            b.businessid not in ('BZID-testPuja'
                            , 'BZID-tech'
                            , 'BZID-sajal'
                            , 'BZID-merchCatalog'
                            , 'BZID-1304457254'
                            , 'BZID-1304463418')
    
            AND c.istestcustomer IS FALSE
            --and ads.addresstype = 'SHIPPING'
    
    
            --AND date(ord.src_created_time) <= '2021-01-14'
    
    
            group by 1
    
    
            """,
            "metadata_query_master": """
    
            SELECT DISTINCT final.*
    
            FROM            (
                                      SELECT    os.*,
                                                --overall_margin_amount        *100.00/gmv_net              AS overall_margin_pct,
                                                total_discount               *100.00/NULLIF(gmv_net,0)    AS pct_discount_taken_on_gmv,
                                                order_items_taken_on_discount*100.00/NULLIF(order_items,0)          AS pct_order_items_taken_on_discount,
                                                sum_return_amount_cust       *100.00/NULLIF(net_of_cancellations,0) AS customer_return_pc,
                                                (total_trips - perfect_delivery)*100.00/NULLIF(total_trips,0)       AS cust_imperfect_delivery_pc,
                                                sum_delivered_amount                                      AS delivered_amount,
                                                sum_reattempt_amount_cust                                 AS reattempt_amount_cust,
                                                sum_return_amount_cust                                    AS return_amount_cust,
                                                sum_return_amount_jt                                      AS return_amount_jt,
                                                sum_missing_amount                                        AS missing_amount,
                                                sum_total_amount                                          AS total_amount,
                                                post_delivery_return_gmv,
                                                total_trips,
                                                perfect_delivery AS perfect_delivery_trips,
                                                complete_rto_trips,
                                                complete_reattempt_trips
                                      FROM      (
                                                         SELECT   
                                                                  businessid,
                                                                  addresscity,
                                                                  Count(DISTINCT order_date)   AS distinct_orderdates,
                                                                  Count(DISTINCT promise_date) AS distinct_promisedates,
                                                                  count(DISTINCT( case when cancelled > 0 then order_date end)) cancellationdt_count,
                                                                  count(DISTINCT( case when returned > 0 then order_date end)) returndt_count,
                                                                  sum(quantity) as quantity_sum,
                                                                  sum(cancelled) as cancelled_sum,
                                                                  sum(returned) as returned_sum,
                                                                  sum(delivered) as delivered_sum,
                                                                  Sum(order_item_amount)       AS ordered_gmv,
                                                                  Sum(
                                                                  CASE
                                                                           WHEN product_type = 'FMCG' THEN order_item_amount
                                                                           ELSE 0
                                                                  END) AS fmcg_gmv,
                                                                  Sum(
                                                                  CASE
                                                                           WHEN product_type = 'Staples' THEN order_item_amount
                                                                           ELSE 0
                                                                  END)                          AS staples_gmv,
                                                                  Sum(tonnage)                  AS tonnage,
                                                                  Sum(shipping_charges)         AS total_shipping,
                                                                  Count(DISTINCT order_item_id) AS order_items,
                                                                  Count(DISTINCT
                                                                  CASE
                                                                           WHEN bought_on_discount = 1 THEN order_item_id
                                                                  END)                 AS order_items_taken_on_discount,
                                                                  Sum(discount_amount) AS total_discount,
                                                                  Count(DISTINCT
                                                                  CASE
                                                                           WHEN product_type = 'Staples' THEN category_name
                                                                  END) AS staples_category_bought,
                                                                  Count(DISTINCT
                                                                  CASE
                                                                           WHEN product_type = 'FMCG' THEN category_name
                                                                  END)                          AS fmcg_category_bought,
                                                                  Count(DISTINCT category_name) AS total_categories_bought,
                                                                  Count(DISTINCT jpin)          AS total_jpins_bought,
                                                                  Count(DISTINCT
                                                                  CASE
                                                                           WHEN product_type = 'Staples' THEN jpin
                                                                  END) AS staples_jpin_bought,
                                                                  Count(DISTINCT
                                                                  CASE
                                                                           WHEN product_type = 'FMCG' THEN jpin
                                                                  END) AS fmcg_jpin_bought,
                                                                  Sum(
                                                                  CASE
                                                                           WHEN product_type = 'FMCG' THEN net_gmv
                                                                           ELSE 0
                                                                  END) AS fmcg_gmv_net,
                                                                  Sum(
                                                                  CASE
                                                                           WHEN product_type = 'Staples' THEN net_gmv
                                                                           ELSE 0
                                                                  END)                      AS staples_gmv_net,
                                                                  Sum(Isnull(net_gmv,0))    AS gmv_net,
                                                                  Sum(net_of_cancellations) AS net_of_cancellations
                                                                  -- Sum(
            --                                                       CASE
            --                                                                WHEN product_type = 'Staples' THEN margin
            --                                                       END) AS staples_margin,
            --                                                       Sum(
            --                                                       CASE
            --                                                                WHEN product_type = 'FMCG' THEN margin
            --                                                       END)        AS fmcg_margin,
            --                                                       Sum(margin) AS overall_margin_amount
                                                         FROM     (
                                                                            SELECT    c.businessid,
                                                                                      ad.addresscity,
                                                                                      Date(ps.updated_promise_time) AS promise_date,
                                                                                      Date(ord.src_created_time)    AS order_date,
                                                                                      ord.quantity as quantity,
                                                                                      ord.delivered_units as delivered,
                                                                                      ord.cancelled_units as cancelled,
                                                                                      ord.returned_units as returned,
                                                                                      ord.order_item_id,
                                                                                      ord.order_item_amount,
                                                                                      ord.shipping_charges,
                                                                                      ((ord.order_item_amount / NULLIF(ord.quantity,0)) * (ord.quantity - ord.cancelled_units - Isnull(ord.return_requested_quantity,0) - Isnull(ord.returned_units,0))) AS net_gmv,
                                                                                      CASE
                                                                                                WHEN cat.DISTRIBUTED IS true THEN 'FMCG'
                                                                                                WHEN cat.DISTRIBUTED IS false THEN 'Staples'
                                                                                      END AS product_type,
                                                                                      ord.order_item_status,
                                                                                      cat.category_name,
                                                                                      prod.jpin,
                                                                                      (ord.quantity - ord.cancelled_units) * sca.deadweight AS tonnage,
                                                                                      CASE
                                                                                                WHEN ord.selling_price - (ord.order_item_amount/NULLIF(quantity,0)) > 0 THEN 1
                                                                                                ELSE 0
                                                                                      END AS bought_on_discount,
                                                                                      CASE
                                                                                                WHEN ord.selling_price - (ord.order_item_amount/NULLIF(quantity,0)) > 0 THEN ord.selling_price - (ord.order_item_amount/NULLIF(quantity,0))
                                                                                                ELSE 0
                                                                                      END                                                                           AS discount_amount,
                                                                                      (ord.order_item_amount / NULLIF(ord.quantity,0)) * (ord.quantity - ord.cancelled_units) AS net_of_cancellations
                                                                                      --CONVERT( decimal(10,4),(shipping_per_unit*net_order_quantity+total_jw_margin_without_backend+total_backend_margin_jw+
                                                                                      --CASE
                                                                                      --          WHEN fulfilling_entity='SS' THEN 0
                                                                                      --          ELSE total_commission
                                                                                      --END+
                                                                                      --CASE
                                                                                      --          WHEN fulfilling_entity='SS' THEN total_backend_margin_ss+total_ss_margin_without_backend- 0.001*price_per_unit*net_order_quantity
                                                                                      --          ELSE 0
                                                                                      --END) ) AS margin
                                                                            FROM      bolt_order_item_snapshot_ ord
                                                                            --JOIN      daily_margin_snapshot mar
                                                                            --ON        mar.order_item_id = ord.order_item_id
                                                                            LEFT JOIN customer_snapshot_ c
                                                                            ON        c.customerid = ord.buyer_id
                                                                            AND       c.istestcustomer IS false
                                                                            AND       c.businessid NOT LIKE '%ech%'
                                                                            AND       c.businessid NOT LIKE '%uja%'
                                                                            AND       c.businessid NOT LIKE '%sajal%'
                                                                            LEFT JOIN listing_snapshot ls
                                                                            ON        ls.listing_id = ord.listing_id
                                                                            LEFT JOIN sellerproduct_snapshot sps
                                                                            ON        sps.sp_id = ls.sp_id
                                                                            LEFT JOIN product_snapshot_ prod
                                                                            ON        prod.jpin = sps.jpin
                                                                            LEFT JOIN category cat
                                                                            ON        cat.pvid = prod.pvid
                                                                            LEFT JOIN promise_snapshot ps
                                                                            ON        ps.promised_entity_id = ord.order_item_id
                                                                            LEFT JOIN supplychainattributes_snapshot_ sca
                                                                            ON        sca.jpin = prod.jpin
                                                                            LEFT JOIN address_snapshot_ ad
                                                                            ON        ad.addressentityid = c.businessid
                                                                            AND       ad.addresstype = 'SHIPPING'
                                                                            WHERE     date(ord.src_created_time) >= '2021-10-18'
                                                                            AND       date(ord.src_created_time) <= '2021-12-18'
                                                                            --AND       ord.order_item_amount > 0
                                                                                      -- and ord.order_item_status not in ('Cancelled','Ready To Ship', 'Confirmed')
                                                                  )
                                                         GROUP BY 1,
                                                                  2
                                                                  ) os
                                      LEFT JOIN
                                                (
                                                          SELECT    
                                                                    c.businessid,
                                                                    sum(
                                                                    CASE
                                                                              WHEN pem.entity_type = 'DELIVERED' THEN pem.actual_amount
                                                                              ELSE
                                                                                        CASE
                                                                                                  WHEN di.delta_type = 'WEIGHT_ISSUE' THEN di.amount_difference
                                                                                                  ELSE 0
                                                                                        END
                                                                    END) AS sum_delivered_amount,
                                                                    sum(
                                                                    CASE
                                                                              WHEN di.delta_type = 'REATTEMPT'
                                                                              AND       di.reason IN ('CUSTOMER_REATTEMPT_EXCEEDED',
                                                                                                      'OUTSTANDING_CREDIT_PAYMENT_REJECTED',
                                                                                                      'NO_VISIT_ON_CUSTOMER_REQUEST',
                                                                                                      'PAYMENT_NOT_AVAILABLE',
                                                                                                      'NOT_NEEDED_ANYMORE',
                                                                                                      'CHANGED_MY_MIND',
                                                                                                      'ALTERNATE_PROCUREMENT',
                                                                                                      'SHOP_OWNER_NOT_AVAILABLE',
                                                                                                      'PLACED_BY_MISTAKE',
                                                                                                      'NO_VISIT_ON_CD_REQUEST',
                                                                                                      'DUPLICATE_ORDER',
                                                                                                      'SHOP_CLOSED') THEN di.amount_difference
                                                                              ELSE 0
                                                                    END) AS sum_reattempt_amount_cust,
                                                                    sum(
                                                                    CASE
                                                                              WHEN di.delta_type = 'REATTEMPT'
                                                                              AND       di.reason NOT IN ('CUSTOMER_REATTEMPT_EXCEEDED',
                                                                                                          'OUTSTANDING_CREDIT_PAYMENT_REJECTED',
                                                                                                          'NO_VISIT_ON_CUSTOMER_REQUEST',
                                                                                                          'PAYMENT_NOT_AVAILABLE',
                                                                                                          'NOT_NEEDED_ANYMORE',
                                                                                                          'CHANGED_MY_MIND',
                                                                                                          'ALTERNATE_PROCUREMENT',
                                                                                                          'SHOP_OWNER_NOT_AVAILABLE',
                                                                                                          'PLACED_BY_MISTAKE',
                                                                                                          'NO_VISIT_ON_CD_REQUEST',
                                                                                                          'DUPLICATE_ORDER',
                                                                                                          'SHOP_CLOSED') THEN di.amount_difference
                                                                              ELSE 0
                                                                    END) AS sum_reattempt_amount_jt ,
                                                                    sum(
                                                                    CASE
                                                                              WHEN di.delta_type IN ('RETURN_TO_ORIGIN',
                                                                                                     'MRP_ISSUE')
                                                                              AND       di.reason IN ('CUSTOMER_REATTEMPT_EXCEEDED',
                                                                                                      'OUTSTANDING_CREDIT_PAYMENT_REJECTED',
                                                                                                      'NO_VISIT_ON_CUSTOMER_REQUEST',
                                                                                                      'PAYMENT_NOT_AVAILABLE',
                                                                                                      'NOT_NEEDED_ANYMORE',
                                                                                                      'CHANGED_MY_MIND',
                                                                                                      'ALTERNATE_PROCUREMENT',
                                                                                                      'SHOP_OWNER_NOT_AVAILABLE',
                                                                                                      'PLACED_BY_MISTAKE',
                                                                                                      'NO_VISIT_ON_CD_REQUEST',
                                                                                                      'DUPLICATE_ORDER',
                                                                                                      'SHOP_CLOSED') THEN di.amount_difference
                                                                              ELSE 0
                                                                    END) AS sum_return_amount_cust ,
                                                                    sum(
                                                                    CASE
                                                                              WHEN di.delta_type IN ('RETURN_TO_ORIGIN',
                                                                                                     'MRP_ISSUE')
                                                                              AND       di.reason NOT IN ('CUSTOMER_REATTEMPT_EXCEEDED',
                                                                                                          'OUTSTANDING_CREDIT_PAYMENT_REJECTED',
                                                                                                          'NO_VISIT_ON_CUSTOMER_REQUEST',
                                                                                                          'PAYMENT_NOT_AVAILABLE',
                                                                                                          'NOT_NEEDED_ANYMORE',
                                                                                                          'CHANGED_MY_MIND',
                                                                                                          'ALTERNATE_PROCUREMENT',
                                                                                                          'SHOP_OWNER_NOT_AVAILABLE',
                                                                                                          'PLACED_BY_MISTAKE',
                                                                                                          'NO_VISIT_ON_CD_REQUEST',
                                                                                                          'DUPLICATE_ORDER',
                                                                                                          'SHOP_CLOSED') THEN di.amount_difference
                                                                              ELSE 0
                                                                    END) AS sum_return_amount_jt,
                                                                    sum(
                                                                    CASE
                                                                              WHEN di.delta_type = 'MISSING' THEN di.amount_difference
                                                                              ELSE 0
                                                                    END) AS sum_missing_amount ,
                                                                    sum(
                                                                    CASE
                                                                              WHEN entity_type IN ('RETURN_TO_ORIGIN',
                                                                                                   'REATTEMPT') THEN di.amount_difference
                                                                              ELSE pem.expected_amount
                                                                    END)                        AS sum_total_amount,
                                                                    isnull(post_delivery_gmv,0) AS post_delivery_return_gmv,
                                                                    total_trips,
                                                                    perfect_delivery,
                                                                    complete_rto_trips,
                                                                    complete_reattempt_trips
                                                          FROM      payment_entity_mapping pem
                                                          LEFT JOIN bolt_order_item_v2_snapshot ord
                                                          ON        pem.entity_id=ord.order_item_id
                                                          LEFT JOIN delta_item di
                                                          ON        pem.mapping_id=di.mapping_id
                                                          JOIN      customer_snapshot_ c
                                                          ON        ord.buyer_id=c.customerid
                                                          JOIN
                                                                    (
                                                                             SELECT  
                                                                                      businessid,
                                                                                      count(DISTINCT trip_id) AS total_trips,
                                                                                      count(DISTINCT
                                                                                      CASE
                                                                                               WHEN order_items = reattempt_order_items
                                                                                               AND      rto_order_items+reattempt_order_items+delivered_items = order_items THEN trip_id
                                                                                      END) AS complete_reattempt_trips,
                                                                                      count(DISTINCT
                                                                                      CASE
                                                                                               WHEN order_items = rto_order_items
                                                                                               AND      rto_order_items+reattempt_order_items+delivered_items = order_items THEN trip_id
                                                                                      END) AS complete_rto_trips,
                                                                                      count(DISTINCT
                                                                                      CASE
                                                                                               WHEN order_items = delivered_items
                                                                                               AND      rto_order_items+reattempt_order_items+delivered_items = order_items THEN trip_id
                                                                                      END) AS perfect_delivery
                                                                             FROM     (
                                                                                               SELECT   
                                                                                                        businessid,
                                                                                                        trip_id,
                                                                                                        count(DISTINCT entity_id) AS order_items,
                                                                                                        count(DISTINCT
                                                                                                        CASE
                                                                                                                 WHEN entity_type IN ('RETURN_TO_ORIGIN')
                                                                                                                 AND      reason  IN ('CUSTOMER_REATTEMPT_EXCEEDED',
                                                                                                                                      'OUTSTANDING_CREDIT_PAYMENT_REJECTED',
                                                                                                                                      'NO_VISIT_ON_CUSTOMER_REQUEST',
                                                                                                                                      'PAYMENT_NOT_AVAILABLE',
                                                                                                                                      'NOT_NEEDED_ANYMORE',
                                                                                                                                      'CHANGED_MY_MIND',
                                                                                                                                      'ALTERNATE_PROCUREMENT',
                                                                                                                                      'SHOP_OWNER_NOT_AVAILABLE',
                                                                                                                                      'PLACED_BY_MISTAKE',
                                                                                                                                      'NO_VISIT_ON_CD_REQUEST',
                                                                                                                                      'DUPLICATE_ORDER',
                                                                                                                                      'SHOP_CLOSED') THEN entity_id
                                                                                                        END) AS rto_order_items,
                                                                                                        count(DISTINCT
                                                                                                        CASE
                                                                                                                 WHEN entity_type IN ('REATTEMPT')
                                                                                                                 AND      reason  IN ('CUSTOMER_REATTEMPT_EXCEEDED',
                                                                                                                                      'OUTSTANDING_CREDIT_PAYMENT_REJECTED',
                                                                                                                                      'NO_VISIT_ON_CUSTOMER_REQUEST',
                                                                                                                                      'PAYMENT_NOT_AVAILABLE',
                                                                                                                                      'NOT_NEEDED_ANYMORE',
                                                                                                                                      'CHANGED_MY_MIND',
                                                                                                                                      'ALTERNATE_PROCUREMENT',
                                                                                                                                      'SHOP_OWNER_NOT_AVAILABLE',
                                                                                                                                      'PLACED_BY_MISTAKE',
                                                                                                                                      'NO_VISIT_ON_CD_REQUEST',
                                                                                                                                      'DUPLICATE_ORDER',
                                                                                                                                      'SHOP_CLOSED') THEN entity_id
                                                                                                        END) AS reattempt_order_items,
                                                                                                        count(DISTINCT
                                                                                                        CASE
                                                                                                                 WHEN entity_type IN ('DELIVERED') THEN entity_id
                                                                                                        END) AS delivered_items
                                                                                               FROM    (
                                                                                                                  SELECT    
                                                                                                                            c.businessid,
                                                                                                                            t.trip_id,
                                                                                                                            pem.entity_id,
                                                                                                                            pem.entity_type,
                                                                                                                            di.reason
                                                                                                                  FROM      payment_entity_mapping pem
                                                                                                                  LEFT JOIN bolt_order_item_v2_snapshot ord
                                                                                                                  ON        pem.entity_id=ord.order_item_id
                                                                                                                  LEFT JOIN delta_item di
                                                                                                                  ON        pem.mapping_id=di.mapping_id
                                                                                                                  JOIN      customer_snapshot_ c
                                                                                                                  ON        ord.buyer_id=c.customerid
                                                                                                                  JOIN      payment py
                                                                                                                  ON        pem.payment_id = py.payment_id
                                                                                                                  JOIN      dw_shipment.trip_node tn
                                                                                                                  ON        tn.node_id = RIGHT( py.trip_node_id, LEN(py.trip_node_id) - 4)
                                                                                                                  AND       tn.deleted_at IS NULL
                                                                                                                  JOIN      dw_shipment.trip t
                                                                                                                  ON        t.trip_id = tn.trip_id
                                                                                                                  AND       t.deleted_at IS NULL
                                                                                                                  WHERE     trunc(pem.created_time) >= '2021-10-18'
                                                                                                                  AND       trunc(pem.created_time) <= '2021-12-18'
                                                                                                                  AND       pem.deleted_at IS NULL
                                                                                                                  AND       pem.is_deleted IS NULL
                                                                                                                  AND       di.deleted_at IS NULL )
                                                                                               GROUP BY 1,
                                                                                                        2
                                                                                                        )
                                                                             WHERE    order_items > 0
                                                                             GROUP BY 1
                                                                                      ) tm
                                                          ON        tm.businessid = c.businessid
    
                                                          LEFT JOIN
                                                                    (
                                                                             SELECT   
                                                                                      cs.businessid,
                                                                                      sum((
                                                                                      CASE
                                                                                               WHEN rs.return_state::text <> 'REJECTED'::character VARYING::text
                                                                                               AND      rs.return_state::text <> 'CANCELLED'::character VARYING::text
                                                                                               AND      rs.return_state::text <> 'APPROVED'::character VARYING::text
                                                                                               AND      rs.is_rto IS false THEN rs.return_item_units
                                                                                               ELSE 0
                                                                                      END)*((ord.order_item_amount + ord.shipping_charges) / ord.quantity)) AS post_delivery_gmv
                                                                             FROM     return_item_snapshot rs
                                                                             JOIN     bolt_order_item_v2_snapshot ord
                                                                             ON       ord.order_item_id = rs.order_item_id
                                                                             JOIN     customer_snapshot_ cs
                                                                             ON       cs.customerid = ord.buyer_id
                                                                             WHERE    is_rto IS false
                                                                             AND      ord.boltordertype = 'MARKETPLACE'
                                                                             AND      date(rs.src_created_time) >= '2021-10-18'
                                                                             GROUP BY 1
                                                                                      ) post
                                                          ON        post.businessid = c.businessid
    
                                                          WHERE     trunc(pem.created_time) >= '2021-10-18'
                                                          AND       trunc(pem.created_time) <= '2021-12-18'
                                                          AND       pem.deleted_at IS NULL
                                                          AND       pem.is_deleted IS NULL
                                                          AND       di.deleted_at IS NULL
                                                          GROUP BY  1,
                                                                    9,
                                                                    10,
                                                                    11,
                                                                    12,
                                                                    13
    
                                                          ORDER BY  1,
                                                                    2) ra
                                      ON        os.businessid = ra.businessid
    
                                      WHERE     gmv_net >= 0 
                                      ) final
            """,
            "queryString_app": """with  cal as (select * from calendar
                              where calendar.calendardate >= '2021-10-18' and calendar.calendardate <= '2021-12-18'
                              )
    
    
            select  c.businessid,
            count ( distinct case when h.en ='ON_APP_CAME_TO_FG' then  cal.calendardate end) cta_dt_cnt,
            count ( distinct case when h.en in('ON_LOAD_PRODUCT_LIST_SCREEN','ON_LOAD_PRODUCT_SCREEN')then cal.calendardate end) ppv_plv_dt_cnt,
            count ( distinct case when h.en in('ON_TAP_GO_TO_CART','ON_TAP_CART_BOX') then cal.calendardate end) atc_dt_cnt
    
            from (select * from hevo_customer_app_events_webhook he where he.en in ('ON_APP_CAME_TO_FG','ON_LOAD_PRODUCT_LIST_SCREEN',
                         'ON_LOAD_PRODUCT_SCREEN',
                         'ON_TAP_GO_TO_CART','ON_TAP_CART_BOX')          
                  and he.uid is not null) as h
    
            left join customer_snapshot_ c on h.uid = c.customerid  
            inner join cal on cast(date(timestamp 'epoch' + (h.ets / 1000) * interval '1 second' + interval '5 hours 30 minutes')as timestamp) = cal.calendardate 
            and 
            c.istestcustomer is FALSE
    
            and c.businessid is not null
            and c.businessid not in ('BZID-testPuja'
                                    , 'BZID-tech'
                                    , 'BZID-sajal'
                                    , 'BZID-merchCatalog'
                                    , 'BZID-1304457254'
                                    , 'BZID-1304463418')
    
            group by 1
    
            """,
            "visits_query": """
    
                    select businessid,  count(distinct time_stamp) as total_visits
    
    
                    from cs_revisits_data
                    where date(time_stamp) >= date('2021-10-18')
                    and date(time_stamp) <= date('2021-12-18')
    
                     group by 1
    
    
                    """,
            "calls_query": """
    
                    select businessid, count(distinct comm_timestamp) calls
    
    
                    from 
                    growth_ops_calling_data
                    where date(comm_timestamp) >= date('2021-10-18')
                    and date(comm_timestamp) <= date('2021-12-18')
    
                     group by 1
    
    
                    """,
            "credit_base_query": """
    
              select 
    
                 cut.bz_id,
                 cl.status,
                 cred.credit_onboard,
                 cl.avg_days_past_due,
                 cl.current_limit as currentlimit,
                 cl.overall_limit as overalllimit,
                 cl.total_bounced as totalbounced,
                 cl.total_outstanding as totaloutstanding,
                 cl.total_outstanding_bounced as totaloutstandingbounced,
                 cl.total_credit_ever_used as totalcreditused,
                 cl.total_bounced_count as totalbouncedcount,
                 cl.total_outstanding_bounced_count as totaloutstandingbouncedcount,
                 cl.total_outstanding_count as totaloutstandingcount,
                 cl.total_credit_ever_used_count as totalcreditusedcount
    
                from credit_line cl
                left join credit_product cp on cl.credit_product_id = cp.product_id
                left join credit_user_type cut on cl.credit_user_type_mapping_id = cut.id
                right join   (select 
    
                        cut.bz_id,
                        cl.status,
    
                        max(date(TIMESTAMP 'epoch' + cl.start_date/1000 *INTERVAL '1 second')) as  credit_onboard
    
    
                        from
                          credit_line cl
                          left join credit_product cp on cl.credit_product_id = cp.product_id
                          left join credit_user_type cut on cl.credit_user_type_mapping_id = cut.id
                        where
                            cp.name not in('DUMMY_PRODUCT')
                         -- cp.product_id not in ( '2500541') 
                        and cp.name not in ('LoanTap-DPN','DeHaat-BlackSoil','LoanTap-DPN','DUMMY_PRODUCT','JT-Institutional-Sales','JT-BILL2BILL')
                        --  and 
                        and cut.bz_id like 'BZID%'
                        group by
                          1,2
                        order by 2,1) as cred
    
                on cred.bz_id = cut.bz_id
                and cred.status = cl.status
                and cred.credit_onboard = date(TIMESTAMP 'epoch' + cl.start_date/1000 *INTERVAL '1 second')
    
    
    
            """,
            "credit_utilization_query": """
    
              select bz_id, avg(utilization) as avg_daily_utilzation
            from (select *,
            date(timestamp 'epoch' + (cdt.created_time/1000) * interval '1 second' + interval '5 hours 30 minutes') as created_date,
            cdt.created_time,
    
            value,
            cla.overall_limit,
            (value/NULLIF(cla.overall_limit,0)*100) as utilization
    
            from credit_transaction ct
            join credit_transaction_details cdt on cdt.credit_transaction = ct.id
            left join (select *,
                       max(cl.created_time) over (partition by cl.id, 
                                                  date(timestamp 'epoch' + (cl.created_time/1000) * interval '1 second' + interval '5 hours 30 minutes') 
                                                  ) as max_ts
                       from credit_line_audit cl
                       where status = 'ACTIVE' ) cla on ct.credit_line_id = cla.id
            left join credit_user_type cut on cla.credit_user_type_mapping_id = cut.id
            where transaction_type = 'DEBIT'
            and cdt.amount_type = 'BASE'
            and date(timestamp 'epoch' + (cdt.created_time/1000) * interval '1 second' + interval '5 hours 30 minutes') >= '2021-10-18'
            and date(timestamp 'epoch' + (cdt.created_time/1000) * interval '1 second' + interval '5 hours 30 minutes') <= '2021-12-18'
            and max_ts = cla.created_time
            )
            group by 1
    
    
            """,
            "dsat_query": """
                SELECT   rg.businessid,
                     Count(rg.rating) AS rating_cnt,
                     ROUND(Avg(rg.rating)) AS avg_rating
            FROM     (
                            SELECT *
                            FROM   (
                                             SELECT    date(timestamp 'epoch' + (ets/1000) * interval '1 second' + interval '5 hours 30 minutes') AS dt,
                                                       uid ,
                                                       cs.businessid AS businessid,
                                                       sid,
                                                       seq,
                                                       srv_req_ent_id,
                                                       srv_id                                                      AS survey_id,
                                                       srv_ans_val/1.00                                                 AS rating
                                                       --row_number() OVER (partition BY uid, sid ORDER BY seq DESC) AS rnk
                                             FROM      hevo_customer_app_events_webhook
                                             LEFT JOIN customer_snapshot_ cs
                                             ON        cs.customerid = hevo_customer_app_events_webhook.uid
                                             JOIN      address_snapshot_ ads
                                             ON        ads.addressentityid=cs.businessid
                                             AND       addresstype='SHIPPING'
                                             AND       cs.businessid NOT IN ( 'BZID-testPuja' ,
                                                                             'BZID-tech' ,
                                                                             'BZID-sajal' ,
                                                                             'BZID-merchCatalog' ,
                                                                             'BZID-1304457254' ,
                                                                             'BZID-1304463418',
                                                                             'BZID-hubballi',
                                                                             'BZID-1304433825',
                                                                             'BZID-1304436504',
                                                                             'BZID-1304435850' )
                                             WHERE     en = 'ON_SURVEY_RATING_CHANGED'
                                             AND       srv_que_id = 'QES-182'
                                             AND       date(timestamp 'epoch' + (ets/1000) * interval '1 second' + interval '5 hours 30 minutes') >= '2021-10-18'
                                             AND       date(timestamp 'epoch' + (ets/1000) * interval '1 second' + interval '5 hours 30 minutes') <= '2021-12-18' )
                    ) rg
            JOIN
                     (
                               SELECT    date(timestamp 'epoch' + (ets/1000) * interval '1 second' + interval '5 hours 30 minutes') AS dt,
                                         uid ,
                                         sid,
                                         seq,
                                         srv_req_ent_id,
                                         srv_id      AS survey_id,
                                         srv_ans_val AS rating
                               FROM      hevo_customer_app_events_webhook
                               LEFT JOIN customer_snapshot_ cs
                               ON        cs.customerid = hevo_customer_app_events_webhook.uid
                               JOIN      address_snapshot_ ads
                               ON        ads.addressentityid=cs.businessid
                               AND       addresstype='SHIPPING'
                               AND       cs.businessid NOT IN ( 'BZID-testPuja' ,
                                                               'BZID-tech' ,
                                                               'BZID-sajal' ,
                                                               'BZID-merchCatalog' ,
                                                               'BZID-1304457254' ,
                                                               'BZID-1304463418',
                                                               'BZID-hubballi',
                                                               'BZID-1304433825',
                                                               'BZID-1304436504',
                                                               'BZID-1304435850' )
                               WHERE     en = 'ON_SURVEY_SUBMIT'
                               AND       date(timestamp 'epoch' + (ets/1000) * interval '1 second' + interval '5 hours 30 minutes') >= '2021-10-18'
                               AND       date(timestamp 'epoch' + (ets/1000) * interval '1 second' + interval '5 hours 30 minutes') <= '2021-12-18' ) ss
                      ON       ss.dt = rg.dt
                      AND      ss.uid = rg.uid
                      AND      ss.srv_req_ent_id = rg.srv_req_ent_id
    
            --where businessid = 'BZID-1304472890'
            group by 1
    
    
    
    
            """,
            "target_scheme_query": """
                select 
                customer as businessid, 
                count(distinct target_scheme_id) as target_schemes_count,
                count(distinct( case when milestone_crossed_cv > 0 then milestone_crossed_cv end)) as milestones_achieved_count,
                sum(jc_payout) as total_JC_earned
    
            from
            (select target_scheme_id, natural_id,description, objective, title, internal_scheme_name,internal_scheme_description, filter_entity_id as Customer,
    
             sum(case when current_value is not null then current_value else 0 end) as current_value, sum(case when jc_payout > 0 then current_value else 0 end) as milestone_crossed_CV,sum(case when jc_payout is not null then jc_payout else 0 end) as jc_payout, sum(case when burn is not null then burn else 0 end) as burn
    
            from
            (
            select *, 
              case when payout_type = 'ABSOLUTE' then payout_val * 1.00
                   when payout_type = 'PERCENTAGE' then payout_val * 1.00 * 0.01 * current_value 
                   end as jc_payout, 
              case when payout_type = 'ABSOLUTE' then payout_val * 1.00 * 0.85 
                   when payout_type = 'PERCENTAGE' then payout_val * 1.00 * 0.01 * current_value * 0.85 
                   end as burn
            from
            (
            select ts.target_scheme_id, ts.natural_id, ts.description, ts.objective, ts.title, ts.internal_scheme_name,ts.internal_scheme_description, gir.filter_entity_id, smt.current_value, 
                case when num_ms = 3 then
            (
                    case when ms1 > current_value then 0
                    when ms1 <= current_value and ms2 > current_value then ms1_payout_val
                    when ms2 <= current_value and ms3 > current_value then ms2_payout_val
                    when ms3 <= current_value then ms3_payout_val end
              )
               when num_ms = 2 then 
            (
              case when ms1 > current_value then 0
                    when ms1 <= current_value and ms2 > current_value then ms1_payout_val
                    when ms2 <= current_value then ms2_payout_val end
              )
            when num_ms = 1 then
            (
              case when ms1 > current_value then 0
                    when ms1 <= current_value then ms1_payout_val end
              ) end
            as payout_val,
            case when num_ms = 3 then
            (
                    case when ms1 > current_value then '0'
                    when ms1 <= current_value and ms2 > current_value then ms1_payout_mode
                    when ms2 <= current_value and ms3 > current_value then ms2_payout_mode
                    when ms3 <= current_value then ms3_payout_mode end
              )
               when num_ms = 2 then 
            (
              case when ms1 > current_value then '0'
                    when ms1 <= current_value and ms2 > current_value then ms1_payout_mode
                    when ms2 <= current_value then ms2_payout_mode end
              )
            when num_ms = 1 then
            (
              case when ms1 > current_value then '0'
                    when ms1 <= current_value then ms1_payout_mode end
              ) end
            as payout_mode,
            case when num_ms = 3 then
            (
                    case when ms1 > current_value then '0'
                    when ms1 <= current_value and ms2 > current_value then ms1_payout_type
                    when ms2 <= current_value and ms3 > current_value then ms2_payout_type
                    when ms3 <= current_value then ms3_payout_type end
              )
               when num_ms = 2 then 
            (
              case when ms1 > current_value then '0'
                    when ms1 <= current_value and ms2 > current_value then ms1_payout_type
                    when ms2 <= current_value then ms2_payout_type end
              )
            when num_ms = 1 then
            (
              case when ms1 > current_value then '0'
                    when ms1 <= current_value then ms1_payout_type end
              ) end
            as payout_type,
                    ms.*
    
            from dw_target_scheme.target_scheme ts
            left join dw_target_scheme.group_inclusion_rules gir on gir.target_scheme_id = ts.target_scheme_id and gir.member_entity_type = 'BUSINESS'
            left join dw_target_scheme.scheme_member_target smt on smt.target_scheme_id = ts.target_scheme_id and smt.member_id = gir.filter_entity_id
            left join (select m1.target_scheme_id as ts, m1.at_value as ms1, m2.at_value as ms2, m3.at_value as ms3,  m1.value as ms1_payout_val, m1.payout_mode as ms1_payout_mode, m1.payout_type as ms1_payout_type, m2.value as ms2_payout_val, m2.payout_mode as ms2_payout_mode, m2.payout_type as ms2_payout_type, m3.value as ms3_payout_val, m3.payout_mode as ms3_payout_mode, m3.payout_type as ms3_payout_type, num_ms
                       from (select ms.target_scheme_id, ms.at_value, p.value, p.payout_mode, p.payout_type 
                             from dw_target_scheme.milestone ms left join dw_target_scheme.payout p on p.milestone_id = ms.milestone_id) m1
            left join (select ms.target_scheme_id, ms.at_value, p.value, p.payout_mode, p.payout_type from dw_target_scheme.milestone ms left join dw_target_scheme.payout p on p.milestone_id = ms.milestone_id) m2 on m2.target_scheme_id = m1.target_scheme_id and m1.at_value < m2.at_value
            left join (select ms.target_scheme_id, ms.at_value, p.value, p.payout_mode, p.payout_type from dw_target_scheme.milestone ms left join dw_target_scheme.payout p on p.milestone_id = ms.milestone_id) m3 on m3.target_scheme_id = m1.target_scheme_id and m2.at_value < m3.at_value
            left join 
            (
            select target_scheme_id as ts, count(distinct milestone_id) as num_ms
            from dw_target_scheme.milestone
            group by 1
            ) a on a.ts = m1.target_scheme_id
            where case when a.num_ms = 1 then m1.at_value is not null and m2.at_value is null and m3.at_value is null
                        when a.num_ms = 2 then m1.at_value is not null and m2.at_value is not null and m3.at_value is null
                        when a.num_ms = 3 then m1.at_value is not null and m2.at_value is not null and m3.at_value is not null
                        else false end) ms on ms.ts = ts.target_scheme_id
            where ts.target_scheme_status = 'ACTIVE' 
            --   and date_add(date_add(from_unixtime(ts.end_time/1000), interval '5 hours'),interval '30 minutes') >= '2022-01-01'
              and date(timestamp 'epoch' + (ts.end_time/1000) * interval '1 second' + interval '5 hours 30 minutes') >= '2021-10-18'
              and date(timestamp 'epoch' + (ts.end_time/1000) * interval '1 second' + interval '5 hours 30 minutes') <= '2021-12-18'
    
             --  ##and ts.target_scheme_id in (100003202, 100003203)
            ) a
              ) a
            group by 1,2,3,4,5,6,7,8) o
            where current_value > 0
            group by 1
    
    
            """,
            "superclub_query": """
                select business_id, sum(points_redeemed) as sc_points_red, count(distinct reward_id) as sc_rewards_count
            from dw_superclub.redeemed_rewards
            where current_status not in ('CANCELLED','Cancelled','cancelled')
            and date(rs_last_updated_time) > '2021-10-18'
            and date(rs_last_updated_time) <= '2021-12-18'
            group by 1
    
            """,
            "null_search_query": """
    
            WITH base AS
            (
                   SELECT *
                          --   dt
                          --   , en_plus_1
                          --   , count(*) as occ
                   FROM   (
                                   SELECT   * ,
                                            Lag(en, 1) OVER(partition BY sid ORDER BY seq) AS en_plus_1 ,
                                            Lag(en, 2) OVER(partition BY sid ORDER BY seq) AS en_plus_2
                                   FROM     (
                                                      SELECT
                                                                --ets
                                                                cs.businessid ,
                                                                uid ,
                                                                en ,
                                                                sid ,
                                                                seq ,
                                                                eid ,
                                                                calendar.month
                                                      FROM      hevo_customer_app_events_webhook
                                                      LEFT JOIN customer_snapshot_ cs
                                                      ON        cs.customerid = hevo_customer_app_events_webhook.uid
                                                      JOIN      address_snapshot_ ads
                                                      ON        ads.addressentityid = cs.businessid
                                                      AND       addresstype = 'SHIPPING'
                                                      AND       cs.businessid NOT IN ( 'BZID-testPuja' ,
                                                                                      'BZID-tech' ,
                                                                                      'BZID-sajal' ,
                                                                                      'BZID-merchCatalog' ,
                                                                                      'BZID-1304457254' ,
                                                                                      'BZID-1304463418' ,
                                                                                      'BZID-hubballi' ,
                                                                                      'BZID-1304433825' ,
                                                                                      'BZID-1304436504' ,
                                                                                      'BZID-1304435850' )
                                                      LEFT JOIN calendar
                                                      ON        date(timestamp 'epoch' + (ets / 1000) * interval '1 second' + interval '5 hours 30 minutes') = calendar.calendardate
                                                      WHERE
                                                                --           etype = 'UA'
                                                                cat IN ( 'SEARCH' ,
                                                                        'PRODUCT' )
                                                      AND       calendar.calendardate <= '2021-12-18'
                                                      AND       calendar.calendardate >= '2021-10-18'
                                                                --and ets < extract('epoch' from current_date + 1 )::BIGINT * 1000
                                                                --and  ads.addresscity in ('Bengaluru','Bangalore','Chikkaballapura','Tumkur','Hosur',
                                                                --'Mysore','Mandya','Hassan','Hubballi','Belgaum','Dharwad','Davanagere','Haveri',
                                                                --'Pune','Hyderabad')
                                                      AND       appvc IN
                                                                          (
                                                                          SELECT DISTINCT appvc
                                                                          FROM            hevo_customer_app_events_webhook) ) )
                   WHERE  en IN ( 'ON_ERROR_EMPTY_PRODUCT_LIST_SCREEN' )
                   AND    (
                                 en_plus_1 NOT IN ( 'ON_LOAD_PRODUCT_LIST_SCREEN' ,
                                                   'ON_ERROR_EMPTY_PRODUCT_LIST_SCREEN' )
                          OR     (
                                        en_plus_2 = 'ON_SUBMIT_SEARCH_QUERY' ) )
                   AND    en_plus_1 IS NOT NULL )
            SELECT   businessid ,
                     count(*) AS null_search_cnt
            FROM     base
            GROUP BY 1
            ORDER BY 1
    
    
    
            """,
        }

    def get_predict_queries(self):
        return {
            "metadata_query_curr": """with base as (select bs.businessid 
                                     , date(bs.onboarddatenew) as onboarddate
                                     , bs.businesstype 
            from 
            business_snapshot bs 
            where date(bs.onboarddatenew) <= '2022-02-18')

            select b.businessid, b.onboarddate, b.businesstype, 

            max(date(ord.src_created_time)) as max_order_dt,
            count(distinct ord.order_id) as total_orders,
            count(distinct(date(ord.src_created_time))) as distinct_order_dates


            from base b
            left join customer_snapshot_ c  on b.businessid = c.businessid
            left join(
                      select * from  bolt_order_item_snapshot_ bos
                      where date(bos.src_created_time) <= '2022-02-18'
                      and bos.boltordertype = 'MARKETPLACE'
                      ) as ord
                      on c.customerid = ord.buyer_id
            left join address_snapshot_ ads ON ads.addressentityid = b.businessid
            left join listing_snapshot ls on ls.listing_id = ord.listing_id
            left join sellerproduct_snapshot sps on sps.sp_id = ls.sp_id
            left join product_snapshot_ prod on prod.jpin = sps.jpin
            left join category cat on cat.pvid = prod.pvid

            where 

            b.businessid not in ('BZID-testPuja'
                            , 'BZID-tech'
                            , 'BZID-sajal'
                            , 'BZID-merchCatalog'
                            , 'BZID-1304457254'
                            , 'BZID-1304463418')

            AND c.istestcustomer IS FALSE
            --and ads.addresstype = 'SHIPPING'


            --AND date(ord.src_created_time) <= '2021-01-14'


            group by 1,2,3


            """,

            "metadata_query_master": """

            SELECT DISTINCT final.*

            FROM            (
                                      SELECT    os.*,
                                                --overall_margin_amount        *100.00/gmv_net              AS overall_margin_pct,
                                                total_discount               *100.00/NULLIF(gmv_net,0)    AS pct_discount_taken_on_gmv,
                                                order_items_taken_on_discount*100.00/NULLIF(order_items,0)          AS pct_order_items_taken_on_discount,
                                                sum_return_amount_cust       *100.00/NULLIF(net_of_cancellations,0) AS customer_return_pc,
                                                (total_trips - perfect_delivery)*100.00/NULLIF(total_trips,0)       AS cust_imperfect_delivery_pc,
                                                sum_delivered_amount                                      AS delivered_amount,
                                                sum_reattempt_amount_cust                                 AS reattempt_amount_cust,
                                                sum_return_amount_cust                                    AS return_amount_cust,
                                                sum_return_amount_jt                                      AS return_amount_jt,
                                                sum_missing_amount                                        AS missing_amount,
                                                sum_total_amount                                          AS total_amount,
                                                post_delivery_return_gmv,
                                                total_trips,
                                                perfect_delivery AS perfect_delivery_trips,
                                                complete_rto_trips,
                                                complete_reattempt_trips
                                      FROM      (
                                                         SELECT   
                                                                  businessid,
                                                                  addresscity,
                                                                  Count(DISTINCT order_date)   AS distinct_orderdates,
                                                                  Count(DISTINCT promise_date) AS distinct_promisedates,
                                                                  count(DISTINCT( case when cancelled > 0 then order_date end)) cancellationdt_count,
                                                                  count(DISTINCT( case when returned > 0 then order_date end)) returndt_count,
                                                                  sum(quantity) as quantity_sum,
                                                                  sum(cancelled) as cancelled_sum,
                                                                  sum(returned) as returned_sum,
                                                                  sum(delivered) as delivered_sum,
                                                                  Sum(order_item_amount)       AS ordered_gmv,
                                                                  Sum(
                                                                  CASE
                                                                           WHEN product_type = 'FMCG' THEN order_item_amount
                                                                           ELSE 0
                                                                  END) AS fmcg_gmv,
                                                                  Sum(
                                                                  CASE
                                                                           WHEN product_type = 'Staples' THEN order_item_amount
                                                                           ELSE 0
                                                                  END)                          AS staples_gmv,
                                                                  Sum(tonnage)                  AS tonnage,
                                                                  Sum(shipping_charges)         AS total_shipping,
                                                                  Count(DISTINCT order_item_id) AS order_items,
                                                                  Count(DISTINCT
                                                                  CASE
                                                                           WHEN bought_on_discount = 1 THEN order_item_id
                                                                  END)                 AS order_items_taken_on_discount,
                                                                  Sum(discount_amount) AS total_discount,
                                                                  Count(DISTINCT
                                                                  CASE
                                                                           WHEN product_type = 'Staples' THEN category_name
                                                                  END) AS staples_category_bought,
                                                                  Count(DISTINCT
                                                                  CASE
                                                                           WHEN product_type = 'FMCG' THEN category_name
                                                                  END)                          AS fmcg_category_bought,
                                                                  Count(DISTINCT category_name) AS total_categories_bought,
                                                                  Count(DISTINCT jpin)          AS total_jpins_bought,
                                                                  Count(DISTINCT
                                                                  CASE
                                                                           WHEN product_type = 'Staples' THEN jpin
                                                                  END) AS staples_jpin_bought,
                                                                  Count(DISTINCT
                                                                  CASE
                                                                           WHEN product_type = 'FMCG' THEN jpin
                                                                  END) AS fmcg_jpin_bought,
                                                                  Sum(
                                                                  CASE
                                                                           WHEN product_type = 'FMCG' THEN net_gmv
                                                                           ELSE 0
                                                                  END) AS fmcg_gmv_net,
                                                                  Sum(
                                                                  CASE
                                                                           WHEN product_type = 'Staples' THEN net_gmv
                                                                           ELSE 0
                                                                  END)                      AS staples_gmv_net,
                                                                  Sum(Isnull(net_gmv,0))    AS gmv_net,
                                                                  Sum(net_of_cancellations) AS net_of_cancellations
                                                                  -- Sum(
            --                                                       CASE
            --                                                                WHEN product_type = 'Staples' THEN margin
            --                                                       END) AS staples_margin,
            --                                                       Sum(
            --                                                       CASE
            --                                                                WHEN product_type = 'FMCG' THEN margin
            --                                                       END)        AS fmcg_margin,
            --                                                       Sum(margin) AS overall_margin_amount
                                                         FROM     (
                                                                            SELECT    c.businessid,
                                                                                      ad.addresscity,
                                                                                      Date(ps.updated_promise_time) AS promise_date,
                                                                                      Date(ord.src_created_time)    AS order_date,
                                                                                      ord.quantity as quantity,
                                                                                      ord.delivered_units as delivered,
                                                                                      ord.cancelled_units as cancelled,
                                                                                      ord.returned_units as returned,
                                                                                      ord.order_item_id,
                                                                                      ord.order_item_amount,
                                                                                      ord.shipping_charges,
                                                                                      ((ord.order_item_amount / NULLIF(ord.quantity,0)) * (ord.quantity - ord.cancelled_units - Isnull(ord.return_requested_quantity,0) - Isnull(ord.returned_units,0))) AS net_gmv,
                                                                                      CASE
                                                                                                WHEN cat.DISTRIBUTED IS true THEN 'FMCG'
                                                                                                WHEN cat.DISTRIBUTED IS false THEN 'Staples'
                                                                                      END AS product_type,
                                                                                      ord.order_item_status,
                                                                                      cat.category_name,
                                                                                      prod.jpin,
                                                                                      (ord.quantity - ord.cancelled_units) * sca.deadweight AS tonnage,
                                                                                      CASE
                                                                                                WHEN ord.selling_price - (ord.order_item_amount/NULLIF(quantity,0)) > 0 THEN 1
                                                                                                ELSE 0
                                                                                      END AS bought_on_discount,
                                                                                      CASE
                                                                                                WHEN ord.selling_price - (ord.order_item_amount/NULLIF(quantity,0)) > 0 THEN ord.selling_price - (ord.order_item_amount/NULLIF(quantity,0))
                                                                                                ELSE 0
                                                                                      END                                                                           AS discount_amount,
                                                                                      (ord.order_item_amount / NULLIF(ord.quantity,0)) * (ord.quantity - ord.cancelled_units) AS net_of_cancellations
                                                                                      --CONVERT( decimal(10,4),(shipping_per_unit*net_order_quantity+total_jw_margin_without_backend+total_backend_margin_jw+
                                                                                      --CASE
                                                                                      --          WHEN fulfilling_entity='SS' THEN 0
                                                                                      --          ELSE total_commission
                                                                                      --END+
                                                                                      --CASE
                                                                                      --          WHEN fulfilling_entity='SS' THEN total_backend_margin_ss+total_ss_margin_without_backend- 0.001*price_per_unit*net_order_quantity
                                                                                      --          ELSE 0
                                                                                      --END) ) AS margin
                                                                            FROM      bolt_order_item_snapshot_ ord
                                                                            --JOIN      daily_margin_snapshot mar
                                                                            --ON        mar.order_item_id = ord.order_item_id
                                                                            LEFT JOIN customer_snapshot_ c
                                                                            ON        c.customerid = ord.buyer_id
                                                                            AND       c.istestcustomer IS false
                                                                            AND       c.businessid NOT LIKE '%ech%'
                                                                            AND       c.businessid NOT LIKE '%uja%'
                                                                            AND       c.businessid NOT LIKE '%sajal%'
                                                                            LEFT JOIN listing_snapshot ls
                                                                            ON        ls.listing_id = ord.listing_id
                                                                            LEFT JOIN sellerproduct_snapshot sps
                                                                            ON        sps.sp_id = ls.sp_id
                                                                            LEFT JOIN product_snapshot_ prod
                                                                            ON        prod.jpin = sps.jpin
                                                                            LEFT JOIN category cat
                                                                            ON        cat.pvid = prod.pvid
                                                                            LEFT JOIN promise_snapshot ps
                                                                            ON        ps.promised_entity_id = ord.order_item_id
                                                                            LEFT JOIN supplychainattributes_snapshot_ sca
                                                                            ON        sca.jpin = prod.jpin
                                                                            LEFT JOIN address_snapshot_ ad
                                                                            ON        ad.addressentityid = c.businessid
                                                                            AND       ad.addresstype = 'SHIPPING'
                                                                            WHERE     date(ord.src_created_time) >= '2021-12-18'
                                                                            AND       date(ord.src_created_time) <= '2022-02-18'
                                                                            --AND       ord.order_item_amount > 0
                                                                                      -- and ord.order_item_status not in ('Cancelled','Ready To Ship', 'Confirmed')
                                                                  )
                                                         GROUP BY 1,
                                                                  2
                                                                  ) os
                                      LEFT JOIN
                                                (
                                                          SELECT    
                                                                    c.businessid,
                                                                    sum(
                                                                    CASE
                                                                              WHEN pem.entity_type = 'DELIVERED' THEN pem.actual_amount
                                                                              ELSE
                                                                                        CASE
                                                                                                  WHEN di.delta_type = 'WEIGHT_ISSUE' THEN di.amount_difference
                                                                                                  ELSE 0
                                                                                        END
                                                                    END) AS sum_delivered_amount,
                                                                    sum(
                                                                    CASE
                                                                              WHEN di.delta_type = 'REATTEMPT'
                                                                              AND       di.reason IN ('CUSTOMER_REATTEMPT_EXCEEDED',
                                                                                                      'OUTSTANDING_CREDIT_PAYMENT_REJECTED',
                                                                                                      'NO_VISIT_ON_CUSTOMER_REQUEST',
                                                                                                      'PAYMENT_NOT_AVAILABLE',
                                                                                                      'NOT_NEEDED_ANYMORE',
                                                                                                      'CHANGED_MY_MIND',
                                                                                                      'ALTERNATE_PROCUREMENT',
                                                                                                      'SHOP_OWNER_NOT_AVAILABLE',
                                                                                                      'PLACED_BY_MISTAKE',
                                                                                                      'NO_VISIT_ON_CD_REQUEST',
                                                                                                      'DUPLICATE_ORDER',
                                                                                                      'SHOP_CLOSED') THEN di.amount_difference
                                                                              ELSE 0
                                                                    END) AS sum_reattempt_amount_cust,
                                                                    sum(
                                                                    CASE
                                                                              WHEN di.delta_type = 'REATTEMPT'
                                                                              AND       di.reason NOT IN ('CUSTOMER_REATTEMPT_EXCEEDED',
                                                                                                          'OUTSTANDING_CREDIT_PAYMENT_REJECTED',
                                                                                                          'NO_VISIT_ON_CUSTOMER_REQUEST',
                                                                                                          'PAYMENT_NOT_AVAILABLE',
                                                                                                          'NOT_NEEDED_ANYMORE',
                                                                                                          'CHANGED_MY_MIND',
                                                                                                          'ALTERNATE_PROCUREMENT',
                                                                                                          'SHOP_OWNER_NOT_AVAILABLE',
                                                                                                          'PLACED_BY_MISTAKE',
                                                                                                          'NO_VISIT_ON_CD_REQUEST',
                                                                                                          'DUPLICATE_ORDER',
                                                                                                          'SHOP_CLOSED') THEN di.amount_difference
                                                                              ELSE 0
                                                                    END) AS sum_reattempt_amount_jt ,
                                                                    sum(
                                                                    CASE
                                                                              WHEN di.delta_type IN ('RETURN_TO_ORIGIN',
                                                                                                     'MRP_ISSUE')
                                                                              AND       di.reason IN ('CUSTOMER_REATTEMPT_EXCEEDED',
                                                                                                      'OUTSTANDING_CREDIT_PAYMENT_REJECTED',
                                                                                                      'NO_VISIT_ON_CUSTOMER_REQUEST',
                                                                                                      'PAYMENT_NOT_AVAILABLE',
                                                                                                      'NOT_NEEDED_ANYMORE',
                                                                                                      'CHANGED_MY_MIND',
                                                                                                      'ALTERNATE_PROCUREMENT',
                                                                                                      'SHOP_OWNER_NOT_AVAILABLE',
                                                                                                      'PLACED_BY_MISTAKE',
                                                                                                      'NO_VISIT_ON_CD_REQUEST',
                                                                                                      'DUPLICATE_ORDER',
                                                                                                      'SHOP_CLOSED') THEN di.amount_difference
                                                                              ELSE 0
                                                                    END) AS sum_return_amount_cust ,
                                                                    sum(
                                                                    CASE
                                                                              WHEN di.delta_type IN ('RETURN_TO_ORIGIN',
                                                                                                     'MRP_ISSUE')
                                                                              AND       di.reason NOT IN ('CUSTOMER_REATTEMPT_EXCEEDED',
                                                                                                          'OUTSTANDING_CREDIT_PAYMENT_REJECTED',
                                                                                                          'NO_VISIT_ON_CUSTOMER_REQUEST',
                                                                                                          'PAYMENT_NOT_AVAILABLE',
                                                                                                          'NOT_NEEDED_ANYMORE',
                                                                                                          'CHANGED_MY_MIND',
                                                                                                          'ALTERNATE_PROCUREMENT',
                                                                                                          'SHOP_OWNER_NOT_AVAILABLE',
                                                                                                          'PLACED_BY_MISTAKE',
                                                                                                          'NO_VISIT_ON_CD_REQUEST',
                                                                                                          'DUPLICATE_ORDER',
                                                                                                          'SHOP_CLOSED') THEN di.amount_difference
                                                                              ELSE 0
                                                                    END) AS sum_return_amount_jt,
                                                                    sum(
                                                                    CASE
                                                                              WHEN di.delta_type = 'MISSING' THEN di.amount_difference
                                                                              ELSE 0
                                                                    END) AS sum_missing_amount ,
                                                                    sum(
                                                                    CASE
                                                                              WHEN entity_type IN ('RETURN_TO_ORIGIN',
                                                                                                   'REATTEMPT') THEN di.amount_difference
                                                                              ELSE pem.expected_amount
                                                                    END)                        AS sum_total_amount,
                                                                    isnull(post_delivery_gmv,0) AS post_delivery_return_gmv,
                                                                    total_trips,
                                                                    perfect_delivery,
                                                                    complete_rto_trips,
                                                                    complete_reattempt_trips
                                                          FROM      payment_entity_mapping pem
                                                          LEFT JOIN bolt_order_item_v2_snapshot ord
                                                          ON        pem.entity_id=ord.order_item_id
                                                          LEFT JOIN delta_item di
                                                          ON        pem.mapping_id=di.mapping_id
                                                          JOIN      customer_snapshot_ c
                                                          ON        ord.buyer_id=c.customerid
                                                          JOIN
                                                                    (
                                                                             SELECT  
                                                                                      businessid,
                                                                                      count(DISTINCT trip_id) AS total_trips,
                                                                                      count(DISTINCT
                                                                                      CASE
                                                                                               WHEN order_items = reattempt_order_items
                                                                                               AND      rto_order_items+reattempt_order_items+delivered_items = order_items THEN trip_id
                                                                                      END) AS complete_reattempt_trips,
                                                                                      count(DISTINCT
                                                                                      CASE
                                                                                               WHEN order_items = rto_order_items
                                                                                               AND      rto_order_items+reattempt_order_items+delivered_items = order_items THEN trip_id
                                                                                      END) AS complete_rto_trips,
                                                                                      count(DISTINCT
                                                                                      CASE
                                                                                               WHEN order_items = delivered_items
                                                                                               AND      rto_order_items+reattempt_order_items+delivered_items = order_items THEN trip_id
                                                                                      END) AS perfect_delivery
                                                                             FROM     (
                                                                                               SELECT   
                                                                                                        businessid,
                                                                                                        trip_id,
                                                                                                        count(DISTINCT entity_id) AS order_items,
                                                                                                        count(DISTINCT
                                                                                                        CASE
                                                                                                                 WHEN entity_type IN ('RETURN_TO_ORIGIN')
                                                                                                                 AND      reason  IN ('CUSTOMER_REATTEMPT_EXCEEDED',
                                                                                                                                      'OUTSTANDING_CREDIT_PAYMENT_REJECTED',
                                                                                                                                      'NO_VISIT_ON_CUSTOMER_REQUEST',
                                                                                                                                      'PAYMENT_NOT_AVAILABLE',
                                                                                                                                      'NOT_NEEDED_ANYMORE',
                                                                                                                                      'CHANGED_MY_MIND',
                                                                                                                                      'ALTERNATE_PROCUREMENT',
                                                                                                                                      'SHOP_OWNER_NOT_AVAILABLE',
                                                                                                                                      'PLACED_BY_MISTAKE',
                                                                                                                                      'NO_VISIT_ON_CD_REQUEST',
                                                                                                                                      'DUPLICATE_ORDER',
                                                                                                                                      'SHOP_CLOSED') THEN entity_id
                                                                                                        END) AS rto_order_items,
                                                                                                        count(DISTINCT
                                                                                                        CASE
                                                                                                                 WHEN entity_type IN ('REATTEMPT')
                                                                                                                 AND      reason  IN ('CUSTOMER_REATTEMPT_EXCEEDED',
                                                                                                                                      'OUTSTANDING_CREDIT_PAYMENT_REJECTED',
                                                                                                                                      'NO_VISIT_ON_CUSTOMER_REQUEST',
                                                                                                                                      'PAYMENT_NOT_AVAILABLE',
                                                                                                                                      'NOT_NEEDED_ANYMORE',
                                                                                                                                      'CHANGED_MY_MIND',
                                                                                                                                      'ALTERNATE_PROCUREMENT',
                                                                                                                                      'SHOP_OWNER_NOT_AVAILABLE',
                                                                                                                                      'PLACED_BY_MISTAKE',
                                                                                                                                      'NO_VISIT_ON_CD_REQUEST',
                                                                                                                                      'DUPLICATE_ORDER',
                                                                                                                                      'SHOP_CLOSED') THEN entity_id
                                                                                                        END) AS reattempt_order_items,
                                                                                                        count(DISTINCT
                                                                                                        CASE
                                                                                                                 WHEN entity_type IN ('DELIVERED') THEN entity_id
                                                                                                        END) AS delivered_items
                                                                                               FROM    (
                                                                                                                  SELECT    
                                                                                                                            c.businessid,
                                                                                                                            t.trip_id,
                                                                                                                            pem.entity_id,
                                                                                                                            pem.entity_type,
                                                                                                                            di.reason
                                                                                                                  FROM      payment_entity_mapping pem
                                                                                                                  LEFT JOIN bolt_order_item_v2_snapshot ord
                                                                                                                  ON        pem.entity_id=ord.order_item_id
                                                                                                                  LEFT JOIN delta_item di
                                                                                                                  ON        pem.mapping_id=di.mapping_id
                                                                                                                  JOIN      customer_snapshot_ c
                                                                                                                  ON        ord.buyer_id=c.customerid
                                                                                                                  JOIN      payment py
                                                                                                                  ON        pem.payment_id = py.payment_id
                                                                                                                  JOIN      dw_shipment.trip_node tn
                                                                                                                  ON        tn.node_id = RIGHT( py.trip_node_id, LEN(py.trip_node_id) - 4)
                                                                                                                  AND       tn.deleted_at IS NULL
                                                                                                                  JOIN      dw_shipment.trip t
                                                                                                                  ON        t.trip_id = tn.trip_id
                                                                                                                  AND       t.deleted_at IS NULL
                                                                                                                  WHERE     trunc(pem.created_time) >= '2021-12-18'
                                                                                                                  AND       trunc(pem.created_time) <= '2022-02-18'
                                                                                                                  AND       pem.deleted_at IS NULL
                                                                                                                  AND       pem.is_deleted IS NULL
                                                                                                                  AND       di.deleted_at IS NULL )
                                                                                               GROUP BY 1,
                                                                                                        2
                                                                                                        )
                                                                             WHERE    order_items > 0
                                                                             GROUP BY 1
                                                                                      ) tm
                                                          ON        tm.businessid = c.businessid

                                                          LEFT JOIN
                                                                    (
                                                                             SELECT   
                                                                                      cs.businessid,
                                                                                      sum((
                                                                                      CASE
                                                                                               WHEN rs.return_state::text <> 'REJECTED'::character VARYING::text
                                                                                               AND      rs.return_state::text <> 'CANCELLED'::character VARYING::text
                                                                                               AND      rs.return_state::text <> 'APPROVED'::character VARYING::text
                                                                                               AND      rs.is_rto IS false THEN rs.return_item_units
                                                                                               ELSE 0
                                                                                      END)*((ord.order_item_amount + ord.shipping_charges) / ord.quantity)) AS post_delivery_gmv
                                                                             FROM     return_item_snapshot rs
                                                                             JOIN     bolt_order_item_v2_snapshot ord
                                                                             ON       ord.order_item_id = rs.order_item_id
                                                                             JOIN     customer_snapshot_ cs
                                                                             ON       cs.customerid = ord.buyer_id
                                                                             WHERE    is_rto IS false
                                                                             AND      ord.boltordertype = 'MARKETPLACE'
                                                                             AND      date(rs.src_created_time) >= '2021-12-18'
                                                                             GROUP BY 1
                                                                                      ) post
                                                          ON        post.businessid = c.businessid

                                                          WHERE     trunc(pem.created_time) >= '2021-12-18'
                                                          AND       trunc(pem.created_time) <= '2022-02-18'
                                                          AND       pem.deleted_at IS NULL
                                                          AND       pem.is_deleted IS NULL
                                                          AND       di.deleted_at IS NULL
                                                          GROUP BY  1,
                                                                    9,
                                                                    10,
                                                                    11,
                                                                    12,
                                                                    13

                                                          ORDER BY  1,
                                                                    2) ra
                                      ON        os.businessid = ra.businessid

                                      WHERE     gmv_net >= 0 
                                      ) final
            """,
            "queryString_app": """with  cal as (select * from calendar
                              where calendar.calendardate >= '2021-12-18' and calendar.calendardate <= '2022-02-18'
                              )


            select  c.businessid,
            count ( distinct case when h.en ='ON_APP_CAME_TO_FG' then  cal.calendardate end) cta_dt_cnt,
            count ( distinct case when h.en in('ON_LOAD_PRODUCT_LIST_SCREEN','ON_LOAD_PRODUCT_SCREEN')then cal.calendardate end) ppv_plv_dt_cnt,
            count ( distinct case when h.en in('ON_TAP_GO_TO_CART','ON_TAP_CART_BOX') then cal.calendardate end) atc_dt_cnt

            from (select * from hevo_customer_app_events_webhook he where he.en in ('ON_APP_CAME_TO_FG','ON_LOAD_PRODUCT_LIST_SCREEN',
                         'ON_LOAD_PRODUCT_SCREEN',
                         'ON_TAP_GO_TO_CART','ON_TAP_CART_BOX')          
                  and he.uid is not null) as h

            left join customer_snapshot_ c on h.uid = c.customerid  
            inner join cal on cast(date(timestamp 'epoch' + (h.ets / 1000) * interval '1 second' + interval '5 hours 30 minutes')as timestamp) = cal.calendardate 
            and 
            c.istestcustomer is FALSE

            and c.businessid is not null
            and c.businessid not in ('BZID-testPuja'
                                    , 'BZID-tech'
                                    , 'BZID-sajal'
                                    , 'BZID-merchCatalog'
                                    , 'BZID-1304457254'
                                    , 'BZID-1304463418')

            group by 1

            """,
            "visits_query": """

                    select businessid,  count(distinct time_stamp) as total_visits


                    from cs_revisits_data
                    where date(time_stamp) >= date('2021-12-18')
                    and date(time_stamp) <= date('2022-02-18')

                     group by 1


                    """,
            "calls_query": """

                    select businessid, count(distinct comm_timestamp) calls


                    from 
                    growth_ops_calling_data
                    where date(comm_timestamp) >= date('2021-12-18')
                    and date(comm_timestamp) <= date('2022-02-18')

                     group by 1


                    """,
            "credit_base_query": """

              select 

                 cut.bz_id,
                 cl.status,
                 cred.credit_onboard,
                 cl.avg_days_past_due,
                 cl.current_limit as currentlimit,
                 cl.overall_limit as overalllimit,
                 cl.total_bounced as totalbounced,
                 cl.total_outstanding as totaloutstanding,
                 cl.total_outstanding_bounced as totaloutstandingbounced,
                 cl.total_credit_ever_used as totalcreditused,
                 cl.total_bounced_count as totalbouncedcount,
                 cl.total_outstanding_bounced_count as totaloutstandingbouncedcount,
                 cl.total_outstanding_count as totaloutstandingcount,
                 cl.total_credit_ever_used_count as totalcreditusedcount

                from credit_line cl
                left join credit_product cp on cl.credit_product_id = cp.product_id
                left join credit_user_type cut on cl.credit_user_type_mapping_id = cut.id
                right join   (select 

                        cut.bz_id,
                        cl.status,

                        max(date(TIMESTAMP 'epoch' + cl.start_date/1000 *INTERVAL '1 second')) as  credit_onboard


                        from
                          credit_line cl
                          left join credit_product cp on cl.credit_product_id = cp.product_id
                          left join credit_user_type cut on cl.credit_user_type_mapping_id = cut.id
                        where
                            cp.name not in('DUMMY_PRODUCT')
                         -- cp.product_id not in ( '2500541') 
                        and cp.name not in ('LoanTap-DPN','DeHaat-BlackSoil','LoanTap-DPN','DUMMY_PRODUCT','JT-Institutional-Sales','JT-BILL2BILL')
                        --  and 
                        and cut.bz_id like 'BZID%'
                        group by
                          1,2
                        order by 2,1) as cred

                on cred.bz_id = cut.bz_id
                and cred.status = cl.status
                and cred.credit_onboard = date(TIMESTAMP 'epoch' + cl.start_date/1000 *INTERVAL '1 second')



            """,
            "credit_utilization_query": """

              select bz_id, avg(utilization) as avg_daily_utilzation
            from (select *,
            date(timestamp 'epoch' + (cdt.created_time/1000) * interval '1 second' + interval '5 hours 30 minutes') as created_date,
            cdt.created_time,

            value,
            cla.overall_limit,
            (value/NULLIF(cla.overall_limit,0)*100) as utilization

            from credit_transaction ct
            join credit_transaction_details cdt on cdt.credit_transaction = ct.id
            left join (select *,
                       max(cl.created_time) over (partition by cl.id, 
                                                  date(timestamp 'epoch' + (cl.created_time/1000) * interval '1 second' + interval '5 hours 30 minutes') 
                                                  ) as max_ts
                       from credit_line_audit cl
                       where status = 'ACTIVE' ) cla on ct.credit_line_id = cla.id
            left join credit_user_type cut on cla.credit_user_type_mapping_id = cut.id
            where transaction_type = 'DEBIT'
            and cdt.amount_type = 'BASE'
            and date(timestamp 'epoch' + (cdt.created_time/1000) * interval '1 second' + interval '5 hours 30 minutes') >= '2021-12-18'
            and date(timestamp 'epoch' + (cdt.created_time/1000) * interval '1 second' + interval '5 hours 30 minutes') <= '2022-02-18'
            and max_ts = cla.created_time
            )
            group by 1


            """,
            "dsat_query": """
                SELECT   rg.businessid,
                     Count(rg.rating) AS rating_cnt,
                     ROUND(Avg(rg.rating)) AS avg_rating
            FROM     (
                            SELECT *
                            FROM   (
                                             SELECT    date(timestamp 'epoch' + (ets/1000) * interval '1 second' + interval '5 hours 30 minutes') AS dt,
                                                       uid ,
                                                       cs.businessid AS businessid,
                                                       sid,
                                                       seq,
                                                       srv_req_ent_id,
                                                       srv_id                                                      AS survey_id,
                                                       srv_ans_val/1.00                                                 AS rating
                                                       --row_number() OVER (partition BY uid, sid ORDER BY seq DESC) AS rnk
                                             FROM      hevo_customer_app_events_webhook
                                             LEFT JOIN customer_snapshot_ cs
                                             ON        cs.customerid = hevo_customer_app_events_webhook.uid
                                             JOIN      address_snapshot_ ads
                                             ON        ads.addressentityid=cs.businessid
                                             AND       addresstype='SHIPPING'
                                             AND       cs.businessid NOT IN ( 'BZID-testPuja' ,
                                                                             'BZID-tech' ,
                                                                             'BZID-sajal' ,
                                                                             'BZID-merchCatalog' ,
                                                                             'BZID-1304457254' ,
                                                                             'BZID-1304463418',
                                                                             'BZID-hubballi',
                                                                             'BZID-1304433825',
                                                                             'BZID-1304436504',
                                                                             'BZID-1304435850' )
                                             WHERE     en = 'ON_SURVEY_RATING_CHANGED'
                                             AND       srv_que_id = 'QES-182'
                                             AND       date(timestamp 'epoch' + (ets/1000) * interval '1 second' + interval '5 hours 30 minutes') >= '2021-12-18'
                                             AND       date(timestamp 'epoch' + (ets/1000) * interval '1 second' + interval '5 hours 30 minutes') <= '2022-02-18' )
                    ) rg
            JOIN
                     (
                               SELECT    date(timestamp 'epoch' + (ets/1000) * interval '1 second' + interval '5 hours 30 minutes') AS dt,
                                         uid ,
                                         sid,
                                         seq,
                                         srv_req_ent_id,
                                         srv_id      AS survey_id,
                                         srv_ans_val AS rating
                               FROM      hevo_customer_app_events_webhook
                               LEFT JOIN customer_snapshot_ cs
                               ON        cs.customerid = hevo_customer_app_events_webhook.uid
                               JOIN      address_snapshot_ ads
                               ON        ads.addressentityid=cs.businessid
                               AND       addresstype='SHIPPING'
                               AND       cs.businessid NOT IN ( 'BZID-testPuja' ,
                                                               'BZID-tech' ,
                                                               'BZID-sajal' ,
                                                               'BZID-merchCatalog' ,
                                                               'BZID-1304457254' ,
                                                               'BZID-1304463418',
                                                               'BZID-hubballi',
                                                               'BZID-1304433825',
                                                               'BZID-1304436504',
                                                               'BZID-1304435850' )
                               WHERE     en = 'ON_SURVEY_SUBMIT'
                               AND       date(timestamp 'epoch' + (ets/1000) * interval '1 second' + interval '5 hours 30 minutes') >= '2021-12-18'
                               AND       date(timestamp 'epoch' + (ets/1000) * interval '1 second' + interval '5 hours 30 minutes') <= '2022-02-18' ) ss
                      ON       ss.dt = rg.dt
                      AND      ss.uid = rg.uid
                      AND      ss.srv_req_ent_id = rg.srv_req_ent_id

            --where businessid = 'BZID-1304472890'
            group by 1




            """,
            "target_scheme_query": """
                select 
                customer as businessid, 
                count(distinct target_scheme_id) as target_schemes_count,
                count(distinct( case when milestone_crossed_cv > 0 then milestone_crossed_cv end)) as milestones_achieved_count,
                sum(jc_payout) as total_JC_earned

            from
            (select target_scheme_id, natural_id,description, objective, title, internal_scheme_name,internal_scheme_description, filter_entity_id as Customer,

             sum(case when current_value is not null then current_value else 0 end) as current_value, sum(case when jc_payout > 0 then current_value else 0 end) as milestone_crossed_CV,sum(case when jc_payout is not null then jc_payout else 0 end) as jc_payout, sum(case when burn is not null then burn else 0 end) as burn

            from
            (
            select *, 
              case when payout_type = 'ABSOLUTE' then payout_val * 1.00
                   when payout_type = 'PERCENTAGE' then payout_val * 1.00 * 0.01 * current_value 
                   end as jc_payout, 
              case when payout_type = 'ABSOLUTE' then payout_val * 1.00 * 0.85 
                   when payout_type = 'PERCENTAGE' then payout_val * 1.00 * 0.01 * current_value * 0.85 
                   end as burn
            from
            (
            select ts.target_scheme_id, ts.natural_id, ts.description, ts.objective, ts.title, ts.internal_scheme_name,ts.internal_scheme_description, gir.filter_entity_id, smt.current_value, 
                case when num_ms = 3 then
            (
                    case when ms1 > current_value then 0
                    when ms1 <= current_value and ms2 > current_value then ms1_payout_val
                    when ms2 <= current_value and ms3 > current_value then ms2_payout_val
                    when ms3 <= current_value then ms3_payout_val end
              )
               when num_ms = 2 then 
            (
              case when ms1 > current_value then 0
                    when ms1 <= current_value and ms2 > current_value then ms1_payout_val
                    when ms2 <= current_value then ms2_payout_val end
              )
            when num_ms = 1 then
            (
              case when ms1 > current_value then 0
                    when ms1 <= current_value then ms1_payout_val end
              ) end
            as payout_val,
            case when num_ms = 3 then
            (
                    case when ms1 > current_value then '0'
                    when ms1 <= current_value and ms2 > current_value then ms1_payout_mode
                    when ms2 <= current_value and ms3 > current_value then ms2_payout_mode
                    when ms3 <= current_value then ms3_payout_mode end
              )
               when num_ms = 2 then 
            (
              case when ms1 > current_value then '0'
                    when ms1 <= current_value and ms2 > current_value then ms1_payout_mode
                    when ms2 <= current_value then ms2_payout_mode end
              )
            when num_ms = 1 then
            (
              case when ms1 > current_value then '0'
                    when ms1 <= current_value then ms1_payout_mode end
              ) end
            as payout_mode,
            case when num_ms = 3 then
            (
                    case when ms1 > current_value then '0'
                    when ms1 <= current_value and ms2 > current_value then ms1_payout_type
                    when ms2 <= current_value and ms3 > current_value then ms2_payout_type
                    when ms3 <= current_value then ms3_payout_type end
              )
               when num_ms = 2 then 
            (
              case when ms1 > current_value then '0'
                    when ms1 <= current_value and ms2 > current_value then ms1_payout_type
                    when ms2 <= current_value then ms2_payout_type end
              )
            when num_ms = 1 then
            (
              case when ms1 > current_value then '0'
                    when ms1 <= current_value then ms1_payout_type end
              ) end
            as payout_type,
                    ms.*

            from dw_target_scheme.target_scheme ts
            left join dw_target_scheme.group_inclusion_rules gir on gir.target_scheme_id = ts.target_scheme_id and gir.member_entity_type = 'BUSINESS'
            left join dw_target_scheme.scheme_member_target smt on smt.target_scheme_id = ts.target_scheme_id and smt.member_id = gir.filter_entity_id
            left join (select m1.target_scheme_id as ts, m1.at_value as ms1, m2.at_value as ms2, m3.at_value as ms3,  m1.value as ms1_payout_val, m1.payout_mode as ms1_payout_mode, m1.payout_type as ms1_payout_type, m2.value as ms2_payout_val, m2.payout_mode as ms2_payout_mode, m2.payout_type as ms2_payout_type, m3.value as ms3_payout_val, m3.payout_mode as ms3_payout_mode, m3.payout_type as ms3_payout_type, num_ms
                       from (select ms.target_scheme_id, ms.at_value, p.value, p.payout_mode, p.payout_type 
                             from dw_target_scheme.milestone ms left join dw_target_scheme.payout p on p.milestone_id = ms.milestone_id) m1
            left join (select ms.target_scheme_id, ms.at_value, p.value, p.payout_mode, p.payout_type from dw_target_scheme.milestone ms left join dw_target_scheme.payout p on p.milestone_id = ms.milestone_id) m2 on m2.target_scheme_id = m1.target_scheme_id and m1.at_value < m2.at_value
            left join (select ms.target_scheme_id, ms.at_value, p.value, p.payout_mode, p.payout_type from dw_target_scheme.milestone ms left join dw_target_scheme.payout p on p.milestone_id = ms.milestone_id) m3 on m3.target_scheme_id = m1.target_scheme_id and m2.at_value < m3.at_value
            left join 
            (
            select target_scheme_id as ts, count(distinct milestone_id) as num_ms
            from dw_target_scheme.milestone
            group by 1
            ) a on a.ts = m1.target_scheme_id
            where case when a.num_ms = 1 then m1.at_value is not null and m2.at_value is null and m3.at_value is null
                        when a.num_ms = 2 then m1.at_value is not null and m2.at_value is not null and m3.at_value is null
                        when a.num_ms = 3 then m1.at_value is not null and m2.at_value is not null and m3.at_value is not null
                        else false end) ms on ms.ts = ts.target_scheme_id
            where ts.target_scheme_status = 'ACTIVE' 
            --   and date_add(date_add(from_unixtime(ts.end_time/1000), interval '5 hours'),interval '30 minutes') >= '2022-01-01'
              and date(timestamp 'epoch' + (ts.end_time/1000) * interval '1 second' + interval '5 hours 30 minutes') >= '2021-12-18'
              and date(timestamp 'epoch' + (ts.end_time/1000) * interval '1 second' + interval '5 hours 30 minutes') <= '2022-02-18'

             --  ##and ts.target_scheme_id in (100003202, 100003203)
            ) a
              ) a
            group by 1,2,3,4,5,6,7,8) o
            where current_value > 0
            group by 1


            """,
            "superclub_query": """
                select business_id, sum(points_redeemed) as sc_points_red, count(distinct reward_id) as sc_rewards_count
            from dw_superclub.redeemed_rewards
            where current_status not in ('CANCELLED','Cancelled','cancelled')
            and date(rs_last_updated_time) > '2021-10-18'
            and date(rs_last_updated_time) <= '2022-02-18'
            group by 1

            """,
            "null_search_query": """

            WITH base AS
            (
                   SELECT *
                          --   dt
                          --   , en_plus_1
                          --   , count(*) as occ
                   FROM   (
                                   SELECT   * ,
                                            Lag(en, 1) OVER(partition BY sid ORDER BY seq) AS en_plus_1 ,
                                            Lag(en, 2) OVER(partition BY sid ORDER BY seq) AS en_plus_2
                                   FROM     (
                                                      SELECT
                                                                --ets
                                                                cs.businessid ,
                                                                uid ,
                                                                en ,
                                                                sid ,
                                                                seq ,
                                                                eid ,
                                                                calendar.month
                                                      FROM      hevo_customer_app_events_webhook
                                                      LEFT JOIN customer_snapshot_ cs
                                                      ON        cs.customerid = hevo_customer_app_events_webhook.uid
                                                      JOIN      address_snapshot_ ads
                                                      ON        ads.addressentityid = cs.businessid
                                                      AND       addresstype = 'SHIPPING'
                                                      AND       cs.businessid NOT IN ( 'BZID-testPuja' ,
                                                                                      'BZID-tech' ,
                                                                                      'BZID-sajal' ,
                                                                                      'BZID-merchCatalog' ,
                                                                                      'BZID-1304457254' ,
                                                                                      'BZID-1304463418' ,
                                                                                      'BZID-hubballi' ,
                                                                                      'BZID-1304433825' ,
                                                                                      'BZID-1304436504' ,
                                                                                      'BZID-1304435850' )
                                                      LEFT JOIN calendar
                                                      ON        date(timestamp 'epoch' + (ets / 1000) * interval '1 second' + interval '5 hours 30 minutes') = calendar.calendardate
                                                      WHERE
                                                                --           etype = 'UA'
                                                                cat IN ( 'SEARCH' ,
                                                                        'PRODUCT' )
                                                      AND       calendar.calendardate <= '2022-02-18'
                                                      AND       calendar.calendardate >= '2021-12-18'
                                                                --and ets < extract('epoch' from current_date + 1 )::BIGINT * 1000
                                                                --and  ads.addresscity in ('Bengaluru','Bangalore','Chikkaballapura','Tumkur','Hosur',
                                                                --'Mysore','Mandya','Hassan','Hubballi','Belgaum','Dharwad','Davanagere','Haveri',
                                                                --'Pune','Hyderabad')
                                                      AND       appvc IN
                                                                          (
                                                                          SELECT DISTINCT appvc
                                                                          FROM            hevo_customer_app_events_webhook) ) )
                   WHERE  en IN ( 'ON_ERROR_EMPTY_PRODUCT_LIST_SCREEN' )
                   AND    (
                                 en_plus_1 NOT IN ( 'ON_LOAD_PRODUCT_LIST_SCREEN' ,
                                                   'ON_ERROR_EMPTY_PRODUCT_LIST_SCREEN' )
                          OR     (
                                        en_plus_2 = 'ON_SUBMIT_SEARCH_QUERY' ) )
                   AND    en_plus_1 IS NOT NULL )
            SELECT   businessid ,
                     count(*) AS null_search_cnt
            FROM     base
            GROUP BY 1
            ORDER BY 1



            """,
        }
