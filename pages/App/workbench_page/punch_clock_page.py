# 打卡-页面
from pages.App.app import App


class PunchClock(App):
    def __init__(self, driver):
        super().__init__(driver)
        # 设置等待页面动态加载超时时间为1s
        self.driver.update_settings({'waitForIdleTimeout': 1})

    def click_go_out(self):
        # self.scroll_page("打卡")
        self.find_xtext_click("外出打卡")
        self.find_xtext_click("次外出", True)

        # assert self.find_xtext_ele("外出打卡成功").text == '外出打卡成功'
