def test_exception_and_logger():
    try:
        x=1/0
    except Exception as e:
        raise CustomException(e, sys)

if __name__ == "__main__":
    try:
        test_exception_and_logger()
    except Exception as e:
        logging.info(f"error: {e}")
        print(e)

    

