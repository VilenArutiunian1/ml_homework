import os
import sys
import json

# Папки, которые нужно пропускать (виртуальные окружения и системные)
EXCLUDED_DIRS = {'venv', '.venv', 'env', '.env', 'jupyter_env', '__pycache__', '.git', '.idea', '.vscode'}

def should_skip_dir(dirname):
    """Пропускаем скрытые папки и стандартные папки окружений."""
    return dirname.startswith('.') or dirname in EXCLUDED_DIRS

def analyze_py(filepath):
    """Анализирует .py файл: возвращает (total, code, comment, blank)."""
    total = code = comment = blank = 0
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                total += 1
                stripped = line.strip()
                if not stripped:
                    blank += 1
                elif stripped.startswith('#'):
                    comment += 1
                else:
                    code += 1
    except Exception as e:
        print(f"Ошибка при чтении {filepath}: {e}", file=sys.stderr)
        return 0, 0, 0, 0
    return total, code, comment, blank

def analyze_ipynb(filepath):
    """Анализирует .ipynb (только code-ячейки): (total, code, comment, blank)."""
    total = code = comment = blank = 0
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                print(f"Предупреждение: пустой файл {filepath}", file=sys.stderr)
                return 0, 0, 0, 0
            notebook = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON в {filepath}: {e}", file=sys.stderr)
        return 0, 0, 0, 0
    except Exception as e:
        print(f"Ошибка при обработке {filepath}: {e}", file=sys.stderr)
        return 0, 0, 0, 0

    for cell in notebook.get('cells', []):
        if cell.get('cell_type') != 'code':
            continue
        source = cell.get('source', '')
        source_lines = source if isinstance(source, list) else source.splitlines(True)
        for line in source_lines:
            total += 1
            stripped = line.strip()
            if not stripped:
                blank += 1
            elif stripped.startswith('#'):
                comment += 1
            else:
                code += 1
    return total, code, comment, blank

def main():
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'

    stats = {
        'py':   {'total': 0, 'code': 0, 'comment': 0, 'blank': 0},
        'ipynb': {'total': 0, 'code': 0, 'comment': 0, 'blank': 0}
    }

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Фильтруем папки: удаляем те, которые нужно пропустить
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]

        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            ext = os.path.splitext(filename)[1].lower()
            if ext == '.py':
                t, c, cm, b = analyze_py(filepath)
                stats['py']['total']   += t
                stats['py']['code']    += c
                stats['py']['comment'] += cm
                stats['py']['blank']   += b
            elif ext == '.ipynb':
                t, c, cm, b = analyze_ipynb(filepath)
                stats['ipynb']['total']   += t
                stats['ipynb']['code']    += c
                stats['ipynb']['comment'] += cm
                stats['ipynb']['blank']   += b

    total = {k: sum(stat[k] for stat in stats.values()) for k in ['total', 'code', 'comment', 'blank']}

    print(f"{'Category':<18} {'Total':>8} {'Code':>8} {'Comment':>8} {'Blank':>8}")
    print("-" * 56)
    for label, key in [("Python (.py)", "py"), ("Jupyter (.ipynb)", "ipynb")]:
        s = stats[key]
        print(f"{label:<18} {s['total']:>8} {s['code']:>8} {s['comment']:>8} {s['blank']:>8}")
    print("-" * 56)
    print(f"{'TOTAL':<18} {total['total']:>8} {total['code']:>8} {total['comment']:>8} {total['blank']:>8}")

if __name__ == "__main__":
    main()