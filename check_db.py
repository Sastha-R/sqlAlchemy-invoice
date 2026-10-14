from database.database import engine


def main() -> None:
    with engine.connect() as connection:
        connection.exec_driver_sql("SELECT 1")
    print("Database connection successful")


if __name__ == "__main__":
    main()
