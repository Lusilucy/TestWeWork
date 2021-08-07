from pages.App.app import App


class WorkBench(App):
    def click_punch_clock(self):
        for i in range(3):
            try:
                self.find_xtext_click("打卡")
                break
            except Exception as e:
                print(e)
        from pages.App.workbench_page.punch_clock_page import PunchClock
        return PunchClock(self.driver)
