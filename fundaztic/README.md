## Notes
1. Although it would be better to separate the webscraping and data cleaning/reporting, I have chosen to bundle it into one application (main.py) for now
2. The app will be scheduled as a cron job on a Linux OCI instance


## Future Improvements
1. Implement retry logic on the login flow - captcha solve rate stands at around 70%.
2. Add more informative logging.
3. Remove explicit wait for file download - replace with a better solution.
