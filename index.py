from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def format_amount(amount):
    # '-2,072.73\n$2,073.08' => 2073.08
    if amount == "":
        return 0
    return float(amount.split("\n")[1].replace("$", "").replace(",", ""))

def open_okx_explorer():
    # 创建Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')  # 最大化窗口
    
    # 创建Chrome浏览器实例
    driver = webdriver.Chrome(options=chrome_options)

    # get url by config.json
    with open("config.json", "r") as f:
        config = json.load(f)
        url = config["url"]
        driver.get(url)
    
    try:
        all_data = []
        page_count = 0
        max_pages = 10

        while page_count < max_pages:
            # 等待表格主体加载完成（最多等待20秒）
            tbody = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "okui-table-tbody"))
            )
            
            # 等待所有行加载完成
            rows = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".okui-table-tbody tr"))
            )
            
            # 获取数据
            for row in rows:
                # 获取当前行的所有列
                columns = row.find_elements(By.TAG_NAME, "td")
                if len(columns) >= 8:
                    date = columns[2].text
                    amount = columns[7].text
                    
                    if date == "" or amount == "":
                        continue
                    # date = 2025/05/09 16:26:21 时间需要等于2025/05/09
                    if date.split(" ")[0] != "2025/05/09":
                        continue
                    all_data.append({
                        "date": date,
                        "amount": format_amount(amount)
                    })
            
            # 点击下一页按钮
            try:
                # 等待下一页按钮可点击
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "okui-pagination-next"))
                )
                next_button.click()
                
                # 等待页面加载完成
                WebDriverWait(driver, 10).until(
                    EC.staleness_of(tbody)
                )
                
                page_count += 1
                print(f"已完成第 {page_count} 页数据提取")
                
            except Exception as e:
                print(f"翻页时发生错误或已到最后一页: {e}")
                break
        
        # 打印所有结果
        print("\n所有数据:")
        for data in all_data:
            print(data)

        # write to file
        with open("data.txt", "w") as f:
            for data in all_data:
                f.write(f"{data['date']} {data['amount']}\n")
        
        print(f"\n总共提取了 {len(all_data)} 条数据")
        input("按回车键关闭浏览器...")
        
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    open_okx_explorer()