import re

with open('views_fix.py', 'r') as f:
    fix_content = f.read()

with open('tender_app/views.py', 'r') as f:
    views_content = f.read()

pattern = r'def all_framework_agreements_view\([^)]*\):.*?return render\([^)]*\)[^\n]*\n'
replacement = fix_content

updated_content = re.sub(pattern, replacement, views_content, flags=re.DOTALL)

with open('tender_app/views_updated.py', 'w') as f:
    f.write(updated_content)

