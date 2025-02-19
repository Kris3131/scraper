from database import init_db


def main():
    try: 
        init_db()
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Exiting gracefully...")
        return
    except Exception as e:
        print(f"Error initializing database: {e}")
        return    

if __name__ == "__main__":
    main()            