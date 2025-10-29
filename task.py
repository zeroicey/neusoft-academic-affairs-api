import threading

from rich.logging import RichHandler
import website
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)

logger = logging.getLogger("rich")

def grab_class_task(student_id, password, kcrwdm, kcmc):
    web = website.Website(student_id, password)
    web.get_cookie()
    while True:
        try:
            web.login()
            logging.info("学号 %s 登录成功", student_id)
            break
        except Exception as e:
            logging.error("学号 %s 登录失败：%s", student_id, e)
            logging.info("正在重试登录...")
    logging.info("开始选课任务，学号：%s", student_id)
    frequency = 10
    for i in range(frequency):
        try:
            res = web.grab_class(kcrwdm, kcmc)
            logger.info("学号 %s 第%s次 抢课结果：%s", student_id, i + 1, res)
        except Exception as e:
            logging.error("学号 %s 第%s次 抢课出错：%s", student_id, i + 1, e)
    try:
        web.logout()
        logging.info("学号 %s 登出成功", student_id)
    except Exception as e:
        logging.error("学号 %s 登出出错：%s", student_id, e)

info = []

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    threads = []
    for student_id, password, kcrwdm, kcmc in info:
        t = threading.Thread(target=grab_class_task, args=(student_id, password, kcrwdm, kcmc, ))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    logging.info("所有任务完成")