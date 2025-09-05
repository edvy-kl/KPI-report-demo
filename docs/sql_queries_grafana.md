## SQL queries used for visuals on Grafana dashboard:

### Total monthly tickets:
```sql
SELECT 
	    month_start,
	    COUNT(*) AS total_tickets
	FROM (
	    SELECT 	      
	        DATE_TRUNC('month', time_created) AS month_start
	    FROM $schema.$table
	) AS t
	GROUP BY month_start
	ORDER BY month_start;
```
### Ticket status overview:
```sql
SELECT status,
	    COUNT(*) AS total_tickets
	    FROM $schema.$table
	WHERE active = false
	GROUP BY status;
```
### Time to first response:
```sql
SELECT
month_start,
AVG((EXTRACT (EPOCH from time_assigned) - EXTRACT (EPOCH from time_created))/60)::INT AS time_to_first_response
FROM(
  SELECT 
  time_assigned,
  time_created,
  DATE_TRUNC('month', time_created) AS month_start
  FROM $schema.$table
) AS t
GROUP BY month_start
ORDER BY month_start
```
### Time to resolution:
```sql
SELECT  month_start,
   EXTRACT(EPOCH FROM AVG(time_closed - time_created)) / 3600 AS time_to_resolution
FROM (
    SELECT 
        DATE_TRUNC('month', time_created) AS month_start,
        time_created,
        time_closed
    FROM $schema.$table
) t
GROUP BY month_start
ORDER BY month_start;
```
### Ticket closure rate:
```sql
	SELECT 
	    month_start,
	    ROUND(
	        AVG(
	            CASE 
	                WHEN (time_closed - time_created) <= INTERVAL '48 hours' 
	                THEN 1 
	                ELSE 0 
	            END
	        ) * 100, 2
	    ) AS rate
	FROM (
	    SELECT 
	        time_closed, 
	        time_created,
	        DATE_TRUNC('month', time_created) AS month_start
	    FROM $schema.$table
	) t
	GROUP BY month_start
ORDER BY month_start;
```
### Callback incidents:
```sql
SELECT 
COUNT (ticket_id) AS no_of_tickets,
month_start
	FROM (
	    SELECT 	  
		ticket_id,
	        DATE_TRUNC('month', time_created) AS month_start
	    FROM $schema.$table
		WHERE needed_call = true
	) AS t
GROUP BY month_start
ORDER BY month_start;
```
### Customer rating:
```sql
	SELECT ROUND(AVG(success_rate),2) AS customer_rating,
		    month_start
		FROM (
		    SELECT 	  
			success_rate,
		        DATE_TRUNC('month', time_created) AS month_start
		    FROM $schema.$table
		) AS t
		GROUP BY month_start
		ORDER BY month_start;
```