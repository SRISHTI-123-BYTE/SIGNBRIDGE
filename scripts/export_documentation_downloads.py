# scripts/export_documentation_downloads.py
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

ARTIFACT_PATH = r"C:/Users/srish/.gemini/antigravity/brain/e9420bd3-4680-46f2-93da-03f387159bbe/algorithms_documentation.md"
DOWNLOADS_DIR = r"C:/Users/srish/Downloads"
FRONTEND_PUBLIC = r"frontend/public"

with open(ARTIFACT_PATH, 'r', encoding='utf-8') as f:
    md_content = f.read()

# 1. Save Markdown copy to Downloads
dest_md = os.path.join(DOWNLOADS_DIR, "SignBridge_Algorithms_Documentation.md")
with open(dest_md, 'w', encoding='utf-8') as f:
    f.write(md_content)
print(f"Exported Markdown to: {dest_md}")

# 2. Save Markdown copy to frontend/public for browser direct download
dest_fe_md = os.path.join(FRONTEND_PUBLIC, "SignBridge_Algorithms_Documentation.md")
with open(dest_fe_md, 'w', encoding='utf-8') as f:
    f.write(md_content)
print(f"Exported Markdown to: {dest_fe_md}")

# 3. Create standalone HTML with KaTeX, Mermaid, and Print-to-PDF styling
html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SignBridge AI: Algorithms & Implementation Documentation</title>
  <!-- KaTeX CSS & JS -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body, {{
      delimiters: [
        {{left: '$$', right: '$$', display: true}},
        {{left: '$', right: '$', display: false}}
      ]
    }});"></script>
  <!-- Mermaid -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>mermaid.initialize({{startOnLoad: true, theme: 'dark'}});</script>
  <!-- Marked Markdown Parser -->
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    :root {{
      --bg: #0b0f19;
      --card-bg: #111827;
      --text: #e2e8f0;
      --text-muted: #94a3b8;
      --border: #1e293b;
      --primary: #6366f1;
      --accent: #10b981;
      --code-bg: #0f172a;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.65;
      padding: 2.5rem 1.5rem;
      margin: 0;
    }}
    .container {{
      max-width: 960px;
      margin: 0 auto;
    }}
    .download-bar {{
      position: sticky;
      top: 1rem;
      z-index: 50;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(17, 24, 39, 0.95);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border);
      padding: 0.75rem 1.25rem;
      border-radius: 1rem;
      margin-bottom: 2rem;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }}
    .download-btn {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: var(--primary);
      color: white;
      text-decoration: none;
      font-weight: 600;
      font-size: 0.85rem;
      padding: 0.5rem 1rem;
      border-radius: 0.5rem;
      border: none;
      cursor: pointer;
      transition: background 0.2s;
    }}
    .download-btn:hover {{
      background: #4f46e5;
    }}
    .download-btn.secondary {{
      background: #1e293b;
      color: #cbd5e1;
      border: 1px solid #334155;
    }}
    .download-btn.secondary:hover {{
      background: #334155;
      color: white;
    }}
    h1, h2, h3, h4 {{
      color: #f8fafc;
      font-weight: 800;
      margin-top: 2rem;
      margin-bottom: 0.75rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.5rem;
    }}
    h1 {{ font-size: 2rem; border-bottom: 2px solid var(--primary); }}
    h2 {{ font-size: 1.5rem; }}
    h3 {{ font-size: 1.2rem; border-bottom: none; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1.5rem 0;
      background: var(--card-bg);
      border-radius: 0.75rem;
      overflow: hidden;
      border: 1px solid var(--border);
      font-size: 0.875rem;
    }}
    th, td {{
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--border);
      text-align: left;
    }}
    th {{
      background: #1e293b;
      color: #f1f5f9;
      font-weight: 700;
    }}
    tr:last-child td {{
      border-bottom: none;
    }}
    pre {{
      background: var(--code-bg);
      border: 1px solid var(--border);
      border-radius: 0.75rem;
      padding: 1.25rem;
      overflow-x: auto;
      font-size: 0.85rem;
      line-height: 1.5;
    }}
    code {{
      font-family: "JetBrains Mono", Consolas, Monaco, monospace;
      color: #a5b4fc;
      background: rgba(99, 102, 241, 0.12);
      padding: 0.15rem 0.35rem;
      border-radius: 0.25rem;
      font-size: 0.88em;
    }}
    pre code {{
      background: transparent;
      padding: 0;
      color: #e2e8f0;
    }}
    blockquote {{
      border-left: 4px solid var(--primary);
      margin: 1.5rem 0;
      padding: 0.75rem 1.25rem;
      background: rgba(99, 102, 241, 0.08);
      border-radius: 0 0.5rem 0.5rem 0;
      color: #cbd5e1;
    }}
    .mermaid {{
      background: var(--card-bg);
      padding: 1.5rem;
      border-radius: 0.75rem;
      border: 1px solid var(--border);
      margin: 1.5rem 0;
      overflow-x: auto;
    }}
    @media print {{
      body {{
        background: white !important;
        color: black !important;
        padding: 0;
      }}
      .download-bar {{
        display: none !important;
      }}
      pre, table {{
        page-break-inside: avoid;
        border: 1px solid #ccc !important;
        background: #f9f9f9 !important;
      }}
      th {{
        background: #eee !important;
        color: black !important;
      }}
      td, th {{
        border: 1px solid #ddd !important;
      }}
      code {{
        color: #111 !important;
        background: #f0f0f0 !important;
      }}
      h1, h2, h3 {{
        color: black !important;
        border-color: #ddd !important;
      }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="download-bar">
      <div>
        <strong style="color: white; font-size: 0.95rem;">SignBridge AI Technical Documentation</strong>
        <span style="display: block; font-size: 0.75rem; color: var(--text-muted);">Complete Mathematical & Architectural Specification</span>
      </div>
      <div style="display: flex; gap: 0.5rem;">
        <button onclick="window.print()" class="download-btn">
          🖨️ Print / Save as PDF
        </button>
        <a href="SignBridge_Algorithms_Documentation.md" download class="download-btn secondary">
          📄 Download Markdown (.md)
        </a>
      </div>
    </div>
    <div id="content"></div>
  </div>

  <script id="raw-markdown" type="text/plain">
{md_content}
  </script>

  <script>
    const rawMd = document.getElementById('raw-markdown').textContent;
    // Replace mermaid blocks with div.mermaid
    const parsed = marked.parse(rawMd);
    document.getElementById('content').innerHTML = parsed;
    
    // Replace code blocks with class language-mermaid to div.mermaid
    document.querySelectorAll('pre code.language-mermaid').forEach(block => {{
      const div = document.createElement('div');
      div.className = 'mermaid';
      div.textContent = block.textContent;
      block.parentElement.replaceWith(div);
    }});
  </script>
</body>
</html>
"""

# Save HTML copy to Downloads
dest_html = os.path.join(DOWNLOADS_DIR, "SignBridge_Algorithms_Documentation.html")
with open(dest_html, 'w', encoding='utf-8') as f:
    f.write(html_template)
print(f"Exported HTML to: {dest_html}")

# Save HTML copy to frontend/public for in-browser viewing / download
dest_fe_html = os.path.join(FRONTEND_PUBLIC, "SignBridge_Algorithms_Documentation.html")
with open(dest_fe_html, 'w', encoding='utf-8') as f:
    f.write(html_template)
print(f"Exported HTML to: {dest_fe_html}")

print("\n=== ALL EXPORTS GENERATED SUCCESSFULLY! ===")
