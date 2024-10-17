-- Lists all bands with "Glam rock" ,ranked by longevity --
SELECT band_name, (IFNULL(CAST(split AS UNSIGNED), 2020) - formed) AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', IFNULL(style, '')) > 0
ORDER BY lifespan DESC;
