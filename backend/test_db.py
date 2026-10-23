import os
from sqlalchemy import create_engine, text

# simple .env reader (no extra library needed)
for line in open(".env"):
    if "=" in line and not line.startswith("#"):
        k, v = line.strip().split("=", 1)
        os.environ[k] = v

engine = create_engine(os.environ["DATABASE_URL"])
with engine.connect() as conn:
    print(conn.execute(text("SELECT 'Database connected!'")).scalar())