# WANGZI's Tech Blog 🚀



## 🏗️ 技术栈版本与选型依据

[![Python 3.8.8](https://img.shields.io/badge/Python-3.8.8-3776AB?logo=python&logoColor=white)](https://www.python.org/)  [![Flask 3.0.3](https://img.shields.io/badge/Flask-3.0.3-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)  [![MinIO RELEASE.2025-02-18T16-25-55Z](https://img.shields.io/badge/MinIO-RELEASE.2025--02--18T16--25--55Z-7D42AE?logo=minio&logoColor=white)](https://min.io/)  [![Docker 26.1.3](https://img.shields.io/badge/Docker-26.1.3-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)  [![MySQL 8.3.0](https://img.shields.io/badge/MySQL-8.3.0-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)  [![Nginx 1.14.1](https://img.shields.io/badge/Nginx-1.14.1-009639?logo=nginx&logoColor=white)](https://nginx.org/)

**线上演示**：https://www.wzportia.tech/



## 🎯 项目定位

一个全栈开发的个人博客，集技术分享、日常感悟、个人成长于一体，核心功能：
- **技术实践**：展示项目开发经验
- **持续学习**：分享日常学习心得
- **计划执行**：记录个人成长计划



## 🛠 技术全景

| 领域       | 技术选型                |
| ---------- | ----------------------- |
| **前端**   | JavaScript + CSS + HTML |
| **后端**   | Python + Flask          |
| **数据库** | MySQL + Minio           |
| **运维**   | Docker + Nginx          |



## 🖥 系统架构

```mermaid
graph TD
    A[用户] --> B[Nginx]
    B --> C[前端静态资源]
    B --> D[Flask应用集群]
    D --> E[(MySQL)]
    D --> F[(Redis)]
    D --> G[(Minio)]

```
