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

如果可选 SQLite 依赖无法安装，现有工程提供降级路径。Windows PowerShell 示例：

```powershell
npm ci --omit=optional
$env:DISABLE_SQLITE_CACHE="1"
$env:DISABLE_SQLITE_PERSISTENCE="1"
npm start
```

降级会影响缓存与持久化能力，不能视为生产部署的等价替代。

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
