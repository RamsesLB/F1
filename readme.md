# F1 schedule
![Render](https://img.shields.io/badge/Render-%46E3B7.svg?style=flat&logo=render&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=flat&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=flat&logo=bootstrap&logoColor=white)

**F1 Schedule** (https://f1.adsumy.com/) is a lightweight, fast Django web application built for my portfolio. It displays the current Formula 1 racing schedule dynamically adapted to the user's local timezone. 

Upon loading, the application automatically scrolls to the next upcoming race, ensuring a seamless user experience. 

## The problem it solves
Finding out exactly when an F1 session starts can be frustrating. Even the official F1 website lacks a straightforward, immediate view of the next race's date and time on its landing page. Other motorsport sites are often packed with ads or present confusing, multi-timezone tables. 

F1 Schedule solves this by delivering a clean, ad-free interface that instantly converts all session times (Practice, Qualifying, Sprint, and Race) to the user's system timezone the moment the page loads.

## Architecture & Workflow
To ensure high performance and respect external API rate limits, the backend implements a strict caching and database fallback strategy using the [Jolpi Ergast API](https://api.jolpi.ca/ergast/):

1. **Cache Check:** Django checks its internal cache (`f1_schedule_{year}`). If valid, data is served immediately without database queries.
2. **Database Fallback:** If the cache is empty, it queries the local database.
3. **API Fetch & Populate:** If the database is empty (e.g., after a fresh deployment or server restart), the app fetches the full season data from the external API, populates the database, and serves the data.
4. **Cache Set:** Finally, the retrieved data is stored in the Django cache for 24 hours to handle high traffic efficiently.

## Tech Stack
* **Backend:** Python, Django, SQLite
* **Frontend:** HTML, CSS, JavaScript (Vanilla), Bootstrap 5
* **Deployment & Serving:** Hosted on Render, static files served via WhiteNoise

