-- 2-fans.sql
-- Task 2: Best band ever!

-- Query to rank country origins of bands by the number of fans
SELECT origin, SUM(fan) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;

