# 教务系统API

这是一个用于访问教务系统的API服务，提供了获取课表和成绩等功能。

## 功能特性

- 获取学生课表信息
- 获取学生成绩信息
- 自动处理验证码识别
- RESTful API设计

## 技术栈

- FastAPI: 现代、高性能的Web框架
- ddddocr: 用于验证码识别
- Requests: 用于HTTP请求处理

## 安装与使用

### 环境要求

- Python 3.8+

### 安装依赖

```bash

# 使用uv安装
uv pip install -r requirements.txt
uv run fastapi dev api.py
```

### 运行服务

```bash
uvicorn api:app --reload
```

服务将在 http://localhost:8000 上运行。

## API接口

### 获取课表

```
GET /schedule
```

参数:
- studentNo: 学号
- password: 密码
- term: 学期，如 20251
- week: 周数

示例请求:
```
http://localhost:8000/schedule?studentNo=123456&password=yourpassword&term=20251&week=9
```

### 获取成绩

```
GET /grades
```

参数:
- studentNo: 学号
- password: 密码
- term: 学期（可选）

示例请求:
```
http://localhost:8000/grades?studentNo=123456&password=yourpassword&term=20242
```

## 开发说明

项目结构:
- api.py: FastAPI应用和路由定义
- website.py: 教务系统网站交互逻辑
- task.py: 任务处理相关功能

## 注意事项

- 本API仅供学习和个人使用
- 请勿频繁请求教务系统，以免对服务器造成压力
- 请妥善保管个人账号密码信息

## 许可证

MIT