# 拾光盒子 CampusLoop：本地 MVP

适用于获得授权的 MVP 源码。本公开展示仓库不包含应用或数据库。

## 环境

推荐 Python 3.12、pip 及隔离虚拟环境。项目使用 Flask 和 SQLite，依赖声明位于 `requirements.txt`。

## 本地运行

在源码根目录执行：

```bash
python -m venv .venv
```

激活虚拟环境后执行：

```bash
python -m pip install -r requirements.txt
python server/app.py
```

访问 `http://localhost:8088`。现有入口会初始化本地数据库，并监听所有网络接口；仅在可信开发网络中使用，不应未经安全改造直接暴露到公网。

## 演示顺序

闲置登记 → 品相与状态流转 → 组合包浏览 → 预约与取货状态 → 运营面板。公开截图中的数据为演示用途。

## 上线前仍需解决

- 正式身份认证与服务端权限控制。
- 真实支付及退款对账，而非仅改变业务状态。
- 数据备份、输入与上传校验、隐私告知和日志脱敏。
- 生产 Web 服务、HTTPS、运维与恢复流程。

现有 mock 身份、价格预测和模拟运营指标不等于这些能力已经完成。源码中有流程测试，本次未运行，不宣称最新测试通过。

[项目介绍](../../projects/campusloop.md) · [部署总览](../deployment.md)
