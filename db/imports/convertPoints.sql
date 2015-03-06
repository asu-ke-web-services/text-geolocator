/* Script for converting the points from the latitude and longitude
 *  so that the data doesn't need to be re-imported
 */

UPDATE location
SET location = ST_MakePoint(latitude, longitude)
