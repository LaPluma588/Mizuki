import { visit } from "unist-util-visit";

/**
 * rehype 插件：为外部图片添加 referrerpolicy="no-referrer"
 * 根据 siteConfig.imageOptimization.noReferrerDomains 的配置，匹配图片域名
 * 解决 CDN 防盗链（如 B 站图床）导致的图片 403 问题
 */
export function rehypeImageNoReferrer() {
	return (tree) => {
		visit(tree, "element", (node) => {
			if (node.tagName === "img" && node.properties?.src) {
				const src = node.properties.src;
				if (typeof src === "string" && src.startsWith("http")) {
					try {
						const hostname = new URL(src).hostname;
						// 匹配配置中 *.hdslb.com 等防盗链域名
						const domains = [
							"*.hdslb.com",
						];
						const matched = domains.some((pattern) => {
							const regexPattern = pattern.replace(/\./g, "\\.").replace(/\*/g, ".*");
							return new RegExp(`^${regexPattern}$`).test(hostname);
						});
						if (matched) {
							node.properties.referrerpolicy = "no-referrer";
						}
					} catch {
						// 忽略无效 URL
					}
				}
			}
		});
	};
}
