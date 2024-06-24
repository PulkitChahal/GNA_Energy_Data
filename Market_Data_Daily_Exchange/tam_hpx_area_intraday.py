import os
import glob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import shutil
import time
from datetime import datetime
from datetime import timedelta
import xlwings as xw


def run():
    try:
        options = Options()
        # options.add_argument("--headless") # Run selenium under headless mode
        prefs = {"download.default_directory": r"C:\GNA\Market Data\test"}
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.hpxindia.com/MarketDepth/TAM/TradeDetails.html")
    except Exception as e:
        return "Webpage Not Found"

    try:
        time.sleep(5)
        # Wait till product is available
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[3]/div/div[1]/div[2]/span[2]/button")
            )
        )

        # Select Product
        data = driver.find_element(
            By.XPATH, "/html/body/div[3]/div/div[1]/div[2]/span[2]/button"
        )
        data.click()
        time.sleep(1)

        # Select Trade Period
        dropdown = Select(
            driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[2]/select")
        )
        your_value = "Yesterday"
        dropdown.select_by_value(your_value)
        time.sleep(1)

        # Update Report
        update = driver.find_element(
            By.XPATH, "/html/body/div[3]/div/div[3]/div[2]/input[1]"
        )
        update.click()
    except Exception as e:
        return "Date Not Selected"

    try:
        try:
            time.sleep(5)
            # Wait till data is available
            driver.find_element(
                By.XPATH, "/html/body/div[4]/div[2]/div/div/div/div[1]/div[1]/table"
            )
        except Exception as e:
            return "Data Not Available"

        # Wait till download button is available
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//html/body/div[4]/div[2]/div/div/div/div[1]/div[1]/table")
            )
        )
        time.sleep(2)

        # Download excel file
        table = driver.find_element(
            By.XPATH, "/html/body/div[4]/div[1]/div/center/div[2]"
        )
        table.click()
    except Exception as e:
        return "Excel File Download could Not Start"

    try:
        path_to_add = r"C:\GNA\Market Data\test"
        if not os.path.exists(path_to_add):
            os.makedirs(path_to_add)
        time.sleep(4)

        for file in glob.glob(os.path.join(path_to_add, "*.xls")):
            print(file)
        else:
            pass

        try:
            # Set Name for File and convert it into .xlsx
            xls_file_path = os.path.join(path_to_add, file)
            prev_date = datetime.today() - timedelta(days=1)
            new_date = prev_date.strftime("%d.%m.%y")
            xlsx_file = (
                "TAM HPX Area Price Intraday_"
                + datetime.now().strftime(new_date)
                + ".xlsx"
            )
            xlsx_file_path = os.path.join(path_to_add, xlsx_file)

            app = xw.App(visible=False)  # Open Excel in the background
            workbook = app.books.open(xls_file_path)
            workbook.save(xlsx_file_path)
            workbook.close()
            app.quit()
            print(f"Conversion completed. File saved at: {xlsx_file_path}")
        except Exception as e:
            return "Either File Not Converted To .xlsx Or Name Not Changed"
        finally:
            # Remove File from test Folder
            os.remove(os.path.join(path_to_add, file))

        try:
            # Make Copy of File to New Folder
            local_path = r"C:\GNA\Market Data\All Data"
            if not os.path.exists(local_path):
                os.makedirs(local_path)
            shutil.copyfile(
                os.path.join(path_to_add, xlsx_file), rf"{local_path}/{xlsx_file}"
            )
            time.sleep(2)

            file_store = r"C:\GNA\Market Data\TAM All Exchanges"
            if not os.path.exists(file_store):
                os.makedirs(file_store)
            shutil.copyfile(
                os.path.join(path_to_add, xlsx_file), rf"{file_store}/{xlsx_file}"
            )
        except Exception as e:
            return "File Not Shifted To Local Path"
        finally:
            # Remove File from test Folder
            os.remove(os.path.join(path_to_add, xlsx_file))

        for file in glob.glob(os.path.join(path_to_add, "*.xlsx.crdownload")):
            print("Error file found:", file)
        else:
            pass
    except Exception as e:
        return "Error in File !Try Again!"

    return "Success"


# run()
