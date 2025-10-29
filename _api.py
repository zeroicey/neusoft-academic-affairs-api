from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from website import Website
from database import DatabaseManager
import logging
from typing import Dict, Any

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="东软学院教务系统API", version="1.0.0")

# 请求模型
class LoginRequest(BaseModel):
    student_id: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    student_id: str
    cookie_cached: bool

# 全局数据库管理器
db_manager = DatabaseManager()

@app.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest) -> LoginResponse:
    """
    用户登录接口
    - 首先检查数据库中是否有有效的cookie
    - 如果有有效cookie，直接返回成功
    - 如果没有，进行登录并保存cookie
    """
    try:
        # 检查是否已有有效cookie
        cached_cookie = db_manager.get_valid_cookie(request.student_id)
        if cached_cookie:
            logger.info(f"学号 {request.student_id} 使用缓存的cookie登录")
            return LoginResponse(
                success=True,
                message="使用缓存cookie登录成功",
                student_id=request.student_id,
                cookie_cached=True
            )
        
        # 创建Website实例并尝试登录
        website = Website(request.student_id, request.password)
        
        # 获取cookie（会自动保存到数据库）
        website.get_cookie()
        
        # 尝试登录
        website.login()
        
        logger.info(f"学号 {request.student_id} 登录成功，cookie已保存")
        
        return LoginResponse(
            success=True,
            message="登录成功，cookie已保存",
            student_id=request.student_id,
            cookie_cached=False
        )
        
    except Exception as e:
        logger.error(f"学号 {request.student_id} 登录失败: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"登录失败: {str(e)}"
        )

@app.get("/cookie/status/{student_id}")
async def check_cookie_status(student_id: str) -> Dict[str, Any]:
    """
    检查指定学号的cookie状态
    """
    try:
        cached_cookie = db_manager.get_valid_cookie(student_id)
        
        return {
            "student_id": student_id,
            "has_valid_cookie": cached_cookie is not None,
            "cookie_preview": cached_cookie[:20] + "..." if cached_cookie else None
        }
        
    except Exception as e:
        logger.error(f"检查cookie状态失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"检查cookie状态失败: {str(e)}"
        )

@app.delete("/cookie/{student_id}")
async def invalidate_cookie(student_id: str) -> Dict[str, str]:
    """
    使指定学号的cookie失效
    """
    try:
        db_manager.invalidate_cookie(student_id)
        logger.info(f"学号 {student_id} 的cookie已失效")
        
        return {
            "message": f"学号 {student_id} 的cookie已失效",
            "student_id": student_id
        }
        
    except Exception as e:
        logger.error(f"使cookie失效失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"使cookie失效失败: {str(e)}"
        )

@app.post("/cleanup")
async def cleanup_expired_cookies() -> Dict[str, str]:
    """
    清理所有过期的cookie
    """
    try:
        db_manager.cleanup_expired_cookies()
        logger.info("过期cookie清理完成")
        
        return {"message": "过期cookie清理完成"}
        
    except Exception as e:
        logger.error(f"清理过期cookie失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"清理过期cookie失败: {str(e)}"
        )

@app.get("/")
async def root():
    """
    根路径，返回API信息
    """
    return {
        "message": "东软学院教务系统API",
        "version": "1.0.0",
        "endpoints": {
            "login": "POST /login - 用户登录",
            "cookie_status": "GET /cookie/status/{student_id} - 检查cookie状态",
            "invalidate_cookie": "DELETE /cookie/{student_id} - 使cookie失效",
            "cleanup": "POST /cleanup - 清理过期cookie"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)