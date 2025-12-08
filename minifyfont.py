import os
import subprocess
import argparse
import jinja_filters
import html
import string

# File types in which we want to search for used characters
SCAN_EXTENSIONS = {".html"}

def extract_used_characters(root_dir):
  """
  Walk through project files in root_dir and extract all literal characters used.
  """
  chars = set()

  for subdir, _, files in os.walk(root_dir):
    for filename in files:
      if os.path.splitext(filename)[1].lower() in SCAN_EXTENSIONS:
        file_path = os.path.join(subdir, filename)
        try:
          with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            text = html.unescape(text)
            for c in text:
              # Ignore control characters
              if ord(c) >= 32:
                chars.add(c)
        except Exception as e:
          print(f"Could not read {file_path}: {e}")

  return "".join(sorted(chars))


def write_chars_file(chars, output_file):
  with open(output_file, "w", encoding="utf-8") as f:
    f.write(chars)
  print(f"[OK] Saved used character list to {output_file}")


def get_all_used_characters(site_root_dir):
  """
  Combines:
  - Literal characters from site files
  - Selected Nerd Font icons
  - Always includes 0-9, a-z, A-Z
  """
  chars = set()

  # Always include alphanumerics
  chars.update(string.ascii_lowercase)
  chars.update(string.ascii_uppercase)
  chars.update(string.digits)

  # Add characters found in site
  chars.update(extract_used_characters(site_root_dir))

  # Add Python mapping icons
  chars.update(jinja_filters.LANGUAGE_MAPPING.values())

  return "".join(sorted(chars))


def subset_font(font_path, chars_file, output_path):
  """
  Use pyftsubset to generate a minimized .woff2 font containing only used chars.
  """
  cmd = [
    "pyftsubset",
    font_path,
    f"--output-file={output_path}",
    f"--text-file={chars_file}",
    "--flavor=woff2",
    "--layout-features='*'",
    "--glyph-names",
    "--symbol-cmap",
    "--legacy-cmap",
    "--notdef-glyph",
    "--notdef-outline",
    "--no-recalc-bounds",
    "--no-hinting",
    "--drop-tables=FFTM"
  ]

  print(f"[RUNNING] {' '.join(cmd)}")
  subprocess.run(" ".join(cmd), shell=True, check=True)
  print(f"[OK] Subset font written to {output_path}")


def main():
  parser = argparse.ArgumentParser(description="Subset Nerd Font .woff2 files for deployment")
  parser.add_argument("--site-dir", required=True, help="Directory containing source files")
  parser.add_argument("--fonts-dir", required=True, help="Directory containing .woff2 fonts")
  parser.add_argument("--output-dir", required=True, help="Directory to write subset fonts")

  args = parser.parse_args()

  os.makedirs(args.output_dir, exist_ok=True)

  print("[*] Extracting characters used in site...")
  chars = get_all_used_characters(args.site_dir)

  chars_file = os.path.join(args.output_dir, "used_chars.txt")
  write_chars_file(chars, chars_file)

  print("[*] Subsetting fonts...")
  for filename in os.listdir(args.fonts_dir):
    if filename.lower().endswith(".woff2") and not filename.lower().endswith(".subset.woff2"):
      font_path = os.path.join(args.fonts_dir, filename)

      out_path = os.path.join(
        args.output_dir,
        os.path.splitext(filename)[0] + ".subset.woff2"
      )

      subset_font(font_path, chars_file, out_path)

  print("Done!\n")


if __name__ == "__main__":
  main()
