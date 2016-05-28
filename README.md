# sports-roster-api
A free, open source alternative to Sportradar or ESPN's API

I was looking for an API to use to get rosters for teams in various leagues, but they all cost money. I knew that all of the data was easily available on ESPN.com, so I wrote a simple scraper to get the data I need.

### Installation
 - Clone repository
 - If you want updated rosters, run the roster_scraper.py.
   - Example: `python roster_scraper.py -s NBA`
   - This will overwrite the json file associated with that sport
 - Install dependencies for server
   - `npm install`
 - Run server
   - `node sports-roster-server.js`
