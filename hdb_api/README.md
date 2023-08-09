[![N|Solid](https://www.usbr.gov/uc/water/hydrodata/assets/img/BofR-horiz-cmyk.png)](https://www.usbr.gov/)
# A python wrapper for the [HDB API](http://ibr3lcrsrv02.bor.doi.net/swagger/ui/index)
 Creates native Python objects or pandas dataframes from HDB API endpoints
  - [Pandas](https://pandas.pydata.org/)
    -     
        -   pip install pandas

  - [SQLAlchemy](https://www.sqlalchemy.org/)
    - 
        - pip install sqlalchemy

# What's new?

  - UC API url
    -
      - [http://ibr3lcrsrv02.bor.doi.net/swagger/ui/index](http://ibr3lcrsrv02.bor.doi.net/swagger/ui/index)
  - LC API url
    - 
      - [http://ibr4ucrap020.bor.doi.net/swagger/ui/index](http://ibr4ucrap020.bor.doi.net/swagger/ui/index)
  
# Config example:
  - Create a file hdb_api/hdb_config.json (or designate a path explictly in use)
  ```
  {
  "uc": {
    "dialect": "oracle",
    "driver": "cx_oracle",
    "username": "uc_username",
    "psswrd": "password",
    "port": "1521",
    "host": "host.bor.doi.net",
    "database": "db_name"
  },
  "lc": {
    "dialect": "oracle",
    "driver": "cx_oracle",
    "username": "lc_username",
    "psswrd": "password",
    "port": "1521",
    "host": "host.bor.doi.net",
    "database": "db_name"
  }
}
```