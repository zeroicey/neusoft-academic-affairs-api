import requests
import json
from database import DatabaseManager

# API基础URL
BASE_URL = "http://localhost:8000"

def test_database_functionality():
    """测试数据库功能"""
    print("=== 测试数据库功能 ===")
    
    db = DatabaseManager()
    
    # 测试保存cookie
    test_student_id = "test123"
    test_cookie = "JSESSIONID=test_cookie_value"
    
    db.save_cookie(test_student_id, test_cookie, expires_minutes=1)
    print(f"✓ 保存cookie成功: {test_student_id}")
    
    # 测试获取有效cookie
    retrieved_cookie = db.get_valid_cookie(test_student_id)
    if retrieved_cookie == test_cookie:
        print(f"✓ 获取有效cookie成功: {retrieved_cookie}")
    else:
        print(f"✗ 获取cookie失败，期望: {test_cookie}, 实际: {retrieved_cookie}")
    
    # 测试使cookie无效
    db.invalidate_cookie(test_student_id)
    invalid_cookie = db.get_valid_cookie(test_student_id)
    if invalid_cookie is None:
        print("✓ cookie失效功能正常")
    else:
        print(f"✗ cookie失效功能异常，仍然返回: {invalid_cookie}")
    
    print()

def test_api_endpoints():
    """测试API接口"""
    print("=== 测试API接口 ===")
    
    try:
        # 测试根路径
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✓ 根路径接口正常")
            print(f"  响应: {response.json()['message']}")
        else:
            print(f"✗ 根路径接口异常: {response.status_code}")
        
        # 测试cookie状态检查
        test_student_id = "test456"
        response = requests.get(f"{BASE_URL}/cookie/status/{test_student_id}")
        if response.status_code == 200:
            print("✓ cookie状态检查接口正常")
            data = response.json()
            print(f"  学号: {data['student_id']}, 有效cookie: {data['has_valid_cookie']}")
        else:
            print(f"✗ cookie状态检查接口异常: {response.status_code}")
        
        # 测试清理过期cookie
        response = requests.post(f"{BASE_URL}/cleanup")
        if response.status_code == 200:
            print("✓ 清理过期cookie接口正常")
            print(f"  响应: {response.json()['message']}")
        else:
            print(f"✗ 清理过期cookie接口异常: {response.status_code}")
        
        # 测试使cookie失效
        response = requests.delete(f"{BASE_URL}/cookie/{test_student_id}")
        if response.status_code == 200:
            print("✓ 使cookie失效接口正常")
            print(f"  响应: {response.json()['message']}")
        else:
            print(f"✗ 使cookie失效接口异常: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("✗ 无法连接到API服务器，请确保服务器正在运行")
        print("  启动命令: python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"✗ 测试过程中出现错误: {e}")
    
    print()

def test_login_simulation():
    """模拟登录测试（不实际连接教务系统）"""
    print("=== 模拟登录测试 ===")
    print("注意: 这个测试会尝试连接真实的教务系统，如果没有有效的学号密码会失败")
    print("这是正常的，主要是测试API接口的结构是否正确")
    
    try:
        login_data = {
            "student_id": "test_student",
            "password": "test_password"
        }
        
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        
        if response.status_code == 400:
            print("✓ 登录接口结构正常（预期会因为测试数据而失败）")
            error_detail = response.json().get("detail", "")
            if "登录失败" in error_detail:
                print("  错误信息符合预期")
        elif response.status_code == 200:
            print("✓ 登录成功（如果使用了真实的学号密码）")
            data = response.json()
            print(f"  学号: {data['student_id']}, 成功: {data['success']}")
        else:
            print(f"✗ 登录接口异常: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("✗ 无法连接到API服务器")
    except Exception as e:
        print(f"✗ 测试过程中出现错误: {e}")
    
    print()

if __name__ == "__main__":
    print("开始测试抢课API系统...")
    print()
    
    # 测试数据库功能
    test_database_functionality()
    
    # 测试API接口
    test_api_endpoints()
    
    # 模拟登录测试
    test_login_simulation()
    
    print("测试完成！")
    print()
    print("如果要启动API服务器，请运行:")
    print("python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000")
    print()
    print("然后可以访问 http://localhost:8000/docs 查看API文档")