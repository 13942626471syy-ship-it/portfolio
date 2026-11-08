# WhiteGZ：运行前提与发布检查

适用于获得授权的 WhiteGZ 源码，不适用于本展示仓库。

## 环境与配置

- Node.js 最低 20.18.1，现有预检推荐 Node.js 22 LTS。
- npm 与项目锁文件。
- 根据私有工程的配置模板设置自己的初始强密码、会话密钥及所需模型配置。不要使用演示默认口令上线，不把真实值提交到 Git。
- 企业检索和远程模型能力需要网络；静态资源本地化不等于所有功能完全离线。

## 本地运行

在已授权源码根目录执行：

```bash
npm ci
npm start
```

默认访问 `http://localhost:3001`。启动脚本执行 Express 服务；端口可按私有工程配置调整。

在第二个终端做最小检查，Windows PowerShell 使用 `curl.exe`：

```powershell
curl.exe --fail http://127.0.0.1:3001/api/health
```

应收到包含 `status: "ok"` 的 JSON。这只证明 HTTP 服务有响应。随后用合成数据查看报告、证据和图表编辑流程；检索、模型生成和导出需要各自验证。

如果可选 SQLite 依赖无法安装，现有工程提供降级路径。Windows PowerShell 示例：

```powershell
npm ci --omit=optional
$env:DISABLE_SQLITE_CACHE="1"
$env:DISABLE_SQLITE_PERSISTENCE="1"
npm start
```

降级会影响缓存与持久化能力，不能视为生产部署的等价替代。

## 常见问题

| 现象 | 检查方向 |
| --- | --- |
| 3001 端口被占用 | 先确认占用者；ISAD 后端也默认使用 3001。按工程配置改端口，避免终止不属于本项目的服务 |
| 本地页面能开，模型或检索失败 | 检查对应配置、网络和权限；静态页面可用不代表远程能力已就绪 |
| 证据显示待核验、页码未知 | 补充来源与定位信息，不能通过隐藏提示来替代核验 |

## 更新与恢复

升级前固定源码版本，并备份私有运行目录和配置。新版本先在独立演示目录验证；恢复旧版本时同时检查数据格式兼容性。不要用本展示仓库覆盖产品目录。

## 发布前检查入口

```bash
npm run preflight
npm run check:syntax
npm test
npm run test:integration
npm run ci:release
```

还有浏览器、图表与 PDF 的专项 smoke 入口，以及 `npm run package:release` 打包入口。不同检查可能需要服务、浏览器或模型条件，执行前阅读私有工程说明。

## 验证边界

上述命令已核对包配置，本次没有实际运行它们。公开截图是历史本地回放或合成数据，不是最新线上验收。GitHub Pages 不能承载此 Express 后端。

[项目介绍](../../projects/whitegz.md) · [部署总览](../deployment.md)
