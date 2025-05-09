from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def open_okx_explorer():
    # 创建Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')  # 最大化窗口
    
    # 创建Chrome浏览器实例
    driver = webdriver.Chrome(options=chrome_options)
    
    # 打开OKX区块链浏览器页面
    url = "https://web3.okx.com/zh-hans/explorer/tron/address/TWmc23yDyAbPnT8729NEU13TrB3VLP3Dub/token-transfer"
    driver.get(url)
    
    # 保持浏览器窗口打开
    try:
        input("按回车键关闭浏览器...")
    except KeyboardInterrupt:
        pass
    finally:
        driver.quit()

if __name__ == "__main__":
    open_okx_explorer()