from pathlib import Path
import re, zipfile, shutil

base = Path("/mnt/data")
source = base / "Sleepy_수면패턴_핵심기능.html"
project = base / "sleepy-github"
(project / "css").mkdir(parents=True, exist_ok=True)
(project / "js").mkdir(parents=True, exist_ok=True)

html = source.read_text(encoding="utf-8")

style_match = re.search(r"<style>(.*?)</style>", html, re.S)
script_match = re.search(r"<script>(.*?)</script>", html, re.S)
if not style_match or not script_match:
    raise ValueError("HTML에서 CSS 또는 JavaScript를 찾을 수 없습니다.")

css = style_match.group(1).strip() + "\n"
js = script_match.group(1).strip() + "\n"

index = html
index = re.sub(r"<style>.*?</style>", '  <link rel="stylesheet" href="css/style.css">', index, count=1, flags=re.S)
index = re.sub(r"<script>.*?</script>", '  <script src="js/script.js"></script>', index, count=1, flags=re.S)
index = index.replace("</head>", '  <meta name="description" content="수면 기록과 목표 시간 관리로 규칙적인 수면 습관을 돕는 Sleepy 앱입니다.">\n</head>')
(project / "index.html").write_text(index, encoding="utf-8")
(project / "css" / "style.css").write_text(css, encoding="utf-8")
(project / "js" / "script.js").write_text(js, encoding="utf-8")

readme = """# Sleepy 🌙
