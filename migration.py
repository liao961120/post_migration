#%%
import re
import yaml
from pathlib import Path

src = Path("_posts")
tgt = Path("content/post")
pat_to_rm = [
    re.compile(r'{: width=["\']\d\d%["\']}'),
    re.compile(r"<!--more-->")
]
pat_assets = re.compile(r"(/assets)/[a-zA-Z0-9_/-]+\.(png|svg|jpg|jpeg|gif)")
pat_sourceCode = re.compile(r'<pre class="sourceCode [a-zA-Z0-9]+')

def main():
    for fp in src.glob("*"):
        migrate_post(fp, tgt)



def migrate_post(fp, tgt_dir):
    meta = write_post_yaml(fp)
    content = read_post_content(fp)
    fn, ext, _ = get_post_name_date(fp)
    out_fp = tgt_dir / (fn + ext)

    with open(out_fp, "w", encoding="utf-8") as f:
        f.write(meta + content)


def read_post_content(fp):
    post_content = ""
    with open(fp, encoding="utf-8") as f:
        inYaml = False
        for line in f:
            if line.startswith('---') and (not inYaml):
                inYaml = True
                continue
            if (line.startswith('---') or line.startswith('...')) and inYaml:
                inYaml = False
                continue
            if inYaml: continue

            # Remove Jekyll-specific shortcodes
            for pat in pat_to_rm:
                if pat.search(line): line = pat.sub("", line)
            if pat_assets.search(line): line = line.replace("/assets", "https://img.yongfu.name/assets")
            if pat_sourceCode.search(line): line = line.replace("sourceCode ", "language-")

            post_content += line
    return post_content


def write_post_yaml(fp):
    fn, _, date = get_post_name_date(fp)
    meta = read_post_yaml(fp)
    meta["date"] = '-'.join(date)
    meta["aliases"] = [f'/{"/".join(date)}/{fn}.html']
    if "mathjax" in meta:
        meta["katex"] = meta["mathjax"]
        del meta["mathjax"]
    return '---\n' + yaml.dump(meta, allow_unicode=True) + '---\n\n'


def get_post_name_date(fp):
    fp_split = fp.stem.split("-")
    date = fp_split[:3]
    fn = '-'.join(fp_split[3:])
    ext = fp.name.replace(fp.stem, "")
    return fn, ext, date


def read_post_yaml(fp):
    yaml_str = ""
    with open(fp, encoding="utf-8") as f:
        inYaml = False
        for line in f:
            if line.startswith('---') and (not inYaml):
                inYaml = True
                continue
            if (line.startswith('---') or line.startswith('...')) and inYaml:
                break
            if inYaml: yaml_str += line
    return yaml.load(yaml_str, Loader=yaml.FullLoader)



if __name__ == '__main__':
    main()
