from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException
from website import Website

app = FastAPI()


@app.get("/schedule")
def get_schedule(
    studentNo: str = Query(..., description="学号"),
    password: str = Query(..., description="密码"),
    term: str = Query(..., description="学期，如 20251"),
    week: str = Query(..., description="周数"),
):
    """
    获取学生课表
    按照流程：get_cookie() -> login() -> get_course_schedule() -> logout()
    """
    try:
        # 创建Website实例
        website = Website(studentNo, password)
        
        # 1. 获取cookie
        website.get_cookie()
        
        # 2. 登录
        website.login()
        
        # 3. 获取课表数据
        schedule_data = website.get_course_schedule(term or "20251", week or "9")
        
        # 4. 登出
        website.logout()
        
        return {
            "studentNo": studentNo,
            "term": term or "20251",
            "week": week or 1,
            "success": True,
            "items": schedule_data or []
        }
        
    except Exception as e:
        # 确保在出错时也尝试登出
        try:
            if 'website' in locals():
                website.logout()
        except:
            pass
            
        raise HTTPException(
            status_code=500,
            detail=f"获取课表失败: {str(e)}"
        )


@app.get("/grades")
def get_grades(
    studentNo: str = Query(..., description="学号"),
    password: str = Query(..., description="密码"),
    term: Optional[str] = Query(None, description="学期，可选"),
):
    """
    获取学生成绩
    按照流程：get_cookie() -> login() -> get_courses_grades() -> logout()
    """
    try:
        # 创建Website实例
        website = Website(studentNo, password)
        
        # 1. 获取cookie
        website.get_cookie()
        
        # 2. 登录
        website.login()
        
        # 3. 获取成绩数据
        grades_data = website.get_course_grades(term or "20242")
        
        # 4. 登出
        website.logout()
        
        return {
            "studentNo": studentNo,
            "term": term or "20242",
            "success": True,
            "items": grades_data or []
        }
        
    except Exception as e:
        # 确保在出错时也尝试登出
        try:
            if 'website' in locals():
                website.logout()
        except:
            pass
            
        raise HTTPException(
            status_code=500,
            detail=f"获取成绩失败: {str(e)}"
        )
