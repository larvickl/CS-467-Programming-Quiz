import datetime as dt
import sqlalchemy.types as types


class TZDateTime(types.TypeDecorator):
    """A database column type that enforces correct time zones.  Aware datetimes
    are first converted to UTC and then have the tzinfo removed before committing
    to the database.  Naive datetimes are rejected.  The UTC time zone is added to
    all results retrieved from the database."""
    impl = types.DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """This method will reject naive datetimes and convert aware datetimes to
        UTC before committing to the database as a UTC naive datetime."""
        if value is not None:
            if not value.tzinfo or value.tzinfo.utcoffset(value) is None:
                raise TypeError("tzinfo is required")
            value = value.astimezone(dt.timezone.utc).replace(tzinfo=None)
        return value

    def process_result_value(self, value, dialect):
        """This method will convert datetimes from the database to aware UTC datetimes."""
        if value is not None:
            value = value.replace(tzinfo=dt.timezone.utc)
        return value
    
