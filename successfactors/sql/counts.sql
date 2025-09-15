SELECT 'staging_billionaires' AS table, COUNT(*) AS rows FROM staging_billionaires
UNION ALL
SELECT 'billionaires', COUNT(*) FROM billionaires;
